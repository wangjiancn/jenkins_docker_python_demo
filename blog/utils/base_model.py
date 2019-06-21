import uuid
import datetime
from abc import abstractmethod

from django.db import models, transaction
from django_mysql.models import JSONField, Model

from acl.default_acl import row_acl
from utils.api_response import APIError, APIResponseError
from utils.tool import is_uuid


class MyQuerySet(models.QuerySet):
    def pagination(self, limit=20, offset=0):
        """分页

        Args:
            limit (int, optional): 返回数据条数. Defaults to 20.
            offset (int, optional): 偏移量. Defaults to 0.

        Returns:
            Dict: 返回格式如下:
                {
                    "meta": {
                        "total_count": 20,
                        "limit": 20,
                        "offset": 0
                    },
                    "objects": [
                        {
                            "id": 16,
                            "created": "2019-05-26T13:01:15.411Z",
                            "last_modified": "2019-05-26T13:01:15.411Z",
                            "name": "flask",
                        },
                        ......
                        {
                            "id": 36,
                            "created": "2019-06-16T11:00:48.618Z",
                            "last_modified": "2019-06-16T11:00:48.618Z",
                            "name": "test",
                        }
                    ]
                }
        """
        meta = dict(total_count=self.count(),
                    limit=limit,
                    offset=offset)
        objects = [o.to_dict() for o in self[offset:offset + limit]]
        return dict(meta=meta, objects=objects)

    def get_or_api_404(self, **kwargs) -> 'BaseModel':
        """使用get()方法获取实例,找不到资源抛出APIError

        Raises:
            APIError: code=10004

        Returns:
            instance: 找到资源后返回模型实例
        """
        try:
            obj = self.get(**kwargs)
        except:
            raise APIError(10004)
        else:
            return obj

    def delete(self):
        """软删除
        """
        return self.update(is_active=False)

    def true_delete(self):
        """硬删除
        """
        return super(MyQuerySet, self).delete()


class MyManager(models.Manager):

    def get_queryset(self) -> MyQuerySet:
        return MyQuerySet(self.model, using=self._db)

    def get_or_api_404(self, **kwargs) -> 'BaseModel':
        return self.get_queryset().get_or_api_404(**kwargs)

    def active(self, *args, **filters) -> MyQuerySet:
        filters.update(is_active=True)
        return self.get_queryset().filter(*args, **filters)


