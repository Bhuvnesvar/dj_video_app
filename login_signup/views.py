from .serializers import AuthUserSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from random import randint
from django.contrib.auth import hashers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import hashlib
from .class_and_functions import *
from notification_and_mails.models import *
from coins_and_gifts.class_and_functions import *
from rest_framework import status
from .models import *
from notification_and_mails.models import *
from datetime import datetime
import os
from django.conf import settings
from django.utils.timezone import make_aware
import re


@api_view(['POST'])
def createUser(request):
    data = {}
    try:
        LANG = request.headers["LANG"]
        DEVICEID = request.headers["DEVICEID"]
        DEVICEINFO = request.headers["DEVICEINFO"]
        APPINFO = request.headers["APPINFO"]
        DEVICETYPE = request.headers["DEVICETYPE"]
        TOKEN = request.headers["TOKEN"]

        date_of_birth = request.POST.get('date_of_birth', '')
        mobile_no = request.POST.get('mobile_no', '')
        gender = request.POST.get('gender', '')
        email = request.POST.get('email', '')
        username = request.POST.get('username', '')
        leg = request.POST.get('leg', '')
        name = request.POST.get('name', '')
        referral_code = request.POST.get('referral_code')

        if not username:
            data['code'] = 0
            data['message'] = " Username required."
            data['error'] = True
            return Response(data=data)

        if len(AppUser.objects.filter(username=username)) > 0:
            data['code'] = 0
            data['message'] = "Username already registered."
            data['error'] = True
            return Response(data=data)

        if not email:
            data['code'] = 0
            data['message'] = "Email required."
            data['error'] = True
            return Response(data=data)

        if re.search("^([\w\.\-]+)@([\w\-]+)((\.(\w){2,3})+)$", email) is None:
            data['code'] = 0
            data['message'] = "Send a valid email."
            data['error'] = True
            return Response(data=data)

        if len(User.objects.filter(email=email)) > 0:
            data['code'] = 0
            data['message'] = "Email already registered."
            data['error'] = True
            return Response(data=data)

        if not mobile_no:
            data['code'] = 0
            data['message'] = "Mobile number required."
            data['error'] = True
            return Response(data=data)

        if not mobile_no.isdigit():
            status_code = status.HTTP_400_BAD_REQUEST
            data['error'] = True
            data['code'] = status_code
            data['message'] = 'Please enter valid mobile number.'
            return Response(data=data)

        if len(AppUser.objects.filter(mobile_no=mobile_no)) > 0:
            data['code'] = 0
            data['message'] = "Mobile number already registered."
            data['error'] = True
            return Response(data=data)

        if not name:
            data['code'] = 0
            data['message'] = "Name required."
            data['error'] = True
            return Response(data=data)

        if not gender:
            data['code'] = 0
            data['message'] = "Gender required."
            data['error'] = True
            return Response(data=data)

        if not date_of_birth:
            data['code'] = 0
            data['message'] = "Dob required."
            data['error'] = True
            return Response(data=data)

        try:
            passw = randint(100000, 999999)
            userObj = User()
            userObj.email = email
            userObj.password = hashers.make_password(passw)
            userObj.first_name = name
            userObj.username = mobile_no
            userObj.is_active = True

            userObj.save()

            mutated_dict = {'username': mobile_no, "password": passw}
            serializer = TokenObtainPairSerializer(data=mutated_dict)

            if serializer.is_valid():
                token1 = serializer.validate(mutated_dict)
                token = token1['access']
                print("SSSS" + str(token))
                userQuery = User.objects.filter(email=email)[0]

                Y, M, D = request.data["date_of_birth"].split("-")
                birthday = datetime(int(Y), int(M), int(D), 12, 0, 0)

                appUserObj = AppUser()
                appUserObj.user_id = userQuery
                appUserObj.username = username
                appUserObj.mobile_no = mobile_no
                appUserObj.gender = gender
                appUserObj.date_of_birth = date_of_birth
                appUserObj.is_phone_verified = False
                appUserObj.is_profile_completed = True
                appUserObj.age = (datetime.now() - birthday).days
                appUserObj.ref_code = referral_code
                appUserObj.save()

                deviceInfoObj = DeviceInfo()
                deviceInfoObj.user_id = userQuery
                deviceInfoObj.app_info = APPINFO
                deviceInfoObj.device_id = DEVICEID
                deviceInfoObj.device_type = DEVICETYPE
                deviceInfoObj.device_info = DEVICEINFO
                deviceInfoObj.device_token = TOKEN
                deviceInfoObj.authorization_token = token
                deviceInfoObj.lang = LANG
                deviceInfoObj.save()

                coin_managment_obj = CoinManagement.objects.filter(key='join')[0]
                UserCoins(sender=User.objects.filter(username="admin")[0], receiver=userObj,
                          description=coin_managment_obj.key, coin_count=coin_managment_obj.value).do_transaction()
                print("DEBUG +" "TEST")
                DeviceInfo_obj = DeviceInfo.objects.filter(user_id=userObj.id)[0]
                create_referral_code(userObj, appUserObj.mobile_no, referral_code, DeviceInfo_obj.device_id,
                                     DeviceInfo_obj.device_token, request.data["date_of_birth"], leg)

                try:
                    NotificationEmailSettings(user_id=userQuery).save()
                except:
                    data['code'] = 0
                    data['message'] = "Failed to create notification settings"
                    data['error'] = True
                    return Response(data=data)

                # Response Fire
                statusCode = status.HTTP_200_OK
                data["code"] = statusCode
                data["error"] = False
                data["message"] = "Signup successfully."
                data["data"] = get_user_profile(userQuery.id)
                os.mkdir(settings.MEDIA_ROOT + "/user_" + str(userQuery.id))
                return Response(data=data)

        except Exception as error:
            user_obj = User.objects.filter(email=email)[0]
            user_obj.delete()

            print("CAL2L")
            statusCode = status.HTTP_400_BAD_REQUEST
            data["code"] = statusCode
            data["error"] = True
            data["message"] = str(error)
            return Response(data=data)

    except Exception as error:
        print(str(error))
        print("CAL1L")
        data["code"] = 0
        data["error"] = True
        data["message"] = str(error)
        return Response(data=data)


