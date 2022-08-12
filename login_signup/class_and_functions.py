from star_and_channels.models import Stars
from django.contrib.auth.models import User
from .models import *
import time
from django.conf import settings
from coins_and_gifts.class_and_functions import UserCoins
from coins_and_gifts.models import *
from datetime import datetime
from django.db.models import Q
from notification_and_mails.class_and_functions import *
from random import randint
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import hashers
from pyfcm import FCMNotification


def fcm_notifications(token, message, m_from, type=None, id=None, chat_obj=None):
    path_to_fcm = "https://fcm.googleapis.com"
    server_key = "AAAA6fle2Kk:APA91bGOp9or7BjPXSzmYoeotOCKeSDO8nd7qKX8ddt_0_ksQrodI2VrFJo-bsGloI2DkUdjQnzlEsZC2ZiI8b4tiUq7MUpaP734PMSh47_PBPL4XXkLWLDPEp4CpgWo8EzOs-EgumEm"
    push_service = FCMNotification(api_key=server_key)
    reg_id = token
    message_title = m_from
    message_body = message
    if type == None:
        type = "notification"
    data_message = {
        "title": m_from,
        "body": message,
        "type": type,
        "id": id
    }

    kwargs = {
        "content_available": True,
        'extra_kwargs': {"priority": "high", "mutable_content": True, 'notification': data_message},
    }


    if chat_obj != None:
        data_message.update(chat_obj)
    print(data_message)
    try:
        device_type_obj = DeviceInfo.objects.filter(device_token=token)[0]
        if device_type_obj.device_type == 'A':
            result = push_service.notify_single_device(registration_id=token, data_message=data_message)
        else:
            result = push_service.notify_single_device(registration_id=token, message_title=message_title,
                                                       message_body=message_body, data_message=kwargs)
        # result = FCMNotification(api_key=server_key).notify_single_device(registration_id=reg_id, message_title=message_title, message_body=message_body)
        return result
    except:
        return 0


def authentication_check(request):
    try:
        blacklist = BlackListedAccessTokens.objects.filter(token=request.headers["Authorization"].split(" ")[-1])
        if len(blacklist) == 1:
            return False
        return bool(request.user and request.user.is_authenticated)
    except:
        return False


def get_id_from_auth(request):
    user_id = User.objects.filter(username=request.user)[0].id
    return user_id


def get_user_profile(user_id):
    sub_dict = {}
    user_obj = User.objects.get(pk=user_id)
    app_user_obj = AppUser.objects.filter(user_id=user_id)[0]
    device_obj = DeviceInfo.objects.filter(user_id=user_id)[0]
    sub_dict["id"] = user_obj.id
    sub_dict["name"] = user_obj.first_name
    sub_dict["email"] = user_obj.email
    sub_dict["username"] = app_user_obj.username
    sub_dict["cover_picture"] = "http://" + settings.ALLOWED_HOSTS[1] + "/media/" + \
                                str(app_user_obj.cover_picture)
    sub_dict["display_picture"] = "http://" + settings.ALLOWED_HOSTS[1] + "/media/" + \
                                  str(app_user_obj.display_picture)
    sub_dict['ropos_tag'] = get_roposo_tag(user_id)
    sub_dict["city"] = app_user_obj.city
    sub_dict["age"] = app_user_obj.age
    sub_dict["gender"] = app_user_obj.gender
    sub_dict["dob"] = app_user_obj.date_of_birth
    sub_dict["state"] = app_user_obj.state
    sub_dict["mobile_no"] = app_user_obj.mobile_no
    sub_dict["twitter"] = app_user_obj.twitter_handle
    sub_dict["bio"] = app_user_obj.about
    sub_dict["website"] = app_user_obj.website
    sub_dict["location"] = app_user_obj.location
    sub_dict["profile_link"] = "http://" + settings.ALLOWED_HOSTS[1] + "/login_signup/view_user/" + str(user_obj.id)
    sub_dict["follower_count"] = get_followers_count(user_id)
    sub_dict["notification_count"] = get_notification_count(user_id)
    sub_dict['coin'] = UserCoins(user_id=user_id).get_remaining_balance(timestamp=datetime.now())
    sub_dict["token"] = device_obj.authorization_token
    sub_dict["is_complete"] = app_user_obj.is_profile_completed
    sub_dict["is_phone_verified"] = app_user_obj.is_phone_verified
    sub_dict['support_email'] = "support@TikToker.com"
    sub_dict['support_contact'] = "X0X0X0X0X0"
    try:
        sub_dict['referral_code'] = ReferralId.objects.filter(user_id=user_obj)[0].referral_code
    except:
        sub_dict['referral_code'] = None
    return sub_dict


