from django.shortcuts import render
from rest_framework.decorators import api_view
from login_signup.class_and_functions import *
from rest_framework.response import Response
from .class_and_functions import *
from .models import *
from video.models import *
from django.db.models import Q
from django.db.models import Count
from rest_framework import status


@api_view(['POST', ])
def get_channel_list_view(request):
    data = {}
    if authentication_check(request) is True:
        try:
            channel_obj_list = get_all_channels()
            channel_list =[]
            for channel_obj in channel_obj_list:
                temp_dict = {}
                temp_dict['channel_name'] = channel_obj.channel_name
                temp_dict['api_link'] = "http://" + settings.ALLOWED_HOSTS[1] + \
                                        "/star_and_channels/get_channel_videos/"
                temp_dict['channel_id'] =  channel_obj.id
                channel_list.append(temp_dict)
            temp_dict = {}
            temp_dict['channel_name'] = 'roposo star'
            temp_dict['api_link'] = "http://" + settings.ALLOWED_HOSTS[1] + "/star_and_channels/get_star_videos/"
            temp_dict['channel_id'] = None
            channel_list.append(temp_dict)
            data['code'] = 0
            data['error'] = False
            data['message'] = "Channel list"
            data['data'] = channel_list
            return Response(data=data)
        except:
            data['code'] = 0
            data['message'] = "Some error occurred"
            data['error'] = True
            return Response(data=data)
    else:
        data['code'] = 0
        data['message'] = "Authorization error"
        data['error'] = True
        return Response(status=status.HTTP_401_UNAUTHORIZED,data=data)


@api_view(['POST', ])
def get_channel_videos_view(request):
    data = {}
    if authentication_check(request) is True:
        try:
            channel_id = request.data['channel_id']
            start = int(request.data['start']) * 20
        except:
            data['code'] = 0
            data['message'] = "Please provide start and channel_id"
            data['error'] = True
            return Response(data=data)
        try:
            user_obj = User.objects.get(pk=get_id_from_auth(request))
            video_obj_list = get_all_videos_of_channel(channel_id, start, user_obj)
            if video_obj_list is False:
                data['code'] = 0
                data['message'] = "No videos to show"
                data['error'] = True
                return Response(data=data)
            video_list = []
            for video_obj in video_obj_list:
                temp_dict = {}
                temp_dict['video_link'] = "http://" + settings.ALLOWED_HOSTS[1] + "/video/watch_video/" + \
                                          str(video_obj.id)
                video_list.append(temp_dict)
            data['code'] = 0
            data['error'] = False
            data['message'] = "Video list"
            data['data'] = video_list
            return Response(data=data)
        except:
            data['code'] = 0
            data['message'] = "Some error occurred"
            data['error'] = True
            return Response(data=data)
    else:
        data['code'] = 0
        data['message'] = "Authorization error"
        data['error'] = True
        return Response(status=status.HTTP_401_UNAUTHORIZED,data=data)


@api_view(['POST', ])
def get_star_videos_view(request):
    data = {}
    if authentication_check(request) is True:
        try:
            start = int(request.data['start']) * 20
        except:
            data['code'] = 0
            data['message'] = "Please provide start"
            data['error'] = True
            return Response(data=data)
        try:
            user_obj = User.objects.get(pk=get_id_from_auth(request))
            video_obj_list = get_all_videos_of_star(start, user_obj)
            if video_obj_list is False:
                data['code'] = 0
                data['message'] = "No videos to show"
                data['error'] = True
                return Response(data=data)
            video_list = []
            for video_obj in video_obj_list:
                temp_dict = {}
                temp_dict['video_link'] = "http://" + settings.ALLOWED_HOSTS[1] + "/video/watch_video/" + \
                                          str(video_obj.id)
                video_list.append(temp_dict)
            data['code'] = 0
            data['error'] = False
            data['message'] = "Video list"
            data['data'] = video_list
            return Response(data=data)
        except:
            data['code'] = 0
            data['message'] = "Some error occurred"
            data['error'] = True
            return Response(data=data)
    else:
        data['code'] = 0
        data['message'] = "Authorization error"
        data['error'] = True
        return Response(status=status.HTTP_401_UNAUTHORIZED,data=data)

@api_view(['POST', ])
def get_star_requirments(request):
    data = {}
    sdata={}
    if authentication_check(request) is True:
        all_entries = StarManagement.objects.all()
        for obj in all_entries:
            sdata[obj.key]=obj.value
        data['data']=sdata
        data['code'] = 0
        data['error'] = False
        return Response(data=data)
    else:
        data['code'] = 0
        data['message'] = "Authorization error"
        data['error'] = True
        return Response(status=status.HTTP_401_UNAUTHORIZED,data=data)


@api_view(['POST',])
def find_star_cron(request):
    data = {}
    sdata = {}
    # if authentication_check(request) is True:
    all_entries = StarManagement.objects.all()
    for obj in all_entries:
        sdata[obj.key] = obj.value
    view_count=sdata['views']
    count=0
    queryset=MediaXLikeXViews.objects.values_list('video').annotate(user_count=Count('viewed_by')).order_by('-user_count')
    for item in queryset:
        if item[1] >=view_count:
            try:
                media_obj=MediaTable.objects.get(pk=item[0])
                user_obj=User.objects.get(pk=media_obj.user_id)
                star_obj=Stars(user_id=user_obj,)
                star_obj.save()
                count+=1
            except:
                pass
    like_count = sdata['likes']
    filter_count = Count('liked', filter=Q(liked=True))
    queryset1 = MediaXLikeXViews.objects.values_list('video').annotate(user_count=filter_count).order_by('-user_count')
    for item in queryset1:
        if item[1] >= like_count:
            try:
                media_obj = MediaTable.objects.get(pk=item[0])
                user_obj = User.objects.get(pk=media_obj.user_id)
                star_obj = Stars(user_id=user_obj, )
                star_obj.save()
                count += 1
            except:
                pass
    post_count = sdata['number_of_post']
    queryset1 = MediaTable.objects.values_list('user_id').annotate(user_count=Count('video')).order_by('-user_count')
    for item in queryset1:
        if item[1] >= post_count:
            try:
                user_obj = User.objects.get(pk=item[0])
                star_obj = Stars(user_id=user_obj, )
                star_obj.save()
                count += 1
            except:
                pass
    data['data'] = {"New Star count":count}
    data['code'] = 0
    data['error'] = False
    return Response(data=data)