@api_view(['POST'], )
def login_view(request):
    data = {}
    try:
        print(request.user)

        LANG = request.headers["LANG"]
        DEVICEID = request.headers["DEVICEID"]
        DEVICEINFO = request.headers["DEVICEINFO"]
        APPINFO = request.headers["APPINFO"]
        DEVICETYPE = request.headers["DEVICETYPE"]
        TOKEN = request.headers["TOKEN"]

        mobile_no = request.data['mobile_no']

        if not mobile_no.isdigit():
            data["code"] = 0
            data["error"] = True
            data["message"] = "Please provide a valid mobile number"
            return Response(data=data)
    except:
        data["code"] = 0
        data["error"] = True
        data["message"] = "Please provide a valid mobile number"
        return Response(data=data)

    if len(AppUser.objects.filter(mobile_no=mobile_no)):
        token = randint(100000, 999999)
        otp = token
        app_user_obj = AppUser.objects.filter(mobile_no=mobile_no)[0]
        user_obj = User.objects.get(pk=app_user_obj.user_id_id)

        if user_obj.is_active is False:
            data["code"] = 0
            data["error"] = True
            data['message'] = "This account is suspended."
            return Response(data=data)

        user_obj.password = hashers.make_password(token)
        print('if' + str(hashers.make_password(token)) + "")

        app_user_obj.hash_key = (hashlib.sha256(str(token).encode())).hexdigest()
        app_user_obj.otp_time = time.time()
        app_user_obj.save()
        user_obj.save()

        mutated_dict = {}
        mutated_dict['username'] = mobile_no
        mutated_dict["password"] = token
        tokenSerializer = TokenObtainPairSerializer(data=mutated_dict)
        print('else' + str(hashers.make_password(token)) + "")

        if tokenSerializer.is_valid():
            token1 = tokenSerializer.validate(mutated_dict)
            token = token1['access']

        try:
            print("CALL")
            device_obj = DeviceInfo.objects.filter(user_id=user_obj)[0]
            old_token = device_obj.authorization_token
            blacklist_obj = BlackListedAccessTokens(token=old_token)
            blacklist_obj.save()
            device_obj.lang = LANG
            device_obj.device_id = DEVICEID
            device_obj.device_info = DEVICEINFO
            device_obj.device_type = DEVICETYPE
            device_obj.app_info = APPINFO
            device_obj.device_token = TOKEN
            device_obj.authorization_token = token
            device_obj.save()
            blacklist_obj.save()
        except:
            DeviceInfo_obj = DeviceInfo(lang=LANG, device_id=DEVICEID, device_info=DEVICEINFO,
                                        device_type=DEVICETYPE, app_info=APPINFO,
                                        device_token=TOKEN, authorization_token=token, user_id=user_obj)
            DeviceInfo_obj.save()

        data["code"] = 0
        data["error"] = False
        data['message'] = "Success"
        data['data'] = get_user_profile(user_obj.id)
        data["mobile_no"] = mobile_no
        data["otp"] = otp
        return Response(data=data)
    else:
        token = randint(100000, 999999)
        otp = token
        created_user_flag = 0

        try:
            mutated_dict = {}
            mutated_dict['username'] = mobile_no
            mutated_dict["password"] = hashers.make_password(token)
            mutated_dict["email"] = genrate_random_email()
            serializer = AuthUserSerializer(data=mutated_dict)
            tokenSerializer = TokenObtainPairSerializer(data=mutated_dict)
            print('else' + str(hashers.make_password(token)) + "")

            if serializer.is_valid() and tokenSerializer.is_valid():
                serializer.save()
                token1 = serializer.validate(mutated_dict)
                token = token1['access']
                created_user_flag = 1
                user_obj = User.objects.filter(username=mobile_no)[0]
                app_user_obj = AppUser(username=mobile_no, mobile_no=mobile_no, user_id=user_obj, otp_time=time.time())
                app_user_obj.hash_key = (hashlib.sha256(str(token).encode())).hexdigest()
                app_user_obj.save()

                DeviceInfo_obj = DeviceInfo(lang=LANG, device_id=DEVICEID, device_info=DEVICEINFO,
                                            device_type=DEVICETYPE, app_info=APPINFO,
                                            device_token=TOKEN, authorization_token=token, user_id=user_obj)
                DeviceInfo_obj.save()

                created_user_flag = 0
                # data["status"] = status.HTTP_200_OK
                data["code"] = 0
                data["error"] = False
                data["message"] = "Created successfully"
                data["mobile_no"] = mobile_no
                data['data'] = get_user_profile(user_obj.id)
                data["otp"] = otp
                os.mkdir(settings.MEDIA_ROOT + "/user_" + str(user_obj.id))
                return Response(data=data)

        except:
            if created_user_flag == 1:
                user_obj = User.objects.filter(username=mobile_no)[0]
                user_obj.delete()
            data["code"] = 0
            data["error"] = True
            data["message"] = "User not found."
            return Response(data=data)


@api_view(['POST'], )
def logout_view(request):
    token = request.headers["Authorization"].split(" ")[-1]
    data = {}
    if authentication_check(request) is True:
        device_obj = DeviceInfo.objects.filter(user_id=get_id_from_auth(request))[0]
        device_obj.device_token = ""
        device_obj.save()
        blacklist_obj = BlackListedAccessTokens(token=token)
        blacklist_obj.save()
        data["code"] = 0
        data["error"] = False
        data["message"] = "Logout successful"
        return Response(data=data)
    else:
        data["code"] = 0
        data["error"] = True
        data["message"] = "User not authorised"
        return Response(data=data)


