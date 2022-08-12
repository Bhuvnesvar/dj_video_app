from django.db import models
from django.contrib.auth.models import User


class StarManagement(models.Model):
    class Meta:
        verbose_name_plural = "  Star Management"
    key = models.CharField(max_length=50, null=False)
    value = models.IntegerField(null=False)

    def __str__(self):
        return self.key


class Stars(models.Model):
    class Meta:
        verbose_name_plural = "   Stars"
    user_id = models.OneToOneField(User, on_delete=models.DO_NOTHING, null=False)
    # eligible = models.BooleanField(null=False, default=True)
    approved = models.BooleanField(null=False, default=False)
    approval_time = models.DateTimeField(null=True, default=None)


class ChannelList(models.Model):
    class Meta:
        verbose_name_plural = "Channel List"
    channel_name = models.CharField(null=False, max_length=50)
    channel_description = models.CharField(null=False, max_length=140)

    def __str__(self):
        return self.channel_name


class ChannelXUser(models.Model):
    class Meta:
        verbose_name_plural = " Channel Users"
    channel_id = models.ForeignKey(ChannelList, on_delete=models.CASCADE, null=True)
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    approved = models.BooleanField(null=False, default=False)
    approval_time = models.DateTimeField(null=True, default=None)
