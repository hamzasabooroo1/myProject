 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, authentication, permissions, viewsets
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import render



def homepage(request):   
   return render(request,'login.html')


def user_logout(request):
   return render(request, 'logout.html')
   
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # token, created = Token.objects.get_or_create(user=user)
            tokens=get_tokens_for_user(user)
            return Response({
                'message': 'User registered successfully',
                'tokens': tokens, 
                'user info': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=400)


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response({'error': 'Username and password required'}, status=400) 

        user = authenticate(username=username, password=password)
        if not user:
            return Response({'error': 'Invalid credentials'}, status=400)
        
        obj=User.objects.get(username=username)
        serializer=RegisterSerializer(obj)
        

        # token, created = Token.objects.get_or_create(user=user)
        tokens=get_tokens_for_user(user)
        return Response({'tokens': tokens,
                          'user info': serializer.data
                          })


class LogoutView(APIView):
    permission_classes = [IsAuthenticated] #checks for user's authorization, if the user's logged in through the user's login token

    def post(self, request):
        try:
            
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()  # Adds to blacklist table
            return Response({'message': 'Logout successful, token blacklisted.'}, status=200)
        except Exception as e:
            return Response({'error': 'Invalid or missing refresh token'}, status=400)
        # request.user.auth_token.delete()
        # return Response({'message': 'Logged out successfully.'}, status=200)


class ProfileView(APIView): 
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'username': user.username,
            'email': user.email 
        })  
    
    
# class login_app_ViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = RegisterSerializer


# class UserProfileView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         userprofile = UserProfile.objects.get(user=request.user)
#         if not userprofile:
#             return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
#         serializer = UserProfileSerealizer(userprofile)
#         return Response(serializer.data)
    
#     def post(self, request):
#         user = request.user
#         serializer = UserProfileSerealizer(user, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response({'message ': 'something went wrong'},serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            userprofile = UserProfile.objects.get(user=request.user)
            
        except UserProfile.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=404)

        serializer = UserProfileSerealizer(userprofile)
        return Response( serializer.data)

    def post(self, request):
        try:
            profile = UserProfile.objects.get(user=request.user)
            
            serializer = UserProfileSerealizer(profile, data=request.data, context={'request': request})
        except UserProfile.DoesNotExist:
            serializer = UserProfileSerealizer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Profile saved successfully!', 'data': serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)