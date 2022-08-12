from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
        path('get_notifications/', views.get_notifications_view),
        path('mark_notification_as_read/', views.mark_notification_as_read_view),
        path('n_settings/', views.notification_setting_view),
        path('terms/', views.get_tnc_view),
        path('privacy_policy/', views.get_policy_view),
        path('get_notification_setting_view/', views.get_notification_setting_view),
        path('privacypolicy/', views.get_policy_render),
    ]
