from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class UserProfile(models.Model): 
    profile_pic = models.ImageField(upload_to='profile_pics/')
    user = models.OneToOneField( User, on_delete=models.CASCADE)
    adress=models.CharField(max_length=100)
    contact=models.CharField(max_length=100)
    
    def __str__(self):
        return self.user.username
    
    