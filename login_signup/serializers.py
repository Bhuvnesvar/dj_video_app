from rest_framework import serializers
from .models import AppUser, UserCrossFollower
from django.contrib.auth.models import User


class AuthUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class AppUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = "__all__"


class UserCrossFollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCrossFollower
        fields = "__all__"
