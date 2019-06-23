from django.urls import path


from . import views

urlpatterns = [
    path('article/<int:post_id>/', views.PostView.as_view()),
    path('article/', views.PostView.as_view()),
    path('tag/', views.TagView.as_view()),
    path('cat/', views.CategoryView.as_view()),
    path('', views.index),
    path('action/<str:action_name>/', views.action)
]
