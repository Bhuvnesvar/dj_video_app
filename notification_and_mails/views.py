from django.shortcuts import render
from .models import *
from rest_framework.decorators import api_view
from login_signup.class_and_functions import *
from rest_framework.response import Response
from coins_and_gifts.models import *
from video.models import *
from video.class_and_functions import *
from rest_framework import status
from django.template import Context, Template


@api_view(['POST'])
def get_notifications_view(request):
    data = {}
    if authentication_check(request) is True:
        user_id = get_id_from_auth(request)
        notifications = list(NotificationHistory.objects.filter(user_id=user_id).order_by("time"))
        notifications.reverse()
        sub_list = []
        count = 0
        try:
            for notification in notifications:
                split_list = notification.type_id.split(" ")
                if split_list[0] == 'post':
                    id = split_list[-1]
                    type = "post"
                    image_link = "http://" + settings.ALLOWED_HOSTS[1] + "/media/" + str(
                        MediaTable.objects.get(pk=int(id)).thumbnail)
                elif split_list[0] == 'gift':
                    id = None
                    type = "gift"
                    # print(split_list)
                    image_link = "http://" + settings.ALLOWED_HOSTS[1] + "/media/" + str(
                        GiftManagement.objects.get(pk=int(split_list[-1])).gift)
                    # image_link = "None"
                elif split_list[0] == 'follow':
                    id = split_list[-1]
                    type = "follow"
                    # print(split_list)
                    image_link = "http://" + settings.ALLOWED_HOSTS[1] + "/media/" + str(
                        AppUser.objects.get(user_id=User.objects.get(pk=int(split_list[-1]))).display_picture)
                else:
                    id = None
                    type = "coin"
                    image_link = "None"
                sub_list.append({
                    'notification_id': notification.id,
                    "notification_title": notification.title,
                    "notification_message": notification.message,
                    'type': type,
                    'id': id,
                    'image': image_link,
                    'is_read': notification.is_read,
                    'time': get_date_time_string(notification.time)
                })
                if notification.is_read is True:
                    count += 1
            data["code"] = 0
            data["error"] = False
            data['message'] = "Success"
            data['count'] = count
            data["data"] = sub_list
            return Response(data=data)
        except:
            data["code"] = 0
            data["error"] = True
            data['message'] = "Some error occurred"
            return Response(data=data)
    else:
        data['code'] = 0
        data['message'] = "Please provide proper authorization"
        data['error'] = True
        return Response(status=status.HTTP_401_UNAUTHORIZED, data=data)


@api_view(['POST'])
def mark_notification_as_read_view(request):
    data = {}
    if authentication_check(request) is True:
        user_id = get_id_from_auth(request)
        try:
            notification_id = int(request.data['notification_id'])
        except:
            data["code"] = 0
            data["error"] = True
            data['message'] = "Please send a notification id"
            return Response(data=data)
        try:
            if notification_id == 0:
                notification_list = NotificationHistory.objects.filter(user_id=User.objects.get(pk=user_id),
                                                                       is_read=False)
                for notification_obj in notification_list:
                    notification_obj.is_read = True
                    notification_obj.save()
            else:
                notification_obj = NotificationHistory.objects.get(pk=notification_id)
                notification_obj.is_read = True
                notification_obj.save()
            data["code"] = 0
            data["error"] = False
            data['message'] = "Success"
            return Response(data=data)
        except:
            data["code"] = 0
            data["error"] = True
            data['message'] = "Some error occurred"
            return Response(data=data)
    else:
        data['code'] = 0
        data['message'] = "Please provide proper authorization"
        data['error'] = True
        return Response(status=status.HTTP_401_UNAUTHORIZED, data=data)


