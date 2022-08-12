from rest_framework.decorators import api_view
from rest_framework.response import Response
from login_signup.class_and_functions import *
from rest_framework import status
from .models import *
from .class_and_functions import *
from django.db.models import Q
from video.class_and_functions import *

@api_view(['POST'],)
def get_chat_view(request):
    data = {}
    if authentication_check(request) == True:
        user_id = get_id_from_auth(request)
        user_obj = User.objects.get(pk=user_id)
        try:
            ano_user_id = int(request.data["user_id"])
            start = int(request.data['start']) * 30
            ano_user_obj = User.objects.get(pk=ano_user_id)
        except:
            data['code'] = 0
            data['message'] = "please send user_id and start"
            data['error'] = True
            return Response(data=data)
        try:
            chat_objs = get_chat_from_db(sender=user_obj, receiver=ano_user_obj, start=start)
            chat_objs.reverse()
            sub_list = []
            for message_obj in chat_objs:
                temp_dict = {}
                temp_dict['my_message'] = message_obj.message_from.id == user_id
                temp_dict['message_id'] = message_obj.id
                temp_dict['message_from'] = message_obj.message_from.id
                temp_dict['message_to'] = message_obj.message_to.id
                temp_dict['time'] = get_date_time_string_for_chat(message_obj.time)
                temp_dict['message'] = message_obj.message
                temp_dict['seen'] = message_obj.seen
                sub_list.append(temp_dict)
            data['data'] = sub_list
            data['code'] = 0
            data['message'] = "Chat messages"
            data['error'] = False
            return Response(data=data)
        except:
            data['code'] = 0
            data['message'] = "Some error occurred"
            data['error'] = True
            return Response(data=data)
    else:
        data['code'] = 0
        data['message'] = "please provide proper authorization"
        data['error'] = True
        return Response(status=status.HTTP_401_UNAUTHORIZED, data=data)


@api_view(['POST'],)
def refresh_chat_view(request):
    data = {}
    if authentication_check(request) == True:
        user_id = get_id_from_auth(request)
        user_obj = User.objects.get(pk=user_id)
        try:
            ano_user_id = int(request.data["user_id"])
            last_message_id = int(request.data['last_message_id'])
            ano_user_obj = User.objects.get(pk=ano_user_id)
        except:
            data['code'] = 0
            data['message'] = "please send user_id and last_message_id"
            data['error'] = True
            return Response(data=data)
        try:
            chat_objs = get_chat_from_db(sender=user_obj, receiver=ano_user_obj, last_id=last_message_id)
            # sub_list = []
            # for message_obj in chat_objs:
            temp_dict = {}
            temp_dict['my_message'] = chat_objs.message_from.id == user_id
            temp_dict['message_id'] = chat_objs.id
            temp_dict['message_from'] = chat_objs.message_from.id
            temp_dict['message_to'] = chat_objs.message_to.id
            temp_dict['time'] = get_date_time_string_for_chat(chat_objs.time)
            temp_dict['message'] = chat_objs.message
            temp_dict['seen'] = chat_objs.seen
                # sub_list.append(temp_dict)
            data['data'] = temp_dict
            data['code'] = 0
            data['message'] = "Chat messages"
            data['error'] = False
            return Response(data=data)
        except:
            data['code'] = 0
            data['message'] = "Some error occurred"
            data['error'] = True
            return Response(data=data)
    else:
        data['code'] = 0
        data['message'] = "please provide proper authorization"
        data['error'] = True
        return Response(status=status.HTTP_401_UNAUTHORIZED, data=data)

#abhishek k views

