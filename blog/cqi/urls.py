from django.urls import include, path

from .views import QueryView

urlpatterns = [
    path('<slug:model_name>/', QueryView.as_view()),
    path('<slug:model_name>/<int:id>/', QueryView.as_view())
]
