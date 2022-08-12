from django.db import models
from django.contrib.auth.models import User
# from video.models import *


class NotificationEmailSettings(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False)
    n_follows_me = models.BooleanField(default=True)
    e_follows_me = models.BooleanField(default=True)
    n_like_my_activity = models.BooleanField(default=True)
    e_like_my_activity = models.BooleanField(default=True)
    n_comment_my_activity = models.BooleanField(default=True)
    e_comment_my_activity = models.BooleanField(default=True)
    n_any_other_activity = models.BooleanField(default=True)
    e_any_other_activity = models.BooleanField(default=True)
    n_occasional_updates = models.BooleanField(default=True)
    e_occasional_updates = models.BooleanField(default=True)
    n_chat_notification = models.BooleanField(default=True)


class NotificationTemplates(models.Model):
    class Meta:
        verbose_name_plural = "Notification Template"

    notification_type = models.CharField(null=False, max_length=50)
    notification_template = models.CharField(null=False, max_length=140)

    def __str__(self):
        return self.notification_type


class NotificationHistory(models.Model):
    class Meta:
        verbose_name_plural = "Notification History"

    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False)
    title = models.CharField(max_length=50, null=False)
    message = models.CharField(max_length=150, null=False)
    type_id = models.CharField(max_length=30, null=False)
    is_read = models.BooleanField(default=False)
    time = models.DateTimeField(auto_now_add=True)


class EmailTemplates(models.Model):
    class Meta:
        verbose_name_plural = "Email Templates"

    email_type = models.CharField(null=False, max_length=50)
    email_template = models.FileField(null=False, upload_to="email_templates/")

    def __str__(self):
        return self.email_type


class EmailHistory(models.Model):
    class Meta:
        verbose_name_plural = "Email History"

    email = models.ForeignKey(EmailTemplates, on_delete=models.DO_NOTHING, null=False)
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False)
    email_time = models.DateTimeField(auto_now_add=True)


class TermAndConditionAndPolicy(models.Model):
    class Meta:
        verbose_name_plural = "T&C and Privacy Policy"

    title = models.CharField(max_length=50)
    body = models.TextField()
