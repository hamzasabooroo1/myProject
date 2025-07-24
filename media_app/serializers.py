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
        depth=1
        
    def validate(self, data):#validation for file extension and mediatype matching
        file=data.get('file')
        media_type=data.get('media_type')
        
        if not file or not media_type:
            return data
        
        ext=os.path.splitext(file.name)[1].lower()
        
        type_map = {
            'image': ['.jpg', '.jpeg', '.png'],
            'video': ['.mp4'],
            'audio': ['.mp3'],
            'document': ['.pdf']
        }
        
        expected_extension=type_map.get(media_type)
        if  expected_extension and ext not in expected_extension:
            raise serializers.ValidationError({
                'file':f'file extension "{ext}" doesnot match the media type "{media_type}"'
            })
            
        
        return data