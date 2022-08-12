from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('get_transaction_history/', views.get_transaction_history_view),
    path('get_audio_categories/', views.get_categories_view),
    path('get_category_audios/<cat_id>/', views.get_category_audios_view),
    path('get_all_gifts/', views.get_all_gifts_view),
    path('send_gift/', views.send_gift_view),
    path('points_view/', views.points_view),
    path('last_day_notification_cron/', views.last_day_notification_cron),
    path('get_stickers/', views.get_stickers_view),
    path('add_mlmcoin/', views.add_mlmcoin),
]
