
from .views import *
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

app_name = 'login_app_drf'

urlpatterns = [
   
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('profile/', ProfileView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user-profile-view/'   , UserProfileView.as_view(), name='User-profile-view'),

    path('', homepage,name='homepage'),
    path('user_logout/', user_logout, name='user-logout')
]   