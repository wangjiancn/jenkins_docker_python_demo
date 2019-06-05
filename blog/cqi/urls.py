from django.urls import include, path

from .views import QueryView, QueryMoreView

urlpatterns = [
    path('<slug:query_model>/', QueryMoreView.as_view()),
    path('<slug:query_model>/<int:id>/', QueryView.as_view())
]
