from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status


@api_view(['POST'])
@permission_classes([AllowAny])
def publish_all_blogs(request):
    """Temporary endpoint to publish all blogs - remove after use"""
    try:
        from blogs.mongodb_service import mongodb_service
        if mongodb_service.db:
            result = mongodb_service.blogs_collection.update_many(
                {},  # Update all blogs
                {"$set": {"is_published": True}}
            )
            return Response({'message': f'Successfully updated {result.modified_count} blogs to published status'})
        else:
            return Response({'error': 'MongoDB connection not available'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
