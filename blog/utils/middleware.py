import os

from django.utils.deprecation import MiddlewareMixin

from utils.api_response import APIError, APIResponseError


class APIMiddleware(MiddlewareMixin):

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        response['X-Instance-ID'] = os.environ.get('HOSTNAME', 'none')
        response['X-Instance-Version'] = os.environ.get('VERSION', 'none')
        response['X-Relase-Datetime'] = os.environ.get('RELASE_DATETIME', 'none')

        # Code to be executed for each request/response after
        # the view is called.

        return response

    def process_exception(self, request, exception):
        """处理错误 """
        if isinstance(exception, APIError):
            return APIResponseError(exception.code)
