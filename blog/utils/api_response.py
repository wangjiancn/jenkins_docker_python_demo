import json

from django.core.serializers.json import DjangoJSONEncoder
from django.http.response import HttpResponse

from .error_code import get_msg


class APIError(Exception):
    def __init__(self, code=-1):
        self.code = code


class APIResponse(HttpResponse):
    status_code = 200

    def __init__(self, data='', code=0, encoder=DjangoJSONEncoder, safe=True,
                 json_dumps_params=None, **kwargs):
        json_dumps_params = json_dumps_params or {}
        kwargs.setdefault('content_type', 'application/json')
        res = dict(code=code, msg=get_msg(code))
        if data:
            res.update(data=data)
        if safe and not isinstance(res, dict):
            raise TypeError(
                'In order to allow non-dict objects to be serialized set the '
                'safe parameter to False.'
            )
        res = json.dumps(res, cls=DjangoJSONEncoder, **json_dumps_params)
        super().__init__(content=res, **kwargs)


class APIResponseError(APIResponse):

    status_code = 200

    def __init__(self, code=1, data={}, **kwargs):
        super().__init__(data=data, code=code, **kwargs)
