from django.urls import re_path,path,include
from logoapp.views import get_images,home
urlpatterns = [
    path('', home, name='home'),
    path('save/', get_images, name='get_images')
]