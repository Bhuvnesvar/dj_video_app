from .models import *


def get_notification_count(user_id):
    return len(NotificationHistory.objects.filter(user_id=user_id))
