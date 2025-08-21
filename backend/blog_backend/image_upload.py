from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
import base64
import io

try:
    from PIL import Image
    import requests
    DEPENDENCIES_AVAILABLE = True
except ImportError:
    DEPENDENCIES_AVAILABLE = False

@csrf_exempt
@require_POST
def upload_to_imgbb(request):
    """
    Upload image to ImgBB (free service) to avoid Railway storage limits
    """
    if not DEPENDENCIES_AVAILABLE:
        return JsonResponse({'error': 'Image processing dependencies not available'}, status=500)
    
    try:
        if 'image' not in request.FILES:
            return JsonResponse({'error': 'No image provided'}, status=400)
        
        image_file = request.FILES['image']
        
        # Compress image to reduce size
        image = Image.open(image_file)
        
        # Resize if too large (max 800px width)
        if image.width > 800:
            ratio = 800 / image.width
            new_height = int(image.height * ratio)
            image = image.resize((800, new_height), Image.Resampling.LANCZOS)
        
        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Save to bytes
        img_buffer = io.BytesIO()
        image.save(img_buffer, format='JPEG', quality=85, optimize=True)
        img_buffer.seek(0)
        
        # Convert to base64 for ImgBB
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
        
        # Upload to ImgBB (free tier: 32MB per image, unlimited storage)
        imgbb_api_key = "c7e3fb3a1b8a08c9aa3ef9f6eb2df5f5"  # Public demo key
        
        response = requests.post(
            "https://api.imgbb.com/1/upload",
            data={
                "key": imgbb_api_key,
                "image": img_base64
            }
        )
        
        if response.status_code == 200:
            result = response.json()
            if result['success']:
                return JsonResponse({
                    'success': True,
                    'url': result['data']['url'],
                    'delete_url': result['data']['delete_url']
                })
        
        return JsonResponse({'error': 'Failed to upload image'}, status=500)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
