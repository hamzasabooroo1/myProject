from .views import *
from django.urls import path 




urlpatterns = [
    path('media-list-view/' ,MediaList.as_view()),
    path('media-detail-view/<int:id>' , MediaDetailView.as_view()),
    path('media_description-list-view/',MediaDescriptionList.as_view()),
    path('media-description-detail-view/<int:pk>', MediaDescriptionDetailView.as_view()),
    
    
]