@api_view(['POST'], )
def seen_view(request):
    data = {}
    if authentication_check(request) is True:
        try:
            message_id = request.data['message_id']
            user_id = get_id_from_auth(request)
        except:
            data["code"] = 0
            data["error"] = True
            data["message"] = "Opps!, Something went wrong"
            return Response(data=data)
        try:
            message_obj = ChatTable.objects.get(id=message_id)
            from_obj = message_obj.message_from
            to_obj = message_obj.message_to
            if to_obj.id != user_id:
                data["code"] = 0
                data["error"] = True
                data["message"] = "Opps!, wrong message id"
                return Response(data=data)
            unseen_obj = ChatTable.objects.filter(message_from=from_obj,message_to=to_obj,seen=False)
            for obj in unseen_obj:
                obj.seen=True
                obj.save()

            data["code"] = 0
            data["error"] = False
            data["message"] = "success"
            return Response(data=data)
        except:
            data["code"] = 0
            data["error"] = True
            data["message"] = "Some error occurred"
        return Response(data=data)
    else:
        data["code"] = 0
        data["error"] = True
        data["message"] = "Please provide proper authorization"
        return Response(status=status.HTTP_401_UNAUTHORIZED, data=data)


@api_view(['POST'], )
def delete_view(request):
    data = {}
    if authentication_check(request) is True:
        try:
            message_id = request.data['message_id']
            user_id = get_id_from_auth(request)
        except:
            data["code"] = 0
            data["error"] = True
            data["message"] = "Opps! , Something went wrong"
            return Response(data=data)
        try:
            message_obj = ChatTable.objects.get(id=message_id)
            if user_id != message_obj.message_from.id:
                data["code"] = 0
                data["error"] = False
                data["message"] = "You are not authorized to delete this message "
                return Response(data=data)
            message_obj.delete=True
            message_obj.save()

            data["code"] = 0
            data["error"] = False
            data["message"] = "Message deleted successfully"
            return Response(data=data)
        except:
            data["code"] = 0
            data["error"] = True
            data["message"] = "Some error occurred"
        return Response(data=data)
    else:
        data["code"] = 0
        data["error"] = True
        data["message"] = "Please provide proper authorization"
        return Response(status=status.HTTP_401_UNAUTHORIZED, data=data)



@api_view(['POST'], )
def send_view(request):
    data = {}
    if authentication_check(request) is True:
        try:
            to = request.data['to']
            message = request.data['message']
            user_id = get_id_from_auth(request)
            from_obj = User.objects.get(pk=user_id)
            to_obj = User.objects.get(pk=to)
        except:
            data["code"] = 0
            data["error"] = True
            data["message"] = "Opps! , Something went wrong"
            return Response(data=data)
        try:
            message_obj = ChatTable(message_from=from_obj,message_to=to_obj,message=message)
            message_obj.save()

            temp_dict = {}
            temp_dict['my_message'] = True
            temp_dict['message_id'] = message_obj.id
            temp_dict['message_from'] = message_obj.message_from.id
            temp_dict['message_to'] = message_obj.message_to.id
            temp_dict['time'] = get_date_time_string_for_chat(message_obj.time)
            temp_dict['message'] = message_obj.message
            temp_dict['seen'] = message_obj.seen
            token = DeviceInfo.objects.filter(user_id=to_obj.id)[0]
            notification_setting=NotificationEmailSettings.objects.filter(user_id=to_obj)[0]
            if token != "" and  notification_setting.n_chat_notification==True:
                response = fcm_notifications(token.device_token, message,from_obj.first_name,"chat",from_obj.id,temp_dict)
            data["code"] = 0
            data["error"] = False
            data["message"] = "Message send successfully"
            data["data"] = temp_dict
            return Response(data=data)
        except:
            data["code"] = 0
            data["error"] = True
            data["message"] = "Some error occurred"
        return Response(data=data)
    else:
        data["code"] = 0
        data["error"] = True
        data["message"] = "Please provide proper authorization"
        return Response(status=status.HTTP_401_UNAUTHORIZED, data=data)


