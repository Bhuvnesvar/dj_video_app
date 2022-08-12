from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('get_channel_list/', views.get_channel_list_view),
    path('get_channel_videos/', views.get_channel_videos_view),
    path('get_star_videos/', views.get_star_videos_view),
    path('get_star_requirments/', views.get_star_requirments),
    path('find_star_cron/', views.find_star_cron),
]
