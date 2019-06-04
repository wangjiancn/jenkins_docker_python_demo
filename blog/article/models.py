from django.db import models
from django.db.models import Manager
from utils.base_model import BaseModel
from utils.tool import is_uuid
from acl.models import UserProfile


# Create your models here.

class Tag(BaseModel):
    user_uuid = models.CharField("用户UUID", null=True, max_length=64)
    name = models.CharField(max_length=20, db_index=True, unique=True)
    desc = models.CharField(max_length=50, db_index=True, default='no desciption')


class Category(BaseModel):
    user_uuid = models.CharField("用户UUID", null=True, max_length=64)
    name = models.CharField("分类", max_length=50)
    desc = models.CharField("描述", max_length=50, default='no desciption')


class Comment(BaseModel):
    body = models.TextField("评论内容")
    markdown = models.TextField()
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    parent = models.ForeignKey("self", verbose_name="", on_delete=models.CASCADE, null=True)


class Like(BaseModel):
    from_user_uuid = models.UUIDField("收藏用户UUID")
    to_user_uuid = models.UUIDField("被收藏文章作者UUID")
    kind = models.CharField("类型(文章/wiki/FAQ...)", max_length=50)
    target_uuid = models.UUIDField("被收藏内容的UUID")
    fav_name = models.CharField("收藏夹名称", max_length=50)


class LikeFolder(BaseModel):
    name = models.CharField("名称", max_length=50)
    desc = models.CharField("介绍", max_length=200)
    author = models.ForeignKey(UserProfile, verbose_name="用户ID", on_delete=models.CASCADE)


class Rate(BaseModel):
    target_uuid = models.UUIDField("被收藏内容的UUID")
    goal = models.SmallIntegerField("评分")
    from_user_uuid = models.UUIDField("点赞用户UUID")
    to_user_uuid = models.UUIDField("被点赞用户UUID")
    kind = models.CharField("类型(文章/评论...)", max_length=50)


class Post(BaseModel):

    POST_KIND_OPTIONS = [('原创', '原创'), ('转载', '转载'), ('翻译', '翻译'), ('笔记', '笔记')]
    POST_STATE_OPTIONS = [('草稿', '草稿'), ('已发布', '已发布'), ('已保存', '已保存')]

    desc = models.CharField("描述", max_length=200, db_index=True)
    private = models.BooleanField("是否为私密文章", default=False, db_index=True)
    title = models.CharField("标题", max_length=100, db_index=True)
    tags = models.ManyToManyField(Tag)
    markdown = models.TextField("Markdown正文")
    body = models.TextField("HTML正文")
    kind = models.CharField("类型(文章/原创/笔记)", choices=POST_KIND_OPTIONS, db_index=True, max_length=50)
    state = models.CharField("类型(文章/原创/笔记)", choices=POST_STATE_OPTIONS, db_index=True, max_length=50)
    views_count = models.IntegerField('访问次数', default=0, db_index=True)

    author = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)
    cat = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.id}-{self.title}'

    def to_dict(self):
        data = self._to_dict()
        data.update(
            tags=list(self.tags.values()) if self.tags else [],
            author=self.author.to_dict() if self.author else None)
        return data

    def update_tag(self, tags, user_id=0):
        if tags:
            tag_instances = []
            for tag in tags:
                if not is_uuid(tag):
                    tag_instances.append(Tag.objects.get_or_create(name=tag)[0])
                else:
                    tag_instances.append(Tag.objects.get(uuid=tag))
            self.tags.set(tag_instances)

    def add_view_count(self):
        self.views_count = self.views_count + 1
        self.save()
