from .models import *
from django.db.models import Q
from video.models import *
from login_signup.class_and_functions import *


def check_is_star(user_obj):
    if Stars.objects.filter(user_id=user_obj, approved=True):
        return True
    else:
        return False

def get_category(user_obj):
    channel_list = ChannelXUser.objects.filter(user_id=user_obj, approved=True)
    if channel_list:
        return channel_list[0].channel_id.channel_name
    else:
        return None

def get_all_stars():
    return Stars.objects.filter(approved=True)


def get_all_channels():
    return ChannelList.objects.all()


def get_all_channel_users(channel_id):
    return ChannelXUser.objects.filter(channel_id=channel_id)


def get_all_videos_of_channel(channel_id, start, user_obj):
    page_size = 20
    channel_user_obj_list = get_all_channel_users(channel_id)
    values = []
    for channel_user_obj in channel_user_obj_list:
        values.append(channel_user_obj.user_id)
    block_list = get_block_list_ids(user_obj)
    block_list.append(user_obj.id)
    try:
        return MediaTable.objects.exclude(Q(user_id__in=block_list) | Q(is_available=False)
                                          ).filter(user_id__in=values).order_by('-uploaded_at')[start:start + page_size]
    except:
        return False


def get_all_videos_of_star(start, user_obj):
    page_size = 20
    star_user_obj_list = Stars.objects.filter(approved=True)
    values = []
    for star_user_obj in star_user_obj_list:
        values.append(star_user_obj.user_id)
    block_list = get_block_list_ids(user_obj)
    block_list.append(user_obj.id)
    try:
        return MediaTable.objects.exclude(Q(user_id__in=block_list) | Q(is_available=False)).filter(user_id__in=values).order_by('-uploaded_at'
                                                                                            )[start:start + page_size]
    except:
        return False
