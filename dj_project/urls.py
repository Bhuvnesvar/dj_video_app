"""dj_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url, static
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('api/v1/admin/', admin.site.urls),
    path('api/v1/login_signup/', include("login_signup.urls")),
    path('api/v1/coins_and_gifts/', include("coins_and_gifts.urls")),
    path('api/v1/notification_and_mails/', include("notification_and_mails.urls")),
    path('api/v1/video/', include("video.urls")),
    path('api/v1/report/', include("reported.urls")),
    path('api/v1/filters/', include("effects_and_filters.urls")),
    path('api/v1/star_and_channels/', include("star_and_channels.urls")),
    path('api/v1/dashboard/', include("dashboard.urls")),
    path('api/v1/chat/', include("chat.urls")),
    ] + static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+ static.static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
