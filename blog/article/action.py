from utils.api_response import APIResponse, APIResponseError, APIError
from .models import Post, Tag, Category, Comment, Like, Rate


class Actions():

    def run_action(self, r, *args, **kwargs):
        action_name = kwargs.get('action_name')
        if not action_name or not hasattr(self, action_name):
            raise APIError(11001)
        action = getattr(self, action_name)
        return action(r, *args, **kwargs)

    def publish_post(self, r, *args, **kwargs):
        return APIResponse(kwargs)


actions = Actions()
