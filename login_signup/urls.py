from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('login/', views.login_view),
    path('create_user', views.createUser),
    path('resend_otp', views.resendOtp),
    path('otp_verification/', views.otp_verification_view),
    path('signup_details/', views.signup_details_view),
    path('get_self_info/', views.get_self_info_view),
    path('view_user/<user_id>/', views.view_user_view),
    path('get_followers/', views.get_followers_view),
    path('follow_unfollow/', views.follow_unfollow_view),
    path('logout/', views.logout_view),
    path('profile_update/', views.profile_update_view),
    path('get_followings/', views.get_followings_view),
    path('check_username/', views.check_username_view),
    path('block_user/', views.block_user_id_view),
    path('blocklist/', views.get_blocked_user_list_view),
    path('update_user_token/', views.update_user_token_view),
    path('remove_photo/', views.remove_photo_view),
    path('search_user/', views.search_user_view),
    path('delete_user/', views.delete_user_view),
    path('social_update/', views.social_view),
    path('get_social/', views.get_social_view),
    # path('get_all_number/', views.get_all_number),
]
