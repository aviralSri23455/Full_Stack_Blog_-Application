from django.http import HttpResponse, Http404
from django.conf import settings
from django.views.decorators.http import require_GET
import os
import mimetypes

@require_GET
def serve_media(request, path):
    """
    Serve media files in production.
    This is a simple implementation for Railway deployment.
    """
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    
    if not os.path.exists(file_path):
        raise Http404("Media file not found")
    
    # Get the MIME type
    content_type, _ = mimetypes.guess_type(file_path)
    if content_type is None:
        content_type = 'application/octet-stream'
    
    # Read and serve the file
    with open(file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type=content_type)
        response['Content-Length'] = os.path.getsize(file_path)
        return response
