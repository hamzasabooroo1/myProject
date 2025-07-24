from django.db import models
import uuid

# Create your models here.
class Media(models.Model):
    
    media_type_choices= [
        ('image', 'Image'),
        ('video', 'Video'),
        ('audio', 'Audio'),
        ('document', 'Document'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file=models .FileField(upload_to="media/media_app")
    media_type = models.CharField(max_length=10, choices=media_type_choices)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    
    def __str__(self):
        return self.title
    
class MediaDescription(models.Model):
    
    media = models.ForeignKey(Media, on_delete=models.CASCADE, related_name='descriptions')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    language = models.CharField(max_length=10, default='en')
    description = models.TextField()
    caption = models.CharField(max_length=255, blank=True)
    tags = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    

    

    
