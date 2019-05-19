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
            cat = Category.objects.get_or_api_404(id=kwargs.get('cat_id'))
            return APIResponse(cat.to_dict())
        else:
            cats = Category.objects.all().pagination()
            return APIResponse(cats)


@method_decorator(csrf_exempt, name='dispatch')
class TagView(View):

    def get(self, r, *args, **kwargs):
        if kwargs.get('tag_id'):
            tag = Post.objects.get_or_api_404(id=kwargs.get('tag_id'))
            return APIResponse(tags.to_dict())
        else:
            tags = Tag.objects.all().pagination()
            return APIResponse(tags)


@method_decorator(csrf_exempt, name='dispatch')
class PostView(View):

    def get(self, r, *args, **kwargs):
        if kwargs.get('post_id'):
            post = Post.objects.get_or_api_404(id=kwargs.get('post_id'))
            return APIResponse(post.to_dict())
        else:
            posts = Post.objects.all().pagination()
            return APIResponse(posts)

    @method_decorator(token_required, name='dispatch')
    def post(self, r, *args, **kwargs):
        data = json.loads(r.body)
        # tags = data.pop('tags') if 'tags' in data.keys() else []
        if kwargs.get('post_id'):
            post = Post.objects.get_or_api_404(id=kwargs.get('post_id')).update_fields(**data)
        else:
            post = Post.objects.create(**data, author=r.user)
        return APIResponse(post.to_dict())


def index(r):
    return render(r, 'index.html')
    return APIResponse(dict(name='hello world'))