@api_view(['POST'], )
def otp_verification_view(request):
    data = {}
    try:
        mobile_no = request.data['mobile_no']
        otp = request.data['otp']
        try:
            LANG = request.headers["LANG"]
            DEVICEID = request.headers["DEVICEID"]
            DEVICEINFO = request.headers["DEVICEINFO"]
            APPINFO = request.headers["APPINFO"]
            DEVICETYPE = request.headers["DEVICETYPE"]
            TOKEN = request.headers["TOKEN"]
        except:
            data["code"] = 0
            data["error"] = True
            data["message"] = "Incomplete details"
            return Response(data=data)
    except:
        data["code"] = 0
        data["error"] = True
        data["message"] = "Please provide mobile number"
        return Response(data=data)
    try:
        app_user_obj = AppUser.objects.filter(mobile_no=mobile_no)[0]
        username = app_user_obj.username
        hashed_otp = (hashlib.sha256(otp.encode())).hexdigest()
    except:
        data["code"] = 0
        data["error"] = True
        data["message"] = "User not found"
        return Response(data=data)
    if time.time() - app_user_obj.otp_time < 300:
        mutated_dict = {"username": mobile_no, "password": otp}
        user_obj = app_user_obj.user_id
        user_id = user_obj.id

        app_user_obj.is_phone_verified = True
        app_user_obj.save()

        sub_dict = get_user_profile(user_id)
        user_obj.last_login = datetime.now()
        user_obj.save()

        data["code"] = 0
        data["error"] = False
        data["message"] = "Otp Verified."
        data["data"] = sub_dict
        return Response(data=data)
    else:
        data['code'] = 0
        data['message'] = "Otp either expired or invalid"
        data['error'] = True
        return Response(data=data)


@api_view(['POST'], )
def signup_details_view(request):
    data = {}
    if authentication_check(request) == True:
        user_id = get_id_from_auth(request)
        user_obj = User.objects.get(pk=user_id)
        app_user_obj = AppUser.objects.filter(user_id=user_id)[0]
        try:
            username = request.data["username"]
            if len(User.objects.filter(username=username)) > 0:
                data['code'] = 0
                data['message'] = "Username not available, Please first check username availability"
                data['error'] = True
                return Response(data=data)
            # if re.search("^(?=.{3,25}$)(?![_.])(?!.*[_.]{2})[a-zA-Z0-9._]+(?<![_.])$", request.data["username"]) == None:
            if re.search("^[a-zA-Z0-9_.]*$", request.data["username"]) == None:
                data['code'] = 0
                data[
                    'message'] = "Username should be 3-25 characters and should not contain special, capital, spaces charchter"
                data['error'] = True
                return Response(data=data)
            if re.search("^([\w\.\-]+)@([\w\-]+)((\.(\w){2,3})+)$", request.data["email"]) == None:
                data['code'] = 0
                data['message'] = "Send a valid Email"
                data['error'] = True
                return Response(data=data)
            if len(User.objects.filter(email=request.data["email"])) > 0:
                data['code'] = 0
                data['message'] = "Email already registered"
                data['error'] = True
                return Response(data=data)
            user_obj.first_name = request.data["name"]
            try:
                leg = request.data['leg']
                if leg not in ['R', "L"]:
                    data['code'] = 0
                    data['message'] = "Send a Valid leg"
                    data['error'] = True
                    return Response(data=data)
            except:
                data['code'] = 0
                data['message'] = "Please send leg."
                data['error'] = True
                return Response(data=data)
            if len(request.data["name"]) < 3:
                data['code'] = 0
                data['message'] = "Name should be of atleast 3 letters"
                data['error'] = True
                return Response(data=data)
            user_obj.username = username
            app_user_obj.username = username
            user_obj.email = request.data["email"]
            app_user_obj.date_of_birth = request.data["date_of_birth"]
            app_user_obj.gender = request.data["gender"]
            referral_code = request.data["referral_code"]
            app_user_obj.user_link = "http://" + settings.ALLOWED_HOSTS[1] + "/login_signup/view_user/" + \
                                     str(user_id)
            app_user_obj.is_profile_completed = True
            Y, M, D = request.data["date_of_birth"].split("-")
            birthday = datetime(int(Y), int(M), int(D), 12, 0, 0)
            app_user_obj.age = (datetime.now() - birthday).days // 365
        except:
            data['code'] = 0
            data[
                'message'] = "Please send all the details username, full_name, email, date_of_birth, gender, referral_code"
            data['error'] = True
            return Response(data=data)
        if len(referral_code) != 0:
            if ReferralId.objects.filter(referral_code=referral_code).count() == 0:
                data['code'] = 0
                data['message'] = "Invalid Referral Code"
                data['error'] = True
                return Response(data=data)
        try:
            user_obj.save()
        except:
            data['code'] = 0
            data['message'] = "Send a valid Email"
            data['error'] = True
            return Response(data=data)
        try:
            coin_managment_obj = CoinManagement.objects.filter(key='join')[0]
            UserCoins(sender=User.objects.filter(username="admin")[0], receiver=user_obj,
                      description=coin_managment_obj.key, coin_count=coin_managment_obj.value).do_transaction()

        except:
            data['code'] = 0
            data['message'] = "Failed to credit joining bonus"
            data['error'] = True
            return Response(data=data)

        if len(referral_code) != 0:
            try:
                refer_user(referral_code, user_obj)
            except:
                data['code'] = 0
                data['message'] = "Invalid referral code"
                data['error'] = True
                return Response(data=data)
        if True:
            DeviceInfo_obj = DeviceInfo.objects.filter(user_id=user_obj.id)[0]
            # print('yoyyo',app_user_obj.mobile_no,referral_code,request.data["date_of_birth"],DeviceInfo_obj.device_id,DeviceInfo_obj.device_token)
            create_referral_code(user_obj, app_user_obj.mobile_no, referral_code, DeviceInfo_obj.device_id,
                                 DeviceInfo_obj.device_token, request.data["date_of_birth"], leg)
        else:
            data['code'] = 0
            data['message'] = "Failed to create referral code"
            data['error'] = True
            return Response(data=data)
        #
        try:
            NotificationEmailSettings(user_id=user_obj).save()
        except:
            data['code'] = 0
            data['message'] = "Failed to create notification settings"
            data['error'] = True
            return Response(data=data)
        try:
            app_user_obj.save()
        except:
            data['code'] = 0
            data['message'] = "Please send date in YYYY-MM-DD format and gender as M or F"
            data['error'] = True
            return Response(data=data)
        genrate_and_register_new_token(username, user_id)
        user_data = get_user_profile(user_id)
        data['code'] = 0
        data['message'] = "Success"
        data['error'] = False
        data['data'] = user_data
        # os.mkdir(settings.MEDIA_ROOT + "/user_" + str(user_id))
        return Response(data=data)
    else:
        data['code'] = 0
        data['message'] = "Please provide proper authorization"
        data['error'] = True
        return Response(status=status.HTTP_401_UNAUTHORIZED, data=data)


