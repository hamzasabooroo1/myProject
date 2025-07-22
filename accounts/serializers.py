          
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError


class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    email=serializers.EmailField( required=False, allow_blank=True)
    

    class Meta:
        model = User
        fields = ['username', 'email',   'password1', 'password2']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already registered.")
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already taken.")
        return value

    def validate(self, data):
        if data.get('password1') != data.get('password2'):
            raise serializers.ValidationError("Passwords do not match.")

        # Validate password strength
        try:
            validate_password(data.get('password1'))
        except DjangoValidationError as e:
            print(e)
            raise serializers.ValidationError({'password1': list(e.messages)})

        return data

    def create(self, validated_data):
        user = User(
            username=validated_data.get('username'),
            email=validated_data.get('email'),
        )
        user.set_password(validated_data['password1'])
        user.save()
        return user
 
class UserProfileSerealizer(serializers.ModelSerializer):
    
    user=RegisterSerializer(read_only=True)
    
    class Meta:
        model=UserProfile
        # fields= ['profile_pic','adress', 'contact' , 'user']
        fields='__all__'
        
        
    def create(self, validated_data):
        user = self.context['request'].user
        profile, created = UserProfile.objects.get_or_create(user=user)
        for attr, value in validated_data.items():
            setattr(profile, attr, value)
        profile.save()
        return profile