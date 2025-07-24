from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import *
from .serializers import *
from django.shortcuts import get_object_or_404
  

# Create your views here.


class MediaList(APIView):
    
    permission_classes=[permissions.IsAuthenticated]
    
    def get(self, request):
        objects=Media.objects.all()
        serializer=MediaSerializer(objects, many=True)
        if not objects:
            return Response ({'message': 'no object to display'})
        return Response(serializer.data)
    
    def post(self , request):
        
        serializer=MediaSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors ,status=status.HTTP_400_BAD_REQUEST)
    
class MediaDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request, id):
        
        obj=Media.objects.get(pk=id)
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