@api_view(['POST'], )
def get_self_info_view(request):
    data = {}
    if authentication_check(request) is True:
        user_id = get_id_from_auth(request)
        sub_dict = get_user_profile(user_id)
        data['code'] = 0
        data['message'] = 'Success'
        data['error'] = False
        data['data'] = sub_dict
        return Response(data=data)
    else:
        data['code'] = 0
        data['error'] = True
        data['message'] = "Please provide proper authorization"
        return Response(status=status.HTTP_401_UNAUTHORIZED, data=data)


@api_view(['GET'], )
def view_user_view(request, user_id=None):
    data = {}
    if authentication_check(request) is True:
        try:
            user_obj = User.objects.get(pk=user_id)
            username = user_obj.username
        except:
            data['code'] = 0
            data['error'] = True
            data['message'] = "Sorry user dosen't exist or removed"
            return Response(data=data)
        if user_obj.is_active is False:
            data['code'] = 0
            data['error'] = True
            data['message'] = "Sorry user dosen't exist or removed"
            return Response(data=data)
        try:
            sub_data = {}
            self_user_id = get_id_from_auth(request)
            app_user_obj = AppUser.objects.get(user_id=user_obj)
            # user_obj = User.objects.filter(username=username)[0]
            # user_id = user_obj.id
            sub_data['user_id'] = user_id
            sub_data['cover_picture'] = "http://" + settings.ALLOWED_HOSTS[1] + "/media/" + \
                                        str(app_user_obj.cover_picture)
            sub_data['display_picture'] = "http://" + settings.ALLOWED_HOSTS[1] + "/media/" + \
                                          str(app_user_obj.display_picture)
            sub_data['name'] = user_obj.first_name
            sub_data['username'] = user_obj.username
            sub_data['roposo_tag'] = get_roposo_tag(user_id)
            sub_data['follower_count'] = get_followers_count(user_id)
            sub_data['following_count'] = get_followings_count(user_id)
            sub_data['bio'] = app_user_obj.about
            sub_data["city"] = app_user_obj.city
            sub_data["state"] = app_user_obj.state
            sub_data['location'] = app_user_obj.location
            sub_data['share'] = "http://" + settings.ALLOWED_HOSTS[1] + "/login_signup/view_user/" + str(
                user_id)
            sub_data['you_follow_this_user'] = check_if_you_follow_user(self_user_id=self_user_id, user_id=user_id)
            sub_data['this_user_follow_you'] = check_if_you_follow_user(self_user_id=user_id, user_id=self_user_id)
            sub_data['likes'] = 100
            data['code'] = 0
            data['error'] = False
            data['message'] = "Success"
            data['data'] = sub_data
        except:
            data['code'] = 0
            data['error'] = True
            data['message'] = "Something went wrong"
        return Response(data=data)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED,
                        data={"code": 0, "message": "Please provide proper authorization", 'error': True})


