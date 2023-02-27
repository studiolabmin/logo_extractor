from django.urls import re_path,path,include
from logoapp.views import get_images,download_images

urlpatterns = [
    path('save/', get_images, name='get_images'),
    path('download/', download_images, name='download_images'),
]