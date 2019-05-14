import json

from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate

from .models import UserProfile
from .auth_wrap import token_required
from utils.api_response import APIResponse, APIResponseError


@require_POST
@csrf_exempt
def register(r):
    """注册"""
    data = json.loads(r.body)
    user = UserProfile.objects.create_user(**data)
    return APIResponse(token=user.token)


@csrf_exempt
@require_POST
def login(r):
    """登录"""
    data = json.loads(r.body)
    user = authenticate(**data)
    if user is not None:
        return APIResponse(user.token)
    else:
        return APIResponseError(10005)


@token_required
@require_POST
@csrf_exempt
def logout(r):
    """注销"""
    return APIResponse()
