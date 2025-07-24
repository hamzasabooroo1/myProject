from rest_framework import serializers
from .models import *
import os


class MediaDescriptionSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model=MediaDescription
        fields='__all__'
        
class MediaSerializer(serializers.ModelSerializer):
    descriptions=MediaDescriptionSerializer(many=True, read_only=True)
    
    class Meta:
        model=Media
        fields='__all__'
        read_only_fields = ['media_type', 'media_extension', 'media_size', 'title', 'uploaded_at']