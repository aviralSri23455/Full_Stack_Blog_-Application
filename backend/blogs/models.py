from django.db import models
from accounts.models import CustomUser
from django.core.exceptions import ValidationError
from django.conf import settings
import os


def validate_image(image):
    """Validate image file size and format"""
    if image:
        # Check file size (10MB limit)
        if image.size > getattr(settings, 'MAX_IMAGE_SIZE', 10 * 1024 * 1024):
            raise ValidationError('Image file too large ( > 10MB )')
        
        # Check file extension
        ext = os.path.splitext(image.name)[1].lower()
        allowed_extensions = getattr(settings, 'ALLOWED_IMAGE_EXTENSIONS', ['.jpg', '.jpeg', '.png', '.gif'])
        if ext not in allowed_extensions:
            raise ValidationError(f'Unsupported file extension. Allowed: {", ".join(allowed_extensions)}')


class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(
        upload_to='blog_images/', 
        blank=True, 
        null=True, 
        help_text="Featured image for the blog post (Max: 10MB, Formats: JPG, PNG, GIF)",
        validators=[validate_image]
    )
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='blogs')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
