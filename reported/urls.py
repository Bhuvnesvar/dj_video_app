from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('reportuser/', views.report_user_view),
    path('reportvideo/', views.report_video_view),
    path('reporttype/', views.video_report_type_view),
]
