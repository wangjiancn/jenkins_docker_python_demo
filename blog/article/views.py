import json
import uuid
import os

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views import View
from django.shortcuts import render
from django.utils.decorators import method_decorator
from acl.auth_wrap import token_required

from .models import Post, Tag, Category
from .action import actions
from utils.api_response import APIResponse, APIResponseError
from utils.tool import is_uuid, parse_query_string

# Create your views here.


@method_decorator(csrf_exempt, name='dispatch')
class CategoryView(View):

    def get(self, r, *args, **kwargs):
        if kwargs.get('cat_id'):
            cat = Category.objects.active().get_or_api_404(id=kwargs.get('cat_id'))
            return APIResponse(cat.to_dict())
        else:
            cats = Category.objects.active().all().pagination()
            return APIResponse(cats)


@method_decorator(csrf_exempt, name='dispatch')
class TagView(View):

    def get(self, r, *args, **kwargs):
        pagination, order_by, filters, defer, search = parse_query_string(
            r.GET, 'post')
        if kwargs.get('tag_id'):
            tag = Post.objects.active().defer(*defer).get_or_api_404(id=kwargs.get('tag_id'))
            return APIResponse(tag.to_dict())
        else:
            tags = Tag.objects.active().defer(
                *defer).order_by(*order_by).pagination(**pagination)
            return APIResponse(tags)


@method_decorator(csrf_exempt, name='dispatch')
class PostView(View):

    def get(self, r, *args, **kwargs):
        pagination, order_by, filters, defer, search = parse_query_string(
            r.GET, 'post')
        if kwargs.get('post_id'):
            post = Post.objects.active().defer(*defer).get_or_api_404(id=kwargs.get('post_id'))
            post.add_view_count()
            return APIResponse(post.to_dict())
        else:
            posts = Post.objects.active(
                search, **filters).defer(*defer).order_by(*order_by).pagination(**pagination)
            return APIResponse(posts)

    @method_decorator(token_required, name='dispatch')
    def post(self, r, *args, **kwargs):
        data = json.loads(r.body)
        # tags = data.pop('tags') if 'tags' in data.keys() else []
        if kwargs.get('post_id'):
            post = Post.objects.get_or_api_404(
                id=kwargs.get('post_id')).update_fields(**data)
        else:
            post = Post.create(**data, author=r.user)
        return APIResponse(post.to_dict())

    @method_decorator(token_required, name='dispatch')
    def delete(self, r, *args, **kwargs):
        if kwargs.get('post_id'):
            Post.objects.active(id=kwargs.get('post_id')).delete()
            return APIResponse()
        else:
            return APIResponse(code=10003)


def index(r):
    return APIResponse(dict(
        name='hello world!',
        hostname=os.environ.get('HOSTNAME', 'none'),
        index=1
    ))


@require_POST
@csrf_exempt
def action(r, *args, **kwargs):
    return actions.run_action(r, *args, **kwargs)
