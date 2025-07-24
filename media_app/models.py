from django.db import models
import uuid

# Create your models here.
class Media(models.Model):
    


    file=models .FileField(upload_to="media_app")
    media_type = models.CharField(max_length=10, blank=True, null=True)
    media_extension = models.CharField(max_length=10, blank=True, null=True)
    media_size = models.PositiveBigIntegerField(max_length=10, blank=True, null=True)

    uploaded_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255,null=True,blank=True)
    
    def __str__(self):
        return self.title
    
class MediaDescription(models.Model):
    
    media = models.ForeignKey(Media, on_delete=models.CASCADE, related_name='descriptions')
    language = models.CharField(max_length=10, default='en')
    description = models.TextField()
    caption = models.CharField(max_length=255, blank=True)
    tags = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    

    

    
