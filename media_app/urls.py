from .views import *
from django.urls import path 




urlpatterns = [
    path('media-list-view/' ,MediaList.as_view()),
    path('media-detail-view/<str:id>' , MediaDetailView.as_view()),
    path('media_description-list-view/',MediaDescriptionList.as_view()),
    path('media-description-detail-view/<str:pk>', MediaDescriptionDetailView.as_view()),
    
    
]
