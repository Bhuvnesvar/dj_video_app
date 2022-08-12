from django.db import models
from video.models import *
from django.contrib.auth.models import User

class ReportTypes(models.Model):
    class Meta:
        verbose_name_plural = "     Report Types"
    FOR_CHOICES = (
        ('U', 'User'),
        ('P', 'Post'),
    )
    name = models.CharField(null=False, max_length=30)
    description = models.CharField(null=False, max_length=140)
    for_what = models.CharField(max_length=1, choices=FOR_CHOICES)
    max_reports = models.IntegerField(null=False)

    def __str__(self):
        return self.name


class PostReportHistory(models.Model):
    class Meta:
        verbose_name_plural = "  Post Report History"
    post = models.ForeignKey(MediaTable, on_delete=models.DO_NOTHING)
    reported_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    report_type = models.ForeignKey(ReportTypes, on_delete=models.CASCADE)
    reporting_time = models.DateTimeField(auto_now_add=True)


class UserReportHistory(models.Model):
    class Meta:
        verbose_name_plural = "   User Report History"
    reported_user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='reported_user')
    reported_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='reported_by')
    report_type = models.ForeignKey(ReportTypes, on_delete=models.CASCADE)
    reporting_time = models.DateTimeField(auto_now_add=True)