@api_view(['POST'], )
def chat_view(request):
    data = {}
    if authentication_check(request) is True:
        try:
            user_id = get_id_from_auth(request)
            from_obj = User.objects.get(pk=user_id)
            # to_obj = User.objects.get(pk=to)

        except:
            data["code"] = 0
            data["error"] = True
            data["message"] = "Opps! , Something went wrong"
            return Response(data=data)
        try: #.order_by().values_list('foreign_key', flat=True).distinct()
            chat_objs = ChatTable.objects.filter(Q(message_to=user_id,delete=False)|
                Q(message_from=user_id,delete=False)).order_by('-time')
            sublist=chat_objs.values_list('message_from', 'message_to')
            concat_list = []
            for sub in sublist:
                concat_list += sub
            distinct_list = []
            for id in concat_list:
                if id != user_id:
                    if id not in distinct_list:
                        distinct_list.append(id)

            sublist=[]
            for to_id in distinct_list:
                sub_data={}
                to_obj = User.objects.get(pk=to_id)
                to_AppUser_obj=AppUser.objects.filter(user_id=to_obj)[0]
                sub_data["username"]=to_obj.username
                sub_data["first_name"] = to_obj.first_name
                sub_data["id"] = to_obj.id
                sub_data["display_picture"] = "http://" + settings.ALLOWED_HOSTS[1] + "/media/" +\
                str(to_AppUser_obj.display_picture)
                try:
                    sub_data["last_message"] = ChatTable.objects.filter(Q(message_from=to_id,message_to=user_id,delete=False)|
                    Q(message_from=user_id,message_to=to_id,delete=False)).order_by('-time')[0].message
                    sublist.append(sub_data)
                except:
                    pass
            data["code"] = 0
            data["error"] = False
            data["message"] = "fetched"
            data["data"]=sublist
            return Response(data=data)
        except:
            data["code"] = 0
            data["error"] = True
            data["message"] = "Some error occurred"
        return Response(data=data)
    else:
        data["code"] = 0
        data["error"] = True
        data["message"] = "Please provide proper authorization"
        return Response(status=status.HTTP_401_UNAUTHORIZED, data=data)


# @api_view(['POST'], )
# def chat_view(request):
#     data = {}
#     if authentication_check(request) is True:
#         try:
#             user_id = get_id_from_auth(request)
#             from_obj = User.objects.get(pk=user_id)
#             # to_obj = User.objects.get(pk=to)
#
#         except:
#             data["code"] = 0
#             data["error"] = True
#             data["message"] = "Opps! , Something went wrong"
#             return Response(data=data)
#         try: #.order_by().values_list('foreign_key', flat=True).distinct()
#             from_objs = list(ChatTable.objects.order_by().values_list('message_from', flat=True).distinct())
#             to_objs = list(ChatTable.objects.order_by().values_list('message_to', flat=True).distinct())
#             final_list = set(from_objs + to_objs)
#             sublist=[]
#             try:
#                 final_list.remove(user_id)
#             except:
#                 data["code"] = 0
#                 data["error"] = False
#                 data["message"] = "fetched"
#                 data["data"]=sublist
#                 return Response(data=data)
#             for to_id in final_list:
#                 sub_data={}
#                 to_obj = User.objects.get(pk=to_id)
#                 to_AppUser_obj=AppUser.objects.filter(user_id=to_obj)[0]
#                 sub_data["username"]=to_obj.username
#                 sub_data["first_name"] = to_obj.first_name
#                 sub_data["id"] = to_obj.id
#                 sub_data["display_picture"] = "http://" + settings.ALLOWED_HOSTS[1] + "/media/" +\
#                 str(to_AppUser_obj.display_picture)
#                 try:
#                     sub_data["last_message"] = ChatTable.objects.filter(Q(message_from=to_id,message_to=user_id,delete=False)|
#                     Q(message_from=user_id,message_to=to_id,delete=False)).order_by('-time')[0].message
#                     sublist.append(sub_data)
#                 except:
#                     pass
#             data["code"] = 0
#             data["error"] = False
#             data["message"] = "fetched"
#             data["data"]=sublist
#             return Response(data=data)
#         except:
#             data["code"] = 0
#             data["error"] = True
#             data["message"] = "Some error occurred"
#         return Response(data=data)
#     else:
#         data["code"] = 0
#         data["error"] = True
#         data["message"] = "Please provide proper authorization"
#         return Response(status=status.HTTP_401_UNAUTHORIZED, data=data)
