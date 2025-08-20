from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.conf import settings
from django.conf.urls.static import static

def api_root(request):
    return JsonResponse({
        'message': 'Welcome to Blog API',
        'endpoints': {
            'auth': '/api/auth/',
            'blogs': '/api/blogs/',
            'admin': '/admin/'
        }
    })

urlpatterns = [
    path('', api_root, name='api-root'),
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/blogs/', include('blogs.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