class BaseModel(Model):
    objects = MyManager()

    fields_map = {}

    created = models.DateTimeField("创建时间", auto_now_add=True)
    last_modified = models.DateTimeField("最后修改时间", auto_now_add=True)
    # acl = JSONField(default=get_acl('row', level='sys'))
    acl = JSONField(default=row_acl)
    is_active = models.BooleanField("删除标记", default=True)
    uuid = models.UUIDField(default=uuid.uuid4)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.id} - {self.name}"

    @classmethod
    def _get_fields(cls):
        if cls.fields_map:
            return cls.fields_map

        FOREIGNKEY_LIKE_KEY = ['ForeignKey', 'TreeForeignKey', 'OneToOneField', ]
        MANYTOMANY = ["ManyToManyField"]

        _fields = cls._meta.get_fields()
        # default_related_name = cls._meta.default_related_name or '_set'
        _field_map = {}

        for field in _fields:
            name = field.name
            cls_name = field.__class__.__name__
            if cls_name in FOREIGNKEY_LIKE_KEY:
                _field_map[name] = dict(field=field, cls_name=cls_name)
                _field_map[field.column] = dict(field=field)
            elif cls_name.endswith('Rel'):
                _field_map[f'{name}_set'] = dict(field=field, cls_name=cls_name)
            else:
                _field_map[name] = dict(cls_name=cls_name, field=field)
                if cls_name.endswith('Field') and field.choices:
                    _field_map[name].update({f'{name}_choices': field.choices})
        cls.fields_map = _field_map
        return _field_map

    def _to_dict(self):

        FOREIGNKEY_LIKE_KEY = ['ForeignKey', 'TreeForeignKey', 'OneToOneField', ]
        MANYTOMANY = ["ManyToManyField"]

        data = {}
        field_map = self._get_fields()

        for field_name, field_config in field_map.items():
            cls_name = field_config.get('cls_name', '')
            if cls_name in FOREIGNKEY_LIKE_KEY:
                attr = getattr(self, field_name)
                value = attr.to_dict() if attr else None
            elif cls_name.endswith('Rel'):
                value = ''
            elif cls_name in MANYTOMANY:
                attr = getattr(self, field_name)
                value = [i.to_dict() for i in attr.all()] if attr else []
            else:
                value = self.__dict__.get(field_name)
            if field_name != 'acl':
                data[field_name] = value
        return data

    def to_dict(self):
        return self._to_dict()

    @staticmethod
    def pagination(query_set, limit=20, offset=0):
        meta = dict(total_count=query_set.count(),
                    limit=limit,
                    offset=offset)
        objects = [o.to_dict() for o in query_set[offset:limit]]
        return dict(meta=meta, objects=objects)

    @transaction.atomic
    def update_fields(self, **kwargs):
        _field_map = self._get_fields()
        field_data = {}
        _foreignkey_data = {}
        _manytomany_data = {}
        _no_field = {}
        for field, value in kwargs.items():
            field_info = _field_map.get(field)
            cls_name = field_info.get('cls_name') if field_info else ''
            if field_info and cls_name == 'ForeignKey':
                _foreignkey_data[field] = value or None
            elif field_info and cls_name == 'ManyToManyField':
                _manytomany_data[field] = value or []
            elif field_info:
                field_data[field] = value
            else:
                _no_field[field] = value
        foreignkey_data = self._get_foreignKey(**_foreignkey_data)
        manytomany_data = self._get_manyToMany(**_manytomany_data)
        self.__update(**field_data, **foreignkey_data, **manytomany_data)
        return self

    def _get_foreignKey(self, **kwargs):
        _data = {}
        _field_map = self._get_fields()
        for field, value in kwargs.items():
            model = _field_map.get(field).get('field').related_model
            if is_uuid(value):
                _data[field] = model.objects.get(uuid=value)
            else:
                _data[field] = model.objects.get(id=value)
        return _data

    def _get_manyToMany(self, **kwargs):
        _data = {}
        _field_map = self._get_fields()
        for field, values in kwargs.items():
            model = _field_map.get(field).get('field').related_model
            if values:
                if is_uuid(values[0]):
                    _data[field] = model.objects.filter(uuid__in=values)
                else:
                    _data[field] = model.objects.filter(id__in=values)
            else:
                return {}
        return _data

    def __update(self, **data):
        _field_map = self._get_fields()
        for field, value in data.items():
            if _field_map.get(field).get('cls_name') == "ManyToManyField":
                attr = getattr(self, field)
                attr.set(value)
            else:
                setattr(self, field, value)
        self.save_to_now()
        return self

    @classmethod
    def create(cls, **data):
        _field_map = cls._get_fields()
        data_to_create = {}
        foreign_key_data = {}
        many_to_many_data = {}
        for field, value in data.items():
            field_meta = _field_map.get(field)
            cls_name = field_meta.get('cls_name') if field_meta else None
            if field_meta is None:
                pass
            elif cls_name == "ForeignKey":
                model = field_meta.get('field').related_model
                if isinstance(value, int):
                    data_to_create[field] = model.objects.get_or_api_404(id=value)
                elif isinstance(value, model):
                    data_to_create[field] = value
            elif cls_name == "ManyToManyField":
                if isinstance(value, list):
                    model = field_meta.get('field').related_model
                    many_to_many_data[field] = model.objects.filter(id__in=value)
            elif cls_name.endswith('Field'):
                data_to_create[field] = value
        obj = cls(**data_to_create)
        obj.save_to_now()
        if many_to_many_data:
            for field, value in many_to_many_data.items():
                attr = getattr(obj, field)
                attr.set(value)
        return obj

    def save_to_now(self):
        """保存时修改最后修改时间为当前时间
        """
        self.last_modified = datetime.datetime.now()
        self.save()

    def delete(self):
        """软删除,将is_active字段设置为False
        """
        self.is_active = False
        self.save()

    def ture_delete(self):
        """真实从数据库中删除
        """
        super(BaseModel, self).delete()
