from rest_framework.response import Response
from rest_framework.decorators import api_view
from login_signup.class_and_functions import *
from .models import *
from .class_and_functions import *
from video.models import *
from mutagen.aac import AAC
from django.conf import settings
from login_signup.models import *
import datetime
from django.db.models import Count, Sum
from django.db.models import Q
from pyfcm import FCMNotification
from rest_framework import status


# Create your views here.
@api_view(['POST'], )
def get_transaction_history_view(request):
    data = {}
    if authentication_check(request) is True:
        try:
            start = int(request.data['start']) * 20
        except:
            data["code"] = 0
            data["error"] = True
            data["message"] = "Please send a valid start point"
            return Response(data=data)
        try:
            user_id = get_id_from_auth(request)
            transaction_history = UserCoins(user_id=user_id).get_transactions(start=start)
            if len(transaction_history) == 0:
                data["message"] = "No transactions to show"
                data["error"] = True
            else:
                data["message"] = "Transaction history"
                data["error"] = False
                data['data'] = transaction_history
            data["code"] = 0
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
def get_categories_view(request):
    data = {}
    if authentication_check(request) is True:
        try:
            cat_list = []
            category_list = AudioCategories.objects.all()
            for category_obj in category_list:
                temp_dict = {}
                temp_dict['thumbnail'] = "http://" + settings.ALLOWED_HOSTS[1] + \
                                         "/media/" + str(category_obj.audio_thumbnail)
                temp_dict['category'] = category_obj.audio_category
                temp_dict['category_id'] = category_obj.id
                cat_list.append(temp_dict)
            data["code"] = 0
            data["error"] = False
            data["message"] = "Category list"
            data['data'] = cat_list
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


@api_view(['GET'], )
def get_category_audios_view(request, cat_id=None):
    data = {}
    if authentication_check(request) is True:
        try:
            cat_obj = AudioCategories.objects.get(pk=int(cat_id))
            audio_list = []
            audio_obj_list = AudioManagement.objects.filter(audio_category=cat_obj, is_active=True)
            for audio_obj in audio_obj_list:
                temp_dict = {}
                temp_dict['audio_id'] = audio_obj.id
                temp_dict['audio_name'] = audio_obj.audio_name
                temp_dict['audio_link'] = "http://" + settings.ALLOWED_HOSTS[1] + "/media/" + str(audio_obj.audio)
                audio_location = settings.MEDIA_ROOT + "/" + str(audio_obj.audio)
                # temp_dict['duration'] = str(AAC(audio_location).info.length) + " secs"
                audio_list.append(temp_dict)
            data["code"] = 0
            data["error"] = False
            data["message"] = "Audio list"
            data['data'] = audio_list
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
def get_all_gifts_view(request):
    data = {}
    if authentication_check(request) is True:
        try:
            gift_obj_list = get_all_gifts()
            gift_list = []
            for gift_obj in gift_obj_list:
                temp_dict = {}
                temp_dict['gift_id'] = gift_obj.id
                temp_dict['gift_name'] = gift_obj.gift_name
                temp_dict['gift'] = "http://" + settings.ALLOWED_HOSTS[1] + "/media/" + str(gift_obj.gift)
                temp_dict['coin_cost'] = gift_obj.coin_cost
                gift_list.append(temp_dict)
            data["code"] = 0
            data["error"] = False
            data["message"] = "Gift list"
            data['data'] = gift_list
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
def send_gift_view(request):
    data = {}
    if authentication_check(request) is True:
        try:
            user_id = get_id_from_auth(request)
            user_obj = User.objects.get(pk=user_id)
            app_user_obj = AppUser.objects.filter(user_id=user_id)[0]
            # send_to = request.data['send_to']
            # send_to_obj = User.objects.filter(username=send_to)[0]
            admin_obj = User.objects.filter(username='admin')[0]
            gift_id = int(request.data['gift_id'])
            gift_obj = GiftManagement.objects.get(pk=gift_id)
            video_id = int(request.data['video_id'])
            video_obj = MediaTable.objects.get(pk=video_id)
            if video_obj.is_available is False:
                data["code"] = 0
                data["error"] = True
                data["message"] = "This video has been deleted"
                return Response(data=data)
            send_to_obj = video_obj.user_id
            if user_obj == send_to_obj:
                data["code"] = 0
                data["error"] = True
                data["message"] = "Sorry you can't send gift to yourself"
                return Response(data=data)
        except:
            data["code"] = 0
            data["error"] = True
            data["message"] = "Some error in parameters sent"
            return Response(data=data)
        try:
            gift_transaction = GiftTransactions(sender=user_obj, receiver=send_to_obj, gift_id=gift_obj)
            gift_transaction.save()
            gift_transaction_id = gift_transaction.id
            admin_commission = CoinManagement.objects.filter(key='admin_commission')[0].value / 100
            user_to_admin = UserCoins(sender=user_obj, receiver=admin_obj,
                                      description='Gift ' + str(gift_transaction_id),
                                      coin_count=gift_obj.coin_cost)

            admin_to_receiver = UserCoins(sender=admin_obj, receiver=send_to_obj,
                                          description='Gift ' + str(gift_transaction_id),
                                          coin_count=gift_obj.coin_cost * (1 - admin_commission))
            if user_to_admin.do_transaction() == False:
                gift_transaction.delete()
                data["code"] = 0
                data["error"] = True
                data["message"] = "Not enough coins"
                return Response(data=data)
            admin_to_receiver.do_transaction()
            Comments(video=video_obj, comment_type='M', comment_media_link="http://" + settings.ALLOWED_HOSTS[1] +
                                                                           "/media/" + str(gift_obj.gift),
                     commented_by=user_obj, commented_username=app_user_obj.username).save()
            notification_msg = f'{user_obj.first_name} sent you a {gift_obj.gift_name}'
            notification_obj = NotificationHistory(user_id=video_obj.user_id, title='New Gift',
                                                   message=notification_msg, type_id="gift " + str(gift_id))
            notification_obj.save()
            token = DeviceInfo.objects.filter(user_id=video_obj.user_id)[0]
            response = fcm_notifications(token.device_token, notification_msg, 'New Gift')
            data["code"] = 0
            data["error"] = False
            data["message"] = "Gift sent"
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
def points_view(request):
    data = {}
    if authentication_check(request) is True:
        try:
            obj = headingandpoints.objects.all()
            data1 = {}
            for i in obj:
                if i.heading not in data1.keys():
                    data1[i.heading] = [i.points]
                else:
                    data1[i.heading].append(i.points)
            points = []
            # for list in data1.values():
            #     points.append(list)
            # final={}
            sub = {}
            # count=0
            for key in data1:
                sub["head"] = key
                sub["point"] = data1[key]
                # count+=1
                points.append(sub)
                sub = {}
            data["code"] = 0
            data["error"] = False
            data["message"] = "Heading and Points"
            data["data"] = points
            return Response(data)
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


