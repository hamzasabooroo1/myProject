from .views import *
from django.urls import path 




urlpatterns = [
    path('media-list-view/' ,MediaList.as_view()),
    path('media-detail-view/<int:id>/' , MediaDetailView.as_view()),
    path('media-description-list-view/',MediaDescriptionList.as_view()),
    path('media-description-detail-view/<int:pk>', MediaDescriptionDetailView.as_view()),
    
    #accessig frontends
    
    path('media_list_view_post/', media_list_view_post, name='mlvp'),
    path('media_list_view_get/', media_list_view_get, name='mlvg'),
    path('media_desc_list_post/', media_desc_list_post, name='mdlp'),
    path('media_detail_view_get/<int:mediaId>/', media_detail_view_get, name='mdvg'),
    path('media_detail_view_patch/<int:id>/', media_detail_view_patch, name='mdvp'),
    
    
]
