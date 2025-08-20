from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_list_create, name='blog-list-create'),
    path('<int:pk>/', views.blog_detail, name='blog-detail'),
    path('my-blogs/', views.my_blogs, name='my-blogs'),
    path('<int:pk>/toggle-publish/', views.toggle_blog_publish, name='toggle-blog-publish'),
]
