from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import *
from .serializers import *
from django.shortcuts import get_object_or_404
import mimetypes
  

# Create your views here.

def extract_file_metadata(file):
   
   filename = os.path.basename(file.name)
   title = os.path.splitext(filename)[0]
   extension = os.path.splitext(filename)[1].lower()
   file_size = file.size  # in bytes
   mime_type, _ = mimetypes.guess_type(filename)
   media_type = get_media_type_from_mime(mime_type)

   return {
      'title': title,
      'extension': extension,
      'size': file_size,
      'media_type': media_type
   }
   
def get_media_type_from_mime(mime_type):
   """Classify media type from MIME type."""
   if not mime_type:
      return 'unknown'
   if mime_type.startswith('image/'):
      return 'image'
   if mime_type.startswith('video/'):
      return 'video'
   if mime_type.startswith('audio/'):
      return 'audio'
   if mime_type in [
      'application/pdf',
      'application/msword',
      
   ]:
      return 'document'
   return 'unknown'
class MediaList(APIView):
    
    permission_classes=[permissions.IsAuthenticated] 
    
    
    def post(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({'error': 'No file uploaded.'}, status=status.HTTP_400_BAD_REQUEST)

        metadata = extract_file_metadata(file)
        if metadata['media_type'] == 'unknown':
            return Response({'error': f'Unsupported file type: {metadata["extension"]}'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Create media object
        media = Media.objects.create(
            file=file,
            title=metadata['title'],
            media_extension=metadata['extension'],
            media_size=metadata['size'],
            media_type=metadata['media_type']
        )

        return Response(MediaSerializer(media).data, status=status.HTTP_201_CREATED)
          
    
    def get(self, request):
        objects=Media.objects.all()
        serializer=MediaSerializer(objects, many=True)
        if not objects:
            return Response ({'message': 'no object to display'})
        return Response(serializer.data)
   
   #  def post(self , request):
        
   #      serializer=MediaSerializer(data=request.data)
        
   #      if serializer.is_valid():
   #          serializer.save()
   #          return Response(serializer.data, status=status.HTTP_201_CREATED)
   #      return Response(serializer.errors ,status=status.HTTP_400_BAD_REQUEST)
    
class MediaDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request, id):
        
        obj=get_object_or_404(Media,pk=id)
        serializer=MediaSerializer(obj)
        
        if not obj:
            return Response({'message': f'{obj} not found'},status=200)
        
        return Response(serializer.data)
    
    def patch(self, request, id):
        obj = get_object_or_404(Media, pk=id)
        data=request.data
        serializer=MediaSerializer(obj, data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request,id):
        obj = get_object_or_404(Media, pk=id)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MediaDescriptionList(APIView):
    permission_classes = [permissions.IsAuthenticated]
        
    def get(self, request):
        descriptions = MediaDescription.objects.all()
        serializer = MediaDescriptionSerializer(descriptions, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MediaDescriptionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
class MediaDescriptionDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        description = get_object_or_404(MediaDescription, pk=pk)
        serializer = MediaDescriptionSerializer(description)
        return Response(serializer.data)

    def put(self, request, pk):
        description = get_object_or_404(MediaDescription, pk=pk)
        serializer = MediaDescriptionSerializer(description, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        description = get_object_or_404(MediaDescription, pk=pk)
        description.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
