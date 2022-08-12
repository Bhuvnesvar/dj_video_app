from .models import *
from django.db.models import Q
from datetime import datetime, timezone


def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)


def get_chat_from_db(sender, receiver, start=None, last_id=None):
    page_size = 30
    if start is not None:
        chat = ChatTable.objects.filter(Q(message_from=sender, message_to=receiver, delete=False) | \
        Q(message_from=receiver, message_to=sender, delete=False)).order_by('-time')[start:start+page_size]
        return list(chat)
    else:
        chat = ChatTable.objects.filter(Q(message_from=sender, message_to=receiver,
                                          delete=False, id__gte=last_id) |
        Q(message_from=receiver, message_to=sender, delete=False, id__gte=last_id)).order_by(
            '-time')[0]
        return chat


def get_date_time_string_for_chat(event_time):
    now = datetime.now()
    event_time = utc_to_local(event_time)
    if now.day == event_time.day:
        return event_time.strftime("%I:%M %p")
    else:
        if now.year == event_time.year:
            return event_time.strftime("%I:%M %p  %B %d")
        else:
            return event_time.strftime("%I:%M %p  %B %d %Y")
