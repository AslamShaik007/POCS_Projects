from django.urls import path
from .views import generate_subtitles

urlpatterns = [
    path('', generate_subtitles, name='video_file')
]