@api_view(['POST'])
def notification_setting_view(request):
    data = {}
    if authentication_check(request) is True:
        user_id = get_id_from_auth(request)
        try:
            n_follows_me = bool(int(request.data['n_follows_me']))
            e_follows_me = bool(int(request.data['e_follows_me']))
            n_like_my_activity = bool(int(request.data['n_like_my_activity']))
            e_like_my_activity = bool(int(request.data['e_like_my_activity']))
            n_comment_my_activity = bool(int(request.data['n_comment_my_activity']))
            e_comment_my_activity = bool(int(request.data['e_comment_my_activity']))
            n_any_other_activity = bool(int(request.data['n_any_other_activity']))
            e_any_other_activity = bool(int(request.data['e_any_other_activity']))
            n_occasional_updates = bool(int(request.data['n_occasional_updates']))
            e_occasional_updates = bool(int(request.data['e_occasional_updates']))
            n_chat_notification = bool(int(request.data['n_chat_notification']))

        except:
            data["code"] = 0
            data["error"] = True
            data['message'] = "Something is missing."
            return Response(data=data)
        try:
            obj = NotificationEmailSettings.objects.filter(user_id=user_id)[0]
            obj.n_follows_me = n_follows_me
            obj.e_follows_me = e_follows_me
            obj.n_like_my_activity = n_like_my_activity
            obj.e_like_my_activity = e_like_my_activity
            obj.n_comment_my_activity = n_comment_my_activity
            obj.e_comment_my_activity = e_comment_my_activity
            obj.n_any_other_activity = n_any_other_activity
            obj.e_any_other_activity = e_any_other_activity
            obj.n_occasional_updates = n_occasional_updates
            obj.e_occasional_updates = e_occasional_updates
            obj.n_chat_notification = n_chat_notification
            obj.save()
            data["code"] = 0
            data["error"] = False
            data['message'] = "Settings updated."
            return Response(data=data)
        except:
            data["code"] = 0
            data["error"] = True
            data['message'] = "Something went wrong."
            return Response(data=data)
    else:
        data['code'] = 0
        data['message'] = "Please provide proper authorization"
        data['error'] = True
        return Response(status=status.HTTP_401_UNAUTHORIZED, data=data)


@api_view(['POST'])
def get_tnc_view(request):
    data = {}
    try:
        obj = TermAndConditionAndPolicy.objects.filter(title__icontains="Terms")[0]
        data["code"] = 0
        data["error"] = False
        data['message'] = "Terms and conditions"
        data['data'] = {'title': obj.title, 'body': obj.body}
    except:
        data["code"] = 0
        data["error"] = True
        data['message'] = "Some error occurred"
    return Response(data=data)


@api_view(['POST'])
def get_policy_view(request):
    data = {}
    try:
        obj = TermAndConditionAndPolicy.objects.filter(title__icontains="Privacy")[0]
        data["code"] = 0
        data["error"] = False
        data['message'] = "Privacy Policy"
        data['data'] = {'title': obj.title, 'body': obj.body}
    except:
        data["code"] = 0
        data["error"] = True
        data['message'] = "Some error occurred"
    return Response(data=data)


@api_view(['POST', 'GET'])
def get_policy_render(request):
    data = {}
    try:
        obj = TermAndConditionAndPolicy.objects.filter(title__icontains="Privacy")[0]
        data["code"] = 0
        data["error"] = False
        data['message'] = "Privacy Policy"
        data['data'] = {'title': obj.title, 'body': obj.body}
    except:
        data["code"] = 0
        data["error"] = True
        data['message'] = "Some error occurred"
        data['data'] = {'title': 'ERROR', 'body': "Error"}
    return render(request, 'notification_and_mails/privacy_policy.html', data)


@api_view(['POST'])
def get_notification_setting_view(request):
    data = {}
    if authentication_check(request) is True:
        user_id = get_id_from_auth(request)
        try:
            obj = NotificationEmailSettings.objects.filter(user_id=user_id)[0]
            temp_dict = {}
            temp_dict["n_follows_me"] = obj.n_follows_me
            temp_dict["e_follows_me"] = obj.e_follows_me
            temp_dict["n_like_my_activity"] = obj.n_like_my_activity
            temp_dict["e_like_my_activity"] = obj.e_like_my_activity
            temp_dict["n_comment_my_activity"] = obj.n_comment_my_activity
            temp_dict["e_comment_my_activity"] = obj.e_comment_my_activity
            temp_dict["n_any_other_activity"] = obj.n_any_other_activity
            temp_dict["e_any_other_activity"] = obj.e_any_other_activity
            temp_dict["n_occasional_updates"] = obj.n_occasional_updates
            temp_dict["e_occasional_updates"] = obj.e_occasional_updates
            temp_dict["n_chat_notification"] = obj.n_chat_notification
            data["code"] = 0
            data["error"] = False
            data["data"] = temp_dict
            data['message'] = "Settings view"
            return Response(data=data)
        except:
            data["code"] = 0
            data["error"] = True
            data['message'] = "Something went wrong."
            return Response(data=data)
    else:
        data['code'] = 0
        data['message'] = "Please provide proper authorization"
        data['error'] = True
        return Response(status=status.HTTP_401_UNAUTHORIZED, data=data)