@api_view(['POST'], )
def get_followers_view(request):
    data = {}
    if authentication_check(request) is True:
        try:
            user_id = request.data['user_id']
        except:
            user_id = get_id_from_auth(request)
        try:
            time_stamp = datetime.fromtimestamp(int(request.data['time_stamp']) / 1000)
        except:
            data["code"] = 0
            data["error"] = True
            data["message"] = "Please send a valid time stamp"
            return Response(data=data)
        try:
            sub_data = []
            page_size = 20
            user_x_follower_objects = UserCrossFollower.objects.filter(user_id=user_id,
                                                                       followed_at__lt=time_stamp
                                                                       ).order_by('-followed_at')[:page_size]
            for follower in user_x_follower_objects:
                follower_obj = follower.followed_by
                follower_user = User.objects.get(pk=follower_obj.id)
                if follower_user.is_active is True:
                    follower_app_user = AppUser.objects.filter(user_id=follower_obj)[0]
                    data_obj = {}
                    data_obj["id"] = str(follower_obj.id)
                    data_obj["name"] = follower_user.first_name
                    data_obj["username"] = follower_user.username
                    data_obj["display_picture"] = "http://" + settings.ALLOWED_HOSTS[1] + \
                                                  "/media/" + \
                                                  str(follower_app_user.display_picture)
                    data_obj['you_follow_this_user'] = check_if_you_follow_user(self_user_id=user_id,
                                                                                user_id=follower_obj.id)

                    data_obj["profile_url"] = "http://" + settings.ALLOWED_HOSTS[1] + "/login_signup/view_user/" + str(
                        follower_obj.id)
                    data_obj["time_stamp"] = datetime.timestamp(follower.followed_at)
                    sub_data.append(data_obj)
            data["code"] = 0
            data["error"] = False
            data["message"] = "success"
            data['data'] = sub_data
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
def get_followings_view(request):
    data = {}
    if authentication_check(request) is True:
        try:
            user_id = request.data['user_id']
        except:
            user_id = get_id_from_auth(request)
        try:
            timestamp = datetime.fromtimestamp(int(request.data['time_stamp']) / 1000)
        except:
            data["code"] = 0
            data["error"] = True
            data["message"] = "Please send a valid time stamp"
            return Response(data=data)
        try:
            sub_data = []
            page_size = 20
            user_x_follower_objects = UserCrossFollower.objects.filter(followed_by=user_id,
                                                                       followed_at__lt=timestamp
                                                                       ).order_by('-followed_at')[:page_size]
            for user_x_follower_object in user_x_follower_objects:
                following_user_obj = user_x_follower_object.user_id
                if following_user_obj.is_active is True:
                    # following_user_obj = User.objects.get(pk=following_user_obj.id)
                    following_app_user_obj = AppUser.objects.filter(user_id=following_user_obj)[0]
                    data_obj = {}
                    data_obj["id"] = str(following_user_obj.id)
                    data_obj["name"] = following_user_obj.first_name
                    data_obj["username"] = following_user_obj.username
                    data_obj["display_picture"] = "http://" + settings.ALLOWED_HOSTS[1] + \
                                                  "/media/" + \
                                                  str(following_app_user_obj.display_picture)
                    data_obj["profile_url"] = following_app_user_obj.user_link
                    data_obj["time_stamp"] = datetime.timestamp(user_x_follower_object.followed_at)
                    sub_data.append(data_obj)
            data["code"] = 0
            data["error"] = False
            data["message"] = "Success"
            data['data'] = sub_data
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
def follow_unfollow_view(request):
    data = {}
    if authentication_check(request) is True:
        try:
            follow_user = request.data['follow_user']
            follower_user_obj = User.objects.get(pk=follow_user)
            app_user_obj = AppUser.objects.filter(user_id=follower_user_obj)[0]
            user_id = get_id_from_auth(request)
            user_obj = User.objects.get(pk=user_id)
        except:
            data["code"] = 0
            data["error"] = True
            data["message"] = "Please send a valid user_id"
            return Response(data=data)
        if follower_user_obj.is_active is False:
            data['code'] = 0
            data['error'] = True
            data['message'] = "Sorry user dosen't exist or removed"
            return Response(data=data)
        if follower_user_obj == user_obj:
            data['code'] = 0
            data['error'] = True
            data['message'] = "Sorry you can't follow yourself"
            return Response(data=data)
        if 1:
            user_x_follower_objs = UserCrossFollower.objects.filter(user_id=follower_user_obj, followed_by=user_obj)
            sub_data = {}
            if len(user_x_follower_objs) == 1:
                # try:
                notification_hist_obj = user_x_follower_objs[0].notification_id
                # except:
                #     pass
                user_x_follower_objs[0].delete()
                try:
                    notification_hist_obj.delete()
                except:
                    pass
                data["message"] = "follower deleted"
                #
                sub_data['cover_picture'] = "http://" + settings.ALLOWED_HOSTS[1] + "/media/" + \
                                            str(app_user_obj.cover_picture)
                sub_data['display_picture'] = "http://" + settings.ALLOWED_HOSTS[1] + "/media/" + \
                                              str(app_user_obj.display_picture)
                sub_data['name'] = follower_user_obj.first_name
                sub_data['username'] = follower_user_obj.username
                sub_data['roposo_tag'] = get_roposo_tag(follower_user_obj.id)
                sub_data['follower_count'] = get_followers_count(follower_user_obj.id)
                sub_data['following_count'] = get_followings_count(follower_user_obj.id)
                sub_data['bio'] = app_user_obj.about
                sub_data["city"] = app_user_obj.city
                sub_data["state"] = app_user_obj.state
                sub_data['location'] = app_user_obj.location
                sub_data['likes'] = 420
                sub_data['share'] = "http://" + settings.ALLOWED_HOSTS[1] + "/login_signup/view_user/" + str(
                    follower_user_obj.id)
                sub_data['you_follow_this_user'] = check_if_you_follow_user(self_user_id=user_id,
                                                                            user_id=follower_user_obj.id)
                #
                data['data'] = sub_data
            else:
                user_x_follower_obj = UserCrossFollower(user_id=follower_user_obj, followed_by=user_obj)
                user_x_follower_obj.save()
                data["message"] = "Follower created"
                #
                sub_data['cover_picture'] = "http://" + settings.ALLOWED_HOSTS[1] + "/media/" + \
                                            str(app_user_obj.cover_picture)
                sub_data['display_picture'] = "http://" + settings.ALLOWED_HOSTS[1] + "/media/" + \
                                              str(app_user_obj.display_picture)
                sub_data['name'] = follower_user_obj.first_name
                sub_data['username'] = follower_user_obj.username
                sub_data['roposo_tag'] = get_roposo_tag(follower_user_obj.id)
                sub_data['follower_count'] = get_followers_count(follower_user_obj.id)
                sub_data['following_count'] = get_followings_count(follower_user_obj.id)
                sub_data['bio'] = app_user_obj.about
                sub_data["city"] = app_user_obj.city
                sub_data["state"] = app_user_obj.state
                sub_data['likes'] = 420
                sub_data['location'] = app_user_obj.location
                sub_data['share'] = "http://" + settings.ALLOWED_HOSTS[1] + "/login_signup/view_user/" + str(
                    follower_user_obj.id)
                sub_data['you_follow_this_user'] = check_if_you_follow_user(self_user_id=user_id,
                                                                            user_id=follower_user_obj.id)
                #
                data['data'] = sub_data
                notification_msg = f'{user_obj.first_name} Followed you.'
                notification_obj = NotificationHistory(user_id=follower_user_obj, title='New follow',
                                                       message=notification_msg, type_id='follow ' + str(user_obj.id))
                notification_obj.save()
                user_x_follower_obj.notification_id = notification_obj
                user_x_follower_obj.save()
                token = DeviceInfo.objects.filter(user_id=follower_user_obj)[0]
                notification_setting = NotificationEmailSettings.objects.filter(user_id=follower_user_obj)[0]
                if token != "" and notification_setting.n_follows_me == True:
                    response = fcm_notifications(token.device_token, notification_msg, 'New follow', "notification")
            data["code"] = 0
            data["error"] = False
            return Response(data=data)
            # except:
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
def check_username_view(request):
    data = {}
    if authentication_check(request) is True:
        try:
            username = request.data['username']
        except:
            data["code"] = 0
            data["error"] = True
            data["message"] = "Please send a valid username"
            return Response(data=data)
        try:
            user_obj = User.objects.filter(username=username)
            if len(user_obj) == 1:
                data["message"] = "Username not available"
                data["error"] = True
            else:
                # if re.search("^(?=.{3,25}$)(?![_.])(?!.*[_.]{2})[a-zA-Z0-9._]+(?<![_.])$", username) == None:
                if re.search("^[a-zA-Z0-9_.]*$", username) == None:
                    data['code'] = 0
                    data[
                        'message'] = "Username should be 3-25 characters and should not contain special, capital, spaces charchter"
                    data['error'] = True
                    return Response(data=data)
                data["message"] = "Username available"
                data["error"] = False
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
def profile_update_view(request):
    data = {}
    if authentication_check(request) is True:
        user_id = get_id_from_auth(request)
        app_user_obj = AppUser.objects.filter(user_id=user_id)[0]
        user_obj = User.objects.filter(id=user_id)[0]
        try:
            name = request.data['name']
        except:
            name = user_obj.first_name
        try:
            gender = request.data['gender']
        except:
            gender = app_user_obj.gender
        try:
            username = request.data['username']
        except:
            username = 0
        try:
            bio = request.data['bio']
        except:
            bio = app_user_obj.about
        try:
            twitter = request.data['twitter']
        except:
            twitter = app_user_obj.twitter_handle
        try:
            website = request.data['website']
        except:
            website = app_user_obj.website
        try:
            cover_picture = request.FILES['cover_picture']
        except:
            cover_picture = 0
        try:
            display_picture = request.FILES['display_picture']
        except:
            display_picture = 0

        try:
            user_obj.first_name = name
            app_user_obj.gender = gender
            app_user_obj.about = bio
            app_user_obj.twitter_handle = twitter
            app_user_obj.website = website
            if cover_picture != 0:
                app_user_obj.cover_picture = cover_picture
            if display_picture != 0:
                app_user_obj.display_picture = display_picture

            try:
                if username == 0:
                    user_obj.save()
                    app_user_obj.save()
                    data['code'] = 0
                    data['data'] = get_user_profile(user_id)
                    data['message'] = "User profile is updated"
                    data['error'] = False
                    return Response(data=data)
                else:
                    user_obj.username = username
                    app_user_obj.username = username
                    user_obj.save()
                    app_user_obj.save()
                    data['code'] = 0
                    data['data'] = get_user_profile(user_id)
                    data['message'] = "User profile is updated"
                    data['error'] = False
                    return Response(data=data)
            except:
                data['code'] = 0
                data['message'] = "Username already exists"
                data['error'] = True
                return Response(data=data)
        except:
            data['code'] = 0
            data['message'] = "Somthing went wrong"
            data['error'] = True
            return Response(data=data)