@api_view(['POST', ])
def last_day_notification_cron(request):
    data = {}
    # if authentication_check(request) is True:
    today = datetime.datetime.today()
    old_date = today + datetime.timedelta(days=-1)
    all_entries = CoinTransactions.objects.filter(
        time_of_transaction__year=old_date.year, time_of_transaction__month=old_date.month,
        time_of_transaction__day=old_date.day).values_list('receiver').annotate(
        coin_sum=Sum('coin_count')).order_by('-coin_sum')
    # data['data'] = str(all_entries)
    # data['code'] = 0
    # data['error'] = False
    # return Response(data=data)
    for obj in all_entries:
        user_obj = User.objects.get(pk=obj[0])
        notification_msg = f'You earned {obj[1]} coins yesterday. Keep posting to earn more'
        notification_obj = NotificationHistory(user_id=user_obj, title='New Coins',
                                               message=notification_msg, type_id="coin transation")
        notification_obj.save()
        try:
            token = DeviceInfo.objects.filter(user_id=obj[0])[0]
            response = fcm_notifications(token.device_token, notification_msg, 'New Coins')
        except:
            pass
    data['data'] = str(all_entries)
    data['code'] = 0
    data['error'] = False
    return Response(data=data)


@api_view(['POST'], )
def get_stickers_view(request):
    data = {}
    if authentication_check(request) is True:
        try:
            # start = int(request.data['start']) * 20
            type = request.data['type']
        except:
            data["code"] = 0
            data["error"] = True
            data["message"] = "Some error occurred"
            return Response(data=data)
        try:
            sticker_obj_list = get_all_stickers(type)
            sticker_list = []
            for sticker_obj in sticker_obj_list:
                temp_dict = {}
                temp_dict['sticker_id'] = sticker_obj.id
                temp_dict['sticker_name'] = sticker_obj.sticker_name
                temp_dict['sticker'] = "http://" + settings.ALLOWED_HOSTS[1] + "/media/" + str(sticker_obj.sticker)
                sticker_list.append(temp_dict)
            data["code"] = 0
            data["error"] = False
            data["message"] = "Sticker list"
            data['data'] = sticker_list
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
def add_mlmcoin(request):
    data = {}
    try:
        m_id = ReferralId.objects.filter(referral_code=request.data['member_id'])[0]
        coins = float(request.data['coin'])
        user_obj = User.objects.get(id=m_id.user.id)
        description = request.data['description']
        UserCoins(sender=User.objects.filter(username="admin")[0], receiver=user_obj,
                  description=description, coin_count=coins).do_transaction()
        data['code'] = 0
        data['message'] = "Transection Done"
        data['error'] = False
        return Response(data=data)

    except:
        data['code'] = 0
        data['message'] = "Invalid data"
        data['error'] = True
        return Response(status=status.HTTP_401_UNAUTHORIZED, data=data)
