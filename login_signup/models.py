from django.db import models
from django.contrib.auth.models import User
import time
import os
from django.contrib.auth.models import User
from notification_and_mails.models import *
User._meta.get_field('email')._unique = True
User._meta.get_field('email').blank = False
User._meta.get_field('email').null = False

def get_timestamp():
    return time.time()


class AppUser(models.Model):
    class Meta:
        verbose_name_plural = "   Profile Details"

    def get_upload_path_display_picture(instance, filename):
        return os.path.join("user_%s" % str(User.objects.filter(username=instance.user_id)[0].id), "display_picture",
                            filename)

    def get_upload_path_cover_photo(instance, filename):
        return os.path.join("user_%s" % str(User.objects.filter(username=instance.user_id)[0].id), "cover_photo",
                            filename)

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ('N', None),
    )

    user_id = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=50, null=False, unique=True)
    mobile_no = models.CharField(null=False, max_length=25, unique=True)
    display_picture = models.ImageField(null=True, upload_to=get_upload_path_display_picture,
                                        default="defaults/display_picture.jpg")
    cover_picture = models.ImageField(null=True, upload_to=get_upload_path_cover_photo,
                                      default="defaults/cover_picture.jpg")
    location = models.CharField(null=True, max_length=70, default=None)
    city = models.CharField(null=True, max_length=25, default=None)
    state = models.CharField(null=True, max_length=25, default=None)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default=None, null=True)
    age = models.IntegerField(null=True, default=None)
    date_of_birth = models.DateField(null=True)
    about = models.CharField(null=True, max_length=140, default=None)
    user_link = models.CharField(default=None, null=True, max_length=100)
    twitter_handle = models.CharField(default=None, null=True, max_length=50)
    address = models.CharField(null=True, max_length=250, default=None)
    otp_time = models.FloatField(default=get_timestamp)
    is_profile_completed = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=True)
    hash_key = models.CharField(max_length=200, null=True, default=None)
    website = models.CharField(max_length=50, null=True, default=None)
    ref_code = models.CharField(max_length=100, null=True, default=None)

    def __str__(self):
        return str(self.user_id)


class UserCrossFollower(models.Model):
    class Meta:
        verbose_name_plural = "  Follow Panel"
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name="followed_user_id")
    followed_by = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name="followed_by")
    followed_at = models.DateTimeField(auto_now_add=True)
    notification_id = models.ForeignKey(NotificationHistory, on_delete=models.DO_NOTHING, null=True, default=None)

    def __str__(self):
        return str(self.user_id)


class UserXBlockedUser(models.Model):
    class Meta:
        verbose_name_plural = "Block Panel"
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name="blocked_user_id")
    blocked_by = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name="blocked_by")
    blocked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user_id)


class BlackListedAccessTokens(models.Model):
    token = models.CharField(max_length=250)
    blacklisted_at = models.FloatField(default=get_timestamp)

    def __str__(self):
        return self.token


class DeviceInfo(models.Model):
    LANGUAGE_CHOICES = (
        ('1', 'ENGLISH'),
    )
    DEVICE_CHOICES = (
        ('A', 'Android'),
        ('I', 'IOS'),
        ('W', 'WebApp'),
    )
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    lang = models.CharField(max_length=1, choices=LANGUAGE_CHOICES)
    device_id = models.CharField(max_length=50, null=False)
    device_info = models.CharField(max_length=250, null=False)
    app_info = models.CharField(max_length=20, null=False)
    device_token = models.CharField(max_length=250, null=False)
    device_type = models.CharField(max_length=1, choices=DEVICE_CHOICES)
    authorization_token = models.CharField(max_length=250, null=False)
    user_token = models.CharField(max_length=50, null=False)


class Social_Login(models.Model):
    # class Meta:
    # verbose_name_plural = "Social_Login"
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    facebook=models.BooleanField (null=True, default=False)
    facebook_id=models.CharField(max_length=255, null=True)
    google = models.BooleanField(null=True, default=False)
    google_id = models.CharField(max_length=255, null=True)
