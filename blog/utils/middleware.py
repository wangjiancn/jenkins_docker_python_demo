from django.utils.deprecation import MiddlewareMixin

from utils.api_response import APIError, APIResponseError


class APIExceptionHandleMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        if isinstance(exception, APIError):
            return APIResponseError(exception.code)
        # else:
        #     return request, exception
