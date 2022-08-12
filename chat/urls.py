from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('get_chat/', views.get_chat_view),
    path('refresh_chat/', views.refresh_chat_view),
    path('seen_view/', views.seen_view),
    path('delete_view/', views.delete_view),
    path('send_view/', views.send_view),
    path('chat_view/', views.chat_view),
    # path('trial_chat_view/', views.trial_chat_view),
]