@api_view(['POST'], )
def block_user_id_view(request):
    data = {}
    if authentication_check(request) is True:
        user_id = get_id_from_auth(request)
        user_obj = User.objects.get(pk=user_id)
        try:
            block_user = request.data['user_id']
            block_user_obj = User.objects.get(pk=block_user)
        except:
            data['code'] = 0
            data['message'] = "Provide a username"
            data['error'] = True
            return Response(data=data)
        try:
            if block_user_obj.is_active is True:
                if block_user_obj == user_obj:
                    data['code'] = 0
                    data['error'] = True
                    data['message'] = "Sorry you can't block yourself"
                    return Response(data=data)

                datacheck = UserXBlockedUser.objects.filter(user_id=block_user_obj, blocked_by=user_obj)
                if datacheck:
                    obj = datacheck[0]
                    obj.delete()
                    data['code'] = 0
                    data['message'] = "User unblocked"
                    data['error'] = False
                    return Response(data=data)
                else:
                    obj = UserXBlockedUser(user_id=block_user_obj, blocked_by=user_obj)
                    obj.save()
                    data['code'] = 0
                    data['message'] = "User blocked"
                    data['error'] = False
                    return Response(data=data)
            else:
                data['code'] = 0
                data['error'] = True
                data['message'] = "Sorry user dosen't exist or removed"
                return Response(data=data)
        except:
            data['code'] = 0
            data['message'] = "Some error occurred"
            data['error'] = True
            return Response(data=data)
    else:
        data["code"] = 0
        data["error"] = True
        data["message"] = "Please provide proper authorization"
        return Response(status=status.HTTP_401_UNAUTHORIZED, data=data)