def get_followers_count(user_id):
    return len(UserCrossFollower.objects.filter(user_id=user_id))


def get_followings_count(user_id):
    return len(UserCrossFollower.objects.filter(followed_by=user_id))


def get_blocked_user_count(user_id):
    return len(UserXBlockedUser.objects.filter(user_id=user_id))


def get_blocked_by_count(user_id):
    return len(UserXBlockedUser.objects.filter(blocked_by=user_id))


def get_roposo_tag(user_id):
    if len(Stars.objects.filter(user_id=user_id, approved=True)) == 1:
        return "Roposo Star"
    else:
        return None


def check_if_you_follow_user(self_user_id, user_id):
    if len(UserCrossFollower.objects.filter(user_id=user_id, followed_by=self_user_id)) == 0:
        return False
    else:
        return True


def check_user_block(my_obj, user_obj):
    if len(UserXBlockedUser.objects.filter(Q(user_id=my_obj, blocked_by=user_obj) |
                                           Q(user_id=user_obj, blocked_by=my_obj))) != 0:
        return_val = True
    else:
        return_val = False
    return return_val


def get_block_list_ids(user_obj):
    block_obj_list = UserXBlockedUser.objects.filter(Q(blocked_by=user_obj) | Q(user_id=user_obj))
    block_list = []
    for block_obj in block_obj_list:
        if block_obj.user_id != user_obj:
            block_list.append(block_obj.user_id.id)
        else:
            block_list.append(block_obj.blocked_by.id)
    return block_list


def search_user(start, search_query, user_obj):
    page_size = 20
    block_list = get_block_list_ids(user_obj)
    block_list.append(user_obj.id)
    if search_query.islower():
        user_obj_list = User.objects.exclude(pk__in=block_list).filter(Q(
            Q(username__startswith=search_query) | Q(first_name__startswith=search_query) |
            Q(first_name__startswith=search_query.capitalize())) & Q(is_active=True))[start:start + page_size]
    else:
        user_obj_list = User.objects.exclude(pk__in=block_list).filter(Q(
            Q(username__startswith=search_query) | Q(first_name__startswith=search_query) |
            Q(first_name__startswith=search_query.lower())) & Q(is_active=True))[start:start + page_size]
    return user_obj_list


def genrate_and_register_new_token(username, user_id):
    token = randint(1000000000, 9999999999)
    user_obj = User.objects.get(pk=user_id)
    user_obj.password = hashers.make_password(token)
    user_obj.save()
    mutated_dict = {"username": username, "password": token}
    serializer = TokenObtainPairSerializer(data=mutated_dict)
    if serializer.is_valid():
        token = serializer.validate(mutated_dict)
        device_obj = DeviceInfo.objects.filter(user_id=user_id)[0]
        old_token = device_obj.authorization_token
        blacklist_obj = BlackListedAccessTokens(token=old_token)
        blacklist_obj.save()
        device_obj.authorization_token = token['access']
        device_obj.save()
        sub_dict = get_user_profile(user_id)


def genrate_random_email():
    ran_gen_mail = "random_genrated_" + str((randint(1000000, 9999999))) + "@mail.com"
    if User.objects.filter(email=ran_gen_mail):
        genrate_random_email()
    else:
        return ran_gen_mail


def send_otp(send_type, user_name, random_otp, receiver_number, ):
    # LOGIN SMS_GATEWAY_DETAILS:
    # IP_ADDRESS=43.252.88.230
    # user- U1299
    # password- OgXNtuzD

    # MAKE_TEST_CASE
    receiver_number = '9166910213'

    OTP_SECRET_KEY = '?secret=nvX6qW2cjCoQnjN202Gb'
    OTP_SENDER_ID = '&sender=AZAROW'
    OTP_TEMP_ID = '&tempid=1207162141751156954'
    OTP_MSG_TYPE = '1'
    OTP_ROUTE = 'TA'

    OTP_SMS_TEMP = 'Dear ' + user_name + ', your OTP from AZARO for Registration OTP is ' + random_otp + ' .Do not share the OTP with anyone for security reasons'

    OTP_BASE_URL = 'http://43.252.88.230/index.php/smsapi/httpapi/' + OTP_SECRET_KEY + OTP_SENDER_ID + OTP_TEMP_ID

    OTP_FIRST_URL = '&receiver=' + receiver_number + '&route=' + OTP_ROUTE + '&msgtype=' + OTP_MSG_TYPE + '&sms=' + OTP_SMS_TEMP

    data = requests.post(url=OTP_BASE_URL + OTP_FIRST_URL, data=format)

    print('data=', data.text)

