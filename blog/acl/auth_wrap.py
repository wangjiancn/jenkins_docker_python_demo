import re

from django.conf import settings
from functools import wraps
from utils.api_response import APIResponseError
from acl.models import UserProfile
import jwt


def token_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        authorization = request.headers.get('authorization')
        if not authorization:
            return APIResponseError(10001)
        try:
            authorization = re.sub('Bearer\s', '', authorization)
            request_jwt = jwt.decode(authorization, settings.SECRET_KEY, True)
        except jwt.ExpiredSignatureError:
            return APIResponseError(10007)
        except jwt.DecodeError:
            return APIResponseError(10006)
        else:
            request.user = UserProfile.objects.get(username=request_jwt.get('data', {}).get('username'))
            return view_func(request, *args, **kwargs)
    return _wrapped_view
