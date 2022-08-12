from .models import *


def get_self_report_count(user_obj):
    return len(UserReportHistory.objects.filter(reported_user=user_obj))


def get_video_report_count(user_obj):
    return len(PostReportHistory.objects.filter(post__user_id=user_obj))