@api_view(['POST'], )
def update_user_token_view(request):
    data = {}
    if authentication_check(request) == True:
        user_id = get_id_from_auth(request)
        try:
            token = request.headers["TOKEN"]
        except:
            data['code'] = 0
            data['message'] = "TOKEN not provided"
            data['error'] = True
            return Response(data=data)
        obj = DeviceInfo.objects.filter(user_id=user_id)
        obj.device_token = token
        obj.save()
        data['code'] = 0
        data['message'] = "Device token updated"
        data['error'] = False
        data['data'] = get_user_profile(user_id)
        return Response(data=data)
    else:
        data["code"] = 0
        data["error"] = True
        data["message"] = "Please provide proper authorization"
        return Response(status=status.HTTP_401_UNAUTHORIZED, data=data)


@api_view(['POST'], )
def get_blocked_user_list_view(request):
    data = {}
    if authentication_check(request) is True:
        user_id = get_id_from_auth(request)
        try:
            user_obj = User.objects.get(id=user_id)
            blocked_user_list = UserXBlockedUser.objects.filter(blocked_by_id=user_obj)
            subdata = []
            if blocked_user_list:
                for blocked_user in blocked_user_list:
                    blocked_user_obj = blocked_user.user_id
                    if blocked_user_obj.is_active is True:
                        blocked_app_user_obj = AppUser.objects.filter(user_id=blocked_user_obj.id)[0]
                        subdata.append({"name": blocked_user_obj.first_name, "display_picture":
                            "http://" + settings.ALLOWED_HOSTS[1] + "/media/" + str(
                                blocked_app_user_obj.display_picture)
                                           , "username": blocked_app_user_obj.username
                                           , 'user_id': blocked_user_obj.id})
                data['code'] = 0
                data['message'] = "Blocked user list"
                data['error'] = False
                data["data"] = subdata
                return Response(data)
            else:
                data['code'] = 0
                data['message'] = "No User blocked"
                data['error'] = True
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
        return Response(status=status.HTTP_401_UNAUTHORIZED, data=data)


@api_view(['POST'], )
def remove_photo_view(request):
    data = {}
    if authentication_check(request) is True:
        user_id = get_id_from_auth(request)
        user_obj = User.objects.get(id=user_id)
        app_user_obj = AppUser.objects.filter(user_id=user_obj)[0]
        try:
            photo_type = request.data['photo_type']
            if photo_type != 'd' and photo_type != 'c':
                data['code'] = 0
                data['message'] = "Please send 'd' or 'c' in photo_type attribute"
                data['error'] = True
                return Response(data=data)
        except:
            data['code'] = 0
            data['message'] = "Please provide a proper photo_type attribute"
            data['error'] = True
            return Response(data=data)
        try:
            if photo_type == 'd':
                app_user_obj.display_picture = 'defaults/display_picture.jpg'
                app_user_obj.save()
            elif photo_type == 'c':
                app_user_obj.cover_picture = 'defaults/cover_picture.jpg'
                app_user_obj.save()
            data['code'] = 0
            data['message'] = "Photo removed"
            data['error'] = False
            return Response(data)
        except:
            data['code'] = 0
            data['message'] = "Some error occurded"
            data['error'] = True
            return Response(data=data)
    else:
        data['code'] = 0
        data['message'] = "Authorization error"
        data['error'] = True
        return Response(status=status.HTTP_401_UNAUTHORIZED, data=data)


@api_view(['POST'], )
def search_user_view(request):
    data = {}
    if authentication_check(request) is True:
        try:
            start = int(request.data['start']) * 20
            search_query = request.data['search_query']
        except:
            data['code'] = 0
            data['message'] = "Please provide a proper start and search_query attribute"
            data['error'] = True
            return Response(data=data)
        try:
            self_user_id = get_id_from_auth(request)
            self_user_obj = User.objects.get(pk=self_user_id)
            user_obj_list = search_user(start=start, search_query=search_query, user_obj=self_user_obj)
            user_list = []
            for user_obj in user_obj_list:
                if user_obj != self_user_obj:
                    temp_dict = {}
                    temp_dict['name'] = user_obj.first_name
                    temp_dict['username'] = user_obj.username
                    temp_dict['id'] = user_obj.id
                    temp_dict['you follow this user'] = check_if_you_follow_user(self_user_id=self_user_obj,
                                                                                 user_id=user_obj)
                    try:
                        temp_dict['display_picture'] = "http://" + settings.ALLOWED_HOSTS[1] + "/media/" + \
                                                       str(AppUser.objects.filter(user_id=user_obj)[0].display_picture)
                    except:
                        continue
                    user_list.append(temp_dict)
            data['code'] = 0
            data['message'] = "User list"
            data['error'] = False
            data['data'] = user_list
            return Response(data)
        except:
            data['code'] = 0
            data['message'] = "Some error occurred"
            data['error'] = True
            return Response(data=data)
    else:
        data['code'] = 0
        data['message'] = "Authorization error"
        data['error'] = True
        return Response(status=status.HTTP_401_UNAUTHORIZED, data=data)


@api_view(['POST'], )
def delete_user_view(request):
    data = {}
    if authentication_check(request) is True:
        try:
            self_user_id = get_id_from_auth(request)
            self_user_obj = User.objects.get(pk=self_user_id)
            self_user_obj.is_active = False
            self_user_obj.save()
            data['code'] = 0
            data['message'] = "User deleted successfully"
            data['error'] = False
            data['data'] = ''
            return Response(data)
        except:
            data['code'] = 0
            data['message'] = "Some error occurred"
            data['error'] = True
            return Response(data=data)

    else:
        data['code'] = 0
        data['message'] = "Authorization error"
        data['error'] = True
        return Response(status=status.HTTP_401_UNAUTHORIZED, data=data)


