from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
path('gender_ratio_chart/', views.gender_ratio_chart, name='gender_ratio_chart'),
path('following-chart/', views.following_chart, name='following-chart'),
path('blocking-chart/', views.blocking_chart, name='blocking-chart'),
path('reported_user-chart/', views.reported_user_chart, name='reported_user-chart'),
path('reported_video-chart/', views.reported_video_chart, name='reported_video-chart'),
path('report_type-chart/', views.report_type_chart, name='report_type-chart'),
path('most_allotted_category_chart/', views.most_allotted_category_chart, name='most_allotted_category_chart'),
path('Audio_uses_chart/', views.Audio_uses_chart, name='Audio_uses_chart'),
path('Audio_Catogory_uses_chart/', views.Audio_Catogory_uses_chart, name='Audio_Catogory_uses_chart'),
path('Filter_uses_chart/', views.Filter_uses_chart, name='Filter_uses_chart'),
path('Effect_uses_chart/', views.Effect_uses_chart, name='Effect_uses_chart'),
path('Most_liked_chart/', views.Most_liked_chart, name='Most_liked_chart'),
path('Most_viewed_chart/', views.Most_viewed_chart, name='Most_viewed_chart'),
path('joining-chart/', views.joining_chart, name='joining-chart'),
path('total_user/', views.total_user, name='total_user'),
path('active_user/', views.active_user, name='active_user'),
]
