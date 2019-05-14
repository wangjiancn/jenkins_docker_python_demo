import json
import uuid

from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.utils.decorators import method_decorator
from acl.auth_wrap import token_required
from django.shortcuts import render

from .models import Post, Tag, Category
from utils.api_response import APIResponse, APIResponseError
from utils.tool import is_uuid

# Create your views here.


@method_decorator(csrf_exempt, name='dispatch')
class CategoryView(View):

    def get(self, r, *args, **kwargs):
        if kwargs.get('cat_id'):
            cats = Category.objects.filter(id=kwargs.get(
                'cat_id'))
            if cats:
                return APIResponse(cats[0].to_dict())
            else:
                return APIResponseError(10004)
        else:
            cats = Category.objects.all()
            cat_list = Category.pagination(cats)
            # for post in posts:
            #     post_list.append(post.to_dict())
            return APIResponse(cat_list)


@method_decorator(csrf_exempt, name='dispatch')
class TagView(View):

    def get(self, r, *args, **kwargs):
        if kwargs.get('tag_id'):
            tags = Post.objects.filter(id=kwargs.get(
                'tag_id'))
            if tags:
                return APIResponse(tags[0].to_dict())
            else:
                return APIResponseError(10004)
        else:
            tags = Tag.objects.all()
            tag_list = Tag.pagination(tags)
            # for post in posts:
            #     post_list.append(post.to_dict())
            return APIResponse(tag_list)


@method_decorator(csrf_exempt, name='dispatch')
class PostView(View):

    def get(self, r, *args, **kwargs):
        if kwargs.get('post_id'):
            post = Post.objects.filter(id=kwargs.get(
                'post_id'))
            if post:
                return APIResponse(post[0].to_dict())
            else:
                return APIResponseError(10004)
        else:
            posts = Post.objects.all()
            post_list = Post.pagination(posts)
            # for post in posts:
            #     post_list.append(post.to_dict())
            return APIResponse(post_list)

    @method_decorator(token_required, name='dispatch')
    def post(self, r, *args, **kwargs):
        data = json.loads(r.body)
        tags = data.pop('tags') if 'tags' in data.keys() else []
        if kwargs.get('post_id'):
            post = Post.objects.filter(id=kwargs.get('post_id')).update(**data)
            post = Post.objects.get(id=post)
        else:
            post = Post.objects.create(**data, author=r.user)
        post.update_tag(tags)
        return APIResponse(post.to_dict())


def index(r):
    return render(r, 'index.html')
    return APIResponse(dict(name='hello world'))