@api_view(['POST'], )
def social_view(request):
    data = {}
    if authentication_check(request) is True:
        try:
            self_user_id = get_id_from_auth(request)
            user_obj = User.objects.get(id=self_user_id)
            try:
                facebook = bool(int(request.data['facebook']))
                facebook_id = request.data['facebook_id']
                google = bool(int(request.data['google']))
                google_id = request.data['google_id']
            except:
                data['code'] = 0
                data['message'] = "Please provide all details"
                data['error'] = True
                return Response(data=data)
            # if not facebook and not google:
            #     data['code'] = 0
            #     data['message'] = "Nothing to update"
            #     data['error'] = True
            #     return Response(data=data)
            if facebook:
                if facebook_id:
                    try:
                        obj = Social_Login(user_id=user_obj, facebook=facebook, facebook_id=facebook_id)
                        obj.save()

                    except:
                        social_obj = Social_Login.objects.get(user_id=self_user_id)
                        social_obj.facebook = facebook
                        social_obj.facebook_id = facebook_id
                        social_obj.save()
                else:
                    data['code'] = 0
                    data['message'] = "Please provide all details"
                    data['error'] = True
                    return Response(data=data)
            else:
                try:
                    obj = Social_Login(user_id=user_obj, facebook=facebook, facebook_id=facebook_id)
                    obj.save()

                except:
                    social_obj = Social_Login.objects.get(user_id=self_user_id)
                    social_obj.facebook = facebook
                    social_obj.facebook_id = facebook_id
                    social_obj.save()
            if google:
                if google_id:
                    try:
                        obj = Social_Login(user_id=user_obj, google=google, google_id=google_id)
                        obj.save()
                    except:
                        social_obj = Social_Login.objects.get(user_id=self_user_id)
                        social_obj.google = google
                        social_obj.google_id = google_id
                        social_obj.save()
                else:
                    data['code'] = 0
                    data['message'] = "Please provide all details"
                    data['error'] = True
                    return Response(data=data)
            else:
                try:
                    obj = Social_Login(user_id=user_obj, google=google, google_id=google_id)
                    obj.save()
                except:
                    social_obj = Social_Login.objects.get(user_id=self_user_id)
                    social_obj.google = google
                    social_obj.google_id = google_id
                    social_obj.save()

            data['code'] = 0
            data['message'] = "Social id saved successfully"
            data['error'] = False
            # data['data'] = {'facebook':facebook,
            # "google":google}
            return Response(data)
        except:
            data['code'] = 0
            data['message'] = "Some error occurred"
            data['error'] = True
            return Response(data=data)

    else:
        data['code'] = 0
        data['message'] = "Authorization error"
        data['error'] = True
        return Response(status=status.HTTP_401_UNAUTHORIZED, data=data)


@api_view(['POST'], )
def get_social_view(request):
    data = {}
    if authentication_check(request) is True:
        try:
            self_user_id = get_id_from_auth(request)
            user_obj = User.objects.get(id=self_user_id)
            social_obj = Social_Login.objects.filter(user_id=user_obj)[0]
            subdata = {}
            subdata['facebook'] = social_obj.facebook
            subdata['facebook_id'] = social_obj.facebook_id
            subdata['google'] = social_obj.google
            subdata['google_id'] = social_obj.google_id
            data['code'] = 0
            data['message'] = "Social id"
            data['error'] = False
            data['data'] = subdata
            return Response(data)
        except:
            data['code'] = 0
            data['message'] = "Not linked"
            data['error'] = False
            data['data'] = {
                "facebook": False,
                "facebook_id": None,
                "google": False,
                "google_id": None
            }

            return Response(data=data)

    else:
        data['code'] = 0
        data['message'] = "Authorization error"
        data['error'] = True
        return Response(status=status.HTTP_401_UNAUTHORIZED, data=data)


@api_view(['POST'], )
def resendOtp(request):
    data = {}
    try:
        LANG = request.headers["LANG"]
        DEVICEID = request.headers["DEVICEID"]
        DEVICEINFO = request.headers["DEVICEINFO"]
        APPINFO = request.headers["APPINFO"]
        DEVICETYPE = request.headers["DEVICETYPE"]
        TOKEN = request.headers["TOKEN"]

        mobile_no = request.POST.get('mobile_no')

        if mobile_no is None:
            data["code"] = 0
            data["error"] = True
            data["message"] = "Please enter mobile number"
            return Response(data=data)

        if mobile_no is None:
            data["code"] = 0
            data["error"] = True
            data["message"] = "Please enter mobile number"
            return Response(data=data)

        try:
            app_user_obj = AppUser.objects.filter(mobile_no=mobile_no)[0]
            user_obj = User.objects.get(pk=app_user_obj.user_id_id)
            otp = randint(100000, 999999)
            user_obj.password = hashers.make_password(otp)
            user_obj.save()
            app_user_obj.otp_time = time.time()
            app_user_obj.save()
            data["code"] = 0
            data["error"] = False
            data["message"] = "OTP Resend Successfully."
            data["otp"] = otp
            return Response(data=data)
        except Exception as error:
            data["code"] = 0
            data["error"] = True
            data["message"] = "This mobile number not registered with us."
            return Response(data=data)
    except Exception as error:
        print(str(error))
        data["code"] = 0
        data["error"] = True
        data["message"] = "Something went wrong!"
        return Response(data=data)

#
# @api_view(['POST'],)
# def create_email(request):
#     all_objects = User.objects.all()
#     for obj in all_objects:
#         obj.email = str(randint(100000000,999999999)) + "a@gmail.com"
#         obj.save()
#
#     data['code'] = 0
#     data['message'] = "Not linked"
#     data['error'] = False
#     data['data']=''
#     return Response(data=data)

# @api_view(['POST'],)
# def get_all_number(request):
#     data = {}
#     all_objects = AppUser.objects.all()
#     return_list = []
#     for obj in all_objects:
#         return_list.append(obj.mobile_no)
#     data['code'] = 0
#     data['message'] = "Not linked"
#     data['error'] = False
#     data['data']=return_list
#     return Response(data=data)
