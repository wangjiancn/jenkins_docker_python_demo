import json

from django.apps import apps
from django.db.models import Q
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from acl.auth_wrap import token_required
from utils.api_response import APIError, APIResponse, APIResponseError
from utils.base_model import BaseModel
from utils.tool import parse_query_string

# Create your views here.


model_name_map = {
    'post': 'article.post',
    'article': 'article.post',
    'tag': 'article.tag',
    'category': 'article.category',
}


@method_decorator(csrf_exempt, name="dispatch")
class QueryView(View):
    """通用Restful API接口"""

    def get_model(self, model_name: str) -> BaseModel:
        """从指定模型中获取Django模型对象,未指定抛出APIError

        Args:
            model_name (str): 已定义对象名称,参考model_name_map

        Raises:
            APIError: 会被中间件捕获返回指定错误码的错误消息

        Returns:
            Model: DJango Model对象
        """
        app_lable__model_name = model_name_map.get(model_name)
        if not app_lable__model_name:
            raise APIError(10008)
        model = apps.get_model(app_lable__model_name)
        return model

    def get(self, r, *args, **kwargs):
        """HTTP GET方法

        Args:
            r (request): request对象 

        Returns:
            JSON对象或者错误信息
        """
        model_name = kwargs.get('model_name')
        model = self.get_model(model_name)

        _id = kwargs.get('id')
        if _id:
            data = model.objects.active().get_or_api_404(id=_id).to_dict()
        else:
            query = parse_query_string(r.GET, model_name)
            data = model.objects\
                .active(query.search, **query.filters)\
                .defer(*query.defer)\
                .order_by(*query.order_by)\
                .pagination(**query.pagination)

        return APIResponse(data)

    @method_decorator(token_required, name="dispatch")
    def post(self, r, *args, **kwargs):
        """HTTP POST方法

        更新资源

        Args:
            r (request): [description]

        Returns:
            JSON
        """
        model_name = kwargs.get('model_name')
        model = self.get_model(model_name)
        data = json.loads(r.body)

        _id = kwargs.get('id')
        if _id:
            obj = model.objects.get_or_api_404(id=_id).update_fields(**data)
        else:
            obj = model.create(**data, auth=r.user)

        return APIResponse(obj.to_dict())

    @method_decorator(token_required, name="dispatch")
    def delete(self, r, *args, **kwargs):
        """HTTP DELETE方法

        Args:
            r (requests): request对象

        Raises:
            APIError: API错误

        Returns:
            JSON

        DELETE /post/1  删除 id = 1 的文章
        """
        model_name = kwargs.get('model_name')
        model = self.get_model(model_name)

        _id = kwargs.get('id')
        if _id:
            obj = model.objects.active().get_or_api_404(id=_id).delete()
        else:
            raise APIError(10009)
        return APIResponse()
