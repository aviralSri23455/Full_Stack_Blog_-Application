from rest_framework import serializers
from .models import Blog
from accounts.serializers import UserSerializer


class BlogSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Blog
        fields = ('id', 'title', 'content', 'image', 'image_url', 'author', 'created_at', 'updated_at', 'is_published')
        read_only_fields = ('id', 'author', 'created_at', 'updated_at')

    def get_image_url(self, obj):
        """Return the full image URL"""
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            else:
                # Fallback for when no request context is available
                base_url = 'https://fullstackblog-application-production.up.railway.app'
                return f"{base_url}{obj.image.url}"
        return None

    def validate_content(self, value):
        """Validate that content has at least 50 lines"""
        lines = [line.strip() for line in value.split('\n') if line.strip()]
        if len(lines) < 50:
            raise serializers.ValidationError(
                f"Content must have at least 50 lines. Currently has {len(lines)} lines."
            )
        return value

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class BlogListSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    content_preview = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Blog
        fields = ('id', 'title', 'content_preview', 'image', 'image_url', 'author', 'created_at', 'is_published')

    def get_content_preview(self, obj):
        return obj.content[:200] + '...' if len(obj.content) > 200 else obj.content

    def get_image_url(self, obj):
        """Return the full image URL"""
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            else:
                # Fallback for when no request context is available
                base_url = 'https://fullstackblog-application-production.up.railway.app'
                return f"{base_url}{obj.image.url}"
        return None
