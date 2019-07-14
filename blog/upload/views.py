import uuid
import os

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings

from utils.api_response import APIResponse, APIError, APIResponseError

# Create your views here.


def handle_upload_file(file, path):
    with open(path, 'wb') as destination:
        for chunk in file.chunks():
            destination.write(chunk)


@require_POST
@csrf_exempt
def upload_image(r):
    files = r.FILES
    image = files.get('image')
    if not image:
        return APIResponseError(12002)
    name: str = image.name
    try:
        ext = name.rsplit('.')[1]
    except IndexError:
        return APIResponseError(12001)
    file_name = uuid.uuid4().hex + '.' + ext
    path = os.path.join(settings.ENV_UPLOAD_PATH, 'images', file_name)

    url = os.path.join(settings.STATIC_URL, os.path.join('images', file_name))
    handle_upload_file(image, path)

    return APIResponse(url)
