from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views
from .temp_views import publish_all_blogs

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('reset-demo-password/', views.reset_demo_password, name='reset_demo_password'),
    path('publish-all-blogs/', publish_all_blogs, name='publish_all_blogs'),
]
