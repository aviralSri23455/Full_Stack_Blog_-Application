from django.contrib import admin
from django.urls import path, include, re_path
from django.http import JsonResponse
from django.conf import settings
from django.conf.urls.static import static
from .media_views import serve_media

def api_root(request):
    return JsonResponse({
        'message': 'Welcome to Blog API',
        'endpoints': {
            'auth': '/api/auth/',
            'blogs': '/api/blogs/',
            'admin': '/admin/'
        }
    })

def health_check(request):
    return JsonResponse({'status': 'healthy', 'service': 'blog-backend'})

urlpatterns = [
    path('', api_root, name='api-root'),
    path('api/health/', health_check, name='health-check'),
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/blogs/', include('blogs.urls')),
    # Custom media file serving for production
    re_path(r'^media/(?P<path>.*)$', serve_media, name='media'),
]

# Serve static files
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
