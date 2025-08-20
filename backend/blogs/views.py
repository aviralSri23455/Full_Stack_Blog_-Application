from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from .models import Blog
from .serializers import BlogSerializer, BlogListSerializer
from .mongodb_service import mongodb_service


class BlogPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def blog_list_create(request):
    if request.method == 'GET':
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))
        
        # Get blogs from MongoDB
        result = mongodb_service.get_all_blogs(page, page_size)
        print(f"MongoDB returned {len(result['blogs'])} blogs out of {result['total']} total")
        
        return Response({
            'count': result['total'],
            'next': f"/api/blogs/?page={page + 1}&page_size={page_size}" if page < result['total_pages'] else None,
            'previous': f"/api/blogs/?page={page - 1}&page_size={page_size}" if page > 1 else None,
            'results': result['blogs']
        })
    
    elif request.method == 'POST':
        serializer = BlogSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            blog = serializer.save()
            
            image_url = blog.image.url if blog.image else ''

            # Save to MongoDB
            blog_data = {
                'id': blog.id,
                'title': blog.title,
                'content': blog.content,
                'image': image_url,
                'author_id': blog.author.id,
                'author_email': blog.author.email,
                'author_username': blog.author.username,
                'created_at': blog.created_at.isoformat(),
                'updated_at': blog.updated_at.isoformat(),
                'is_published': blog.is_published
            }
            print(f"Saving blog to MongoDB: {blog.title} (ID: {blog.id})")
            mongodb_service.save_blog(blog_data)
            print(f"Blog saved to MongoDB successfully")
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def blog_detail(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    
    if request.method == 'GET':
        serializer = BlogSerializer(blog)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        if blog.author != request.user:
            return Response({'error': 'You can only edit your own blogs'}, 
                          status=status.HTTP_403_FORBIDDEN)
        serializer = BlogSerializer(blog, data=request.data, context={'request': request})
        if serializer.is_valid():
            blog = serializer.save()
            
            # Update in MongoDB
            blog_data = {
                'id': blog.id,
                'title': blog.title,
                'content': blog.content,
                'image': blog.image or '',
                'author_id': blog.author.id,
                'author_email': blog.author.email,
                'author_username': blog.author.username,
                'created_at': blog.created_at.isoformat(),
                'updated_at': blog.updated_at.isoformat(),
                'is_published': blog.is_published
            }
            mongodb_service.save_blog(blog_data)
            
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        if blog.author != request.user:
            return Response({'error': 'You can only delete your own blogs'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        # Delete from MongoDB
        mongodb_service.delete_blog(blog.id)
        
        blog.delete()
        return Response({'message': 'Blog deleted successfully'}, 
                       status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_blogs(request):
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 10))
    
    # Get user's blogs from MongoDB
    result = mongodb_service.get_user_blogs(request.user.id, page, page_size)
    
    return Response({
        'count': result['total'],
        'next': f"/api/blogs/my-blogs/?page={page + 1}&page_size={page_size}" if page < result['total_pages'] else None,
        'previous': f"/api/blogs/my-blogs/?page={page - 1}&page_size={page_size}" if page > 1 else None,
        'results': result['blogs']
    })


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def toggle_blog_publish(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    
    if blog.author != request.user:
        return Response({'error': 'You can only toggle publication status of your own blogs'}, 
                      status=status.HTTP_403_FORBIDDEN)
    
    # Toggle the publication status
    blog.is_published = not blog.is_published
    blog.save()
    
    # Update in MongoDB
    blog_data = {
        'id': blog.id,
        'title': blog.title,
        'content': blog.content,
        'image': blog.image.url if blog.image else '',
        'author_id': blog.author.id,
        'author_email': blog.author.email,
        'author_username': blog.author.username,
        'created_at': blog.created_at.isoformat(),
        'updated_at': blog.updated_at.isoformat(),
        'is_published': blog.is_published
    }
    mongodb_service.save_blog(blog_data)
    
    return Response({
        'message': f'Blog {"published" if blog.is_published else "unpublished"} successfully',
        'is_published': blog.is_published
    })
