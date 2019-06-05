from django.shortcuts import render
from django.apps import apps
from django.views import View
from utils.api_response import APIResponse

# Create your views here.


class QueryView(View):
    def get(self, r, *args, **kwargs):
        query_model = kwargs.get('query_model')

        pass


class QueryMoreView(View):
    def get(self, r, *args, **kwargs):
        query = r.GET.dict()
        return APIResponse(query)
