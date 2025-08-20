from rest_framework import serializers
from .models import Blog
from accounts.serializers import UserSerializer


class BlogSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    
    class Meta:
        model = Blog
        fields = ('id', 'title', 'content', 'image', 'author', 'created_at', 'updated_at', 'is_published')
        read_only_fields = ('id', 'author', 'created_at', 'updated_at')

    def validate_content(self, value):
        """Validate that content has at least 50 lines"""
        lines = [line.strip() for line in value.split('\n') if line.strip()]
        if len(lines) < 50:
            raise serializers.ValidationError(
                f"Content must have at least 50 lines. Currently has {len(lines)} lines."
            )
        return value

    def validate(self, attrs):
        """Validate the entire serializer data"""
        # Check if this is a create operation and image is required
        if not self.instance and not attrs.get('image'):
            raise serializers.ValidationError({
                'image': 'Image is required for blog creation.'
            })
        return attrs

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class BlogListSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    content_preview = serializers.SerializerMethodField()
    
    class Meta:
        model = Blog
        fields = ('id', 'title', 'content_preview', 'image', 'author', 'created_at', 'is_published')

    def get_content_preview(self, obj):
        return obj.content[:200] + '...' if len(obj.content) > 200 else obj.content
