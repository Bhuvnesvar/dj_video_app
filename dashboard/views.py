from django.shortcuts import render
from django.db.models import Sum
from django.http import JsonResponse
from login_signup.models import *
from reported.models import *
from video.models import *
from coins_and_gifts.models import *
from star_and_channels.models import *
from effects_and_filters.models import *
from datetime import datetime, timedelta
from django.db.models import Count
from django.db.models import Q
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView


def joining_chart(request):
    data_dict = {}
    today = datetime.today()
    days_to_subtract = 30
    old_date = today - timedelta(days_to_subtract)
    for date_num in range(days_to_subtract+1):
        data_dict[old_date.strftime("%B") + " " + str(old_date.day) + " " + str(old_date.year)] = AppUser.objects.filter(
            date_joined__year=old_date.year, date_joined__month=old_date.month, date_joined__day=old_date.day).count()
        old_date = old_date + timedelta(1)

    return JsonResponse(data={
        'labels': list(data_dict.keys()),
        'data': list(data_dict.values()),
    })


def total_user(request):
    total_user=AppUser.objects.all().count()
    if total_user > 1000 and total_user < 1000000:
        total_user = str("{:.1f}".format(total_user/1000)) + " K"
    elif total_user > 1000000:
        total_user = str("{:.1f}".format(total_user/1000000)) + " M"
    return JsonResponse(data={
        'total_user': total_user,
    })

def active_user(request):
    active_user=DeviceInfo.objects.exclude(device_token="").count()
    if active_user > 1000 and active_user < 1000000:
        active_user = str("{:.1f}".format(active_user/1000)) + " K"
    if active_user > 1000000:
        active_user = str("{:.1f}".format(active_user/1000000)) + " M"
    return JsonResponse(data={
        'active_user': active_user,
    })


def gender_ratio_chart(request):
    data_dict = {}
    queryset = AppUser.objects.all().exclude(gender=None).values_list('gender').annotate(user_count=Count('gender')).order_by(
        '-user_count')
    for item in queryset:
        if item[0] == "F":
            label = "Female"
        elif item[0] == "M":
            label = "Male"
        elif item[0] == "O":
            label = "Other"
        data_dict[label] = item[1]

    return JsonResponse(data={
        'labels': list(data_dict.keys()),
        'data': list(data_dict.values()),
    })


def following_chart(request):
    data_dict = {}
    limit = 15
    queryset = UserCrossFollower.objects.values_list('user_id').annotate(user_count=Count('user_id')).order_by('-user_count')
    for item in queryset:
        data_dict[User.objects.get(pk=item[0]).username] = item[1]

    return JsonResponse(data={
        'labels': list(data_dict.keys())[0:limit],
        'data': list(data_dict.values())[0:limit],
    })


def blocking_chart(request):
    data_dict = {}
    limit = 15
    queryset = UserXBlockedUser.objects.values_list('user_id').annotate(user_count=Count('user_id')).order_by('-user_count')
    for item in queryset:
        data_dict[User.objects.get(pk=item[0]).username] = item[1]

    return JsonResponse(data={
        'labels': list(data_dict.keys())[0:limit],
        'data': list(data_dict.values())[0:limit],
    })


def reported_user_chart(request):
    data_dict = {}
    limit = 15
    today = datetime.today()
    days_to_subtract = 30
    old_date = today - timedelta(days_to_subtract)
    # queryset = UserReportHistory.objects.filter(reporting_time__range=[str(old_date.year) + "-" + str(old_date.month) + "-" + str(old_date.day),
    #     str(today.year) + "-" + str(today.month) + "-" + str(today.day)]).values_list('reported_user').annotate(user_count=Count('reported_user')).order_by('-user_count')
    queryset = UserReportHistory.objects.filter(
        reporting_time__range=[old_date.strftime("%Y-%m-%d %H:%M:%S"),
                               today.strftime("%Y-%m-%d %H:%M:%S"),]).values_list(
        'reported_user').annotate(user_count=Count('reported_user')).order_by('-user_count')

    # print("--------------------------------------------------------------------------------------------",queryset)
    # queryset = UserReportHistory.objects.values_list('reported_user').annotate(user_count=Count('reported_user')).order_by('-user_count')

    for item in queryset:
        data_dict[User.objects.get(pk=item[0]).username] = item[1]

    return JsonResponse(data={
        'labels': list(data_dict.keys())[0:limit],
        'data': list(data_dict.values())[0:limit],
    })


def reported_video_chart(request):
    data_dict = {}
    limit = 15
    today = datetime.today()
    days_to_subtract = 30
    old_date = today - timedelta(days_to_subtract)
    queryset = PostReportHistory.objects.filter(reporting_time__range=[old_date.strftime("%Y-%m-%d %H:%M:%S"),
                               today.strftime("%Y-%m-%d %H:%M:%S")]).values_list('post').annotate(post_count=Count('post')).order_by('-post_count')

    for item in queryset:
        data_dict[item[0]] = item[1]

    return JsonResponse(data={
        'labels': list(data_dict.keys())[0:limit],
        'data': list(data_dict.values())[0:limit],
    })


def report_type_chart(request):
    data_dict = {}
    limit = 15
    today = datetime.today()
    days_to_subtract = 30
    old_date = today - timedelta(days_to_subtract)
    queryset = PostReportHistory.objects.filter(reporting_time__range=[old_date.strftime("%Y-%m-%d %H:%M:%S"),
                               today.strftime("%Y-%m-%d %H:%M:%S")]).values_list('report_type').annotate(post_count=Count('report_type')).order_by('-post_count')

    for item in queryset:
        data_dict[ReportTypes.objects.get(pk=item[0]).name] = item[1]

    return JsonResponse(data={
        'labels': list(data_dict.keys())[0:limit],
        'data': list(data_dict.values())[0:limit],
    })


def most_allotted_category_chart(request):
    data_dict = {}
    limit = 15
    queryset = ChannelXUser.objects.values_list('channel_id').annotate(channel_count=Count('channel_id')).order_by('-channel_count')

    for item in queryset:
        try:
            data_dict[ChannelList.objects.get(pk=item[0]).channel_name] = item[1]
        except:
            data_dict[item[0]] = item[1]

    return JsonResponse(data={
        'labels': list(data_dict.keys())[0:limit],
        'data': list(data_dict.values())[0:limit],
    })


def Audio_uses_chart(request):
    data_dict = {}
    limit = 15
    today = datetime.today()
    days_to_subtract = 30
    old_date = today - timedelta(days_to_subtract)
    queryset = MediaXFilterXAudio.objects.filter(
        time__range=[old_date.strftime("%Y-%m-%d %H:%M:%S"),
                               today.strftime("%Y-%m-%d %H:%M:%S")]).values_list(
        'audio').annotate(post_count=Count('audio')).order_by('-post_count')

    for item in queryset:
        try:
            data_dict[AudioManagement.objects.get(pk=item[0]).audio_name] = item[1]
        except:
            data_dict[item[0]] = item[1]

    return JsonResponse(data={
        'labels': list(data_dict.keys())[0:limit],
        'data': list(data_dict.values())[0:limit],
    })

def Audio_Catogory_uses_chart(request):
    data_dict = {}
    limit = 15
    today = datetime.today()
    days_to_subtract = 30
    old_date = today - timedelta(days_to_subtract)
    queryset = MediaXFilterXAudio.objects.filter(
        time__range=[old_date.strftime("%Y-%m-%d %H:%M:%S"),
                               today.strftime("%Y-%m-%d %H:%M:%S")]).values_list(
        'audio__audio_category').annotate(post_count=Count('audio')).order_by('-post_count')

    for item in queryset:
        try:
            data_dict[AudioCategories.objects.get(pk=item[0]).audio_category] = item[1]
        except:
            data_dict[item[0]] = item[1]

    return JsonResponse(data={
        'labels': list(data_dict.keys())[0:limit],
        'data': list(data_dict.values())[0:limit],
    })


def Filter_uses_chart(request):
    data_dict = {}
    limit = 15
    today = datetime.today()
    days_to_subtract = 30
    old_date = today - timedelta(days_to_subtract)
    queryset = EffectsAndFilters.objects.filter(type="F").values_list('name').annotate(post_count=Count('name')).order_by('-post_count')
    for item in queryset:
        data_dict[item[0]] = item[1]

    return JsonResponse(data={
        'labels': list(data_dict.keys())[0:limit],
        'data': list(data_dict.values())[0:limit],
    })

def Effect_uses_chart(request):
    data_dict = {}
    limit = 15
    today = datetime.today()
    days_to_subtract = 30
    old_date = today - timedelta(days_to_subtract)
    queryset = EffectsAndFilters.objects.filter(type="E").values_list('name').annotate(post_count=Count('name')).order_by('-post_count')
    for item in queryset:
        data_dict[item[0]] = item[1]

    return JsonResponse(data={
        'labels': list(data_dict.keys())[0:limit],
        'data': list(data_dict.values())[0:limit],
    })


def Most_liked_chart(request):
    data_dict = {}
    limit = 15
    today = datetime.today()
    days_to_subtract = 30
    old_date = today - timedelta(days_to_subtract)
    filter_count= Count('liked', filter=Q(liked=True))
    queryset = MediaXLikeXViews.objects.filter(liked=True).values_list('video').annotate(post_count=Count('video')).order_by('-post_count')
    for item in queryset:
        data_dict[item[0]] = item[1]

    return JsonResponse(data={
        'labels': list(data_dict.keys())[0:limit],
        'data': list(data_dict.values())[0:limit],
    })


def Most_liked_chart(request):
    data_dict = {}
    limit = 15
    queryset = MediaXLikeXViews.objects.filter(liked=True).values_list('video').annotate(post_count=Count('video')).order_by('-post_count')
    for item in queryset:
        data_dict[item[0]] = item[1]

    return JsonResponse(data={
        'labels': list(data_dict.keys())[0:limit],
        'data': list(data_dict.values())[0:limit],
    })

def Most_viewed_chart(request):
    data_dict = {}
    limit = 15
    queryset = MediaXLikeXViews.objects.values_list('video').annotate(post_count=Count('video')).order_by('-post_count')
    for item in queryset:
        data_dict[item[0]] = item[1]

    return JsonResponse(data={
        'labels': list(data_dict.keys())[0:limit],
        'data': list(data_dict.values())[0:limit],
    })
