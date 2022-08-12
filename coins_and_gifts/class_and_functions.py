from .models import *
import time
from django.contrib.auth.models import User
from datetime import datetime
from django.db.models import Q
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table
from reportlab.platypus import TableStyle
from reportlab.lib import colors
from django.conf import settings
import os
import random
from django.conf import settings
import requests
from rest_framework.response import Response


def create_transaction_pdf(heading_table, data, filePath, fileName):
    pdf = SimpleDocTemplate(
        filePath + fileName,
        pagesize=letter
    )

    table = Table(data)
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.black),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
    ])

    table.setStyle(style)
    rowNumb = len(data)
    for i in range(1, rowNumb):
        if i % 2 == 0:
            bc = colors.lightblue
        else:
            bc = colors.white
        ts = TableStyle(
            [('BACKGROUND', (0, i), (-1, i), bc)]
        )
        table.setStyle(ts)

    ts = TableStyle(
        [
            ('BOX', (0, 0), (-1, -1), 2, colors.black),
            ('LINEBEFORE', (2, 1), (2, -1), 2, colors.red),
            ('LINEABOVE', (0, 2), (-1, 2), 2, colors.green),
            ('GRID', (0, 0), (-1, -1), 2, colors.black),
        ]
    )
    table.setStyle(ts)
    heading_style = TableStyle([
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 18),
    ])
    heading_table.setStyle(heading_style)
    elems = []
    elems.append(heading_table)
    elems.append(table)

    if len(data) == 1:
        elems.append(Table([["No transactions to show"]]))

    if fileName in os.listdir(filePath):
        os.remove(filePath + fileName)
    pdf.build(elems)


def append_temp_dict(transaction_history_list, sender, receiver, transaction_type, description, coin_count,
                     time_of_transaction, is_expired, gift_image=None):
    temp_dict = {}
    temp_dict['sender'] = sender
    temp_dict['receiver'] = receiver
    temp_dict['transaction_type'] = transaction_type
    temp_dict['description'] = description
    temp_dict['coin_count'] = coin_count
    temp_dict['time_of_transaction'] = time_of_transaction
    temp_dict['is_expired'] = is_expired
    temp_dict['gift_image'] = gift_image
    transaction_history_list.append(temp_dict)


class UserCoins:
    def __init__(self, user_id=None, sender=None, receiver=None, description=None, coin_count=None):
        self.user_id = user_id
        self.sender = sender
        self.receiver = receiver
        self.description = description
        self.coin_count = coin_count

    def get_transactions(self, start):
        page_size = 20
        transaction_history = CoinTransactions.objects.filter(Q(sender_id=self.user_id) |
                                                              Q(receiver_id=self.user_id)).order_by(
            '-time_of_transaction')
        transaction_history_list = []
        daily_activity_type = ["watch_video"]
        daily_post_type = ["post_video", "video_like", "video_view"]
        stored_day = None
        daily_activity = None
        post_activity = None
        for history_object in transaction_history:
            if history_object.time_of_transaction.day == stored_day:
                if history_object.description in daily_activity_type:
                    daily_activity += history_object.coin_count
                elif history_object.description in daily_post_type:
                    post_activity += history_object.coin_count
                elif history_object.description == "join":
                    append_temp_dict(transaction_history_list, history_object.sender.username,
                                     history_object.receiver.username,
                                     "credit", "Joining bonus", history_object.coin_count,
                                     history_object.time_of_transaction.strftime("%d-%b"), history_object.is_expired)
                elif history_object.description == "star":
                    append_temp_dict(transaction_history_list, history_object.sender.username,
                                     history_object.receiver.username,
                                     "credit", "Becoming star bonus", history_object.coin_count,
                                     history_object.time_of_transaction.strftime("%d-%b"), history_object.is_expired)
                elif history_object.description == "channel_alloting":
                    append_temp_dict(transaction_history_list, history_object.sender.username,
                                     history_object.receiver.username,
                                     "credit", "Channel alloting bonus", history_object.coin_count,
                                     history_object.time_of_transaction.strftime("%d-%b"), history_object.is_expired)
                elif "Gift" in history_object.description and history_object.sender.id == self.user_id:
                    try:
                        gift_transaction_obj = GiftTransactions.objects.get(
                            pk=history_object.description.split(" ")[-1])
                        gift_image = "http://" + settings.ALLOWED_HOSTS[1] + "/media/" + str(
                            gift_transaction_obj.gift_id.gift)
                        append_temp_dict(transaction_history_list, gift_transaction_obj.sender.username,
                                         gift_transaction_obj.receiver.username, "debit",
                                         "You given a " + gift_transaction_obj.gift_id.gift_name + " to " + gift_transaction_obj.receiver.first_name,
                                         history_object.coin_count,
                                         history_object.time_of_transaction.strftime("%d-%b"),
                                         history_object.is_expired, gift_image)
                    except:
                        pass
                elif "Gift" in history_object.description and history_object.receiver.id == self.user_id:
                    try:
                        gift_transaction_obj = GiftTransactions.objects.get(
                            pk=history_object.description.split(" ")[-1])
                        gift_image = "http://" + settings.ALLOWED_HOSTS[1] + "/media/" + str(
                            gift_transaction_obj.gift_id.gift)
                        append_temp_dict(transaction_history_list, gift_transaction_obj.sender.username,
                                         gift_transaction_obj.receiver.username, "debit",
                                         "You recieved a " + gift_transaction_obj.gift_id.gift_name + " to " + gift_transaction_obj.receiver.first_name,
                                         history_object.coin_count,
                                         history_object.time_of_transaction.strftime("%d-%b"),
                                         history_object.is_expired,
                                         gift_image)
                    except:
                        pass
            else:
                if stored_day != None:
                    if post_activity != 0:
                        append_temp_dict(transaction_history_list, history_object.sender.username,
                                         history_object.receiver.username,
                                         "credit", "Bonus coins based on your post activity", post_activity,
                                         history_object.time_of_transaction.strftime("%d-%b"),
                                         history_object.is_expired)
                    if daily_activity != 0:
                        append_temp_dict(transaction_history_list, history_object.sender.username,
                                         history_object.receiver.username,
                                         "credit", "Bonus coins based on your daily activity", daily_activity,
                                         history_object.time_of_transaction.strftime("%d-%b"),
                                         history_object.is_expired)
                daily_activity = 0
                post_activity = 0
                if history_object.description in daily_activity_type:
                    daily_activity += history_object.coin_count
                elif history_object.description in daily_post_type:
                    post_activity += history_object.coin_count
                elif history_object.description == "join":
                    append_temp_dict(transaction_history_list, history_object.sender.username,
                                     history_object.receiver.username,
                                     "credit", "Joining bonus", history_object.coin_count,
                                     history_object.time_of_transaction.strftime("%d-%b"), history_object.is_expired)
                elif history_object.description == "star":
                    append_temp_dict(transaction_history_list, history_object.sender.username,
                                     history_object.receiver.username,
                                     "credit", "Becoming star bonus", history_object.coin_count,
                                     history_object.time_of_transaction.strftime("%d-%b"), history_object.is_expired)
                elif history_object.description == "channel_alloting":
                    append_temp_dict(transaction_history_list, history_object.sender.username,
                                     history_object.receiver.username,
                                     "credit", "Channel alloting bonus", history_object.coin_count,
                                     history_object.time_of_transaction.strftime("%d-%b"), history_object.is_expired)
                elif "Gift" in history_object.description and history_object.sender.id == self.user_id:
                    try:
                        gift_transaction_obj = GiftTransactions.objects.get(
                            pk=history_object.description.split(" ")[-1])
                        gift_image = "http://" + settings.ALLOWED_HOSTS[1] + "/media/" + str(
                            gift_transaction_obj.gift_id.gift)
                        append_temp_dict(transaction_history_list, gift_transaction_obj.sender.username,
                                         gift_transaction_obj.receiver.username, "debit",
                                         "You given a " + gift_transaction_obj.gift_id.gift_name + " to " + gift_transaction_obj.receiver.first_name,
                                         history_object.coin_count,
                                         history_object.time_of_transaction.strftime("%d-%b"),
                                         history_object.is_expired,
                                         gift_image)
                    except:
                        pass
                elif "Gift" in history_object.description and history_object.receiver.id == self.user_id:
                    try:
                        gift_transaction_obj = GiftTransactions.objects.get(
                            pk=history_object.description.split(" ")[-1])
                        gift_image = "http://" + settings.ALLOWED_HOSTS[1] + "/media/" + str(
                            gift_transaction_obj.gift_id.gift)
                        append_temp_dict(transaction_history_list, gift_transaction_obj.sender.username,
                                         gift_transaction_obj.receiver.username, "debit",
                                         "You recieved a " + gift_transaction_obj.gift_id.gift_name + " to " + gift_transaction_obj.receiver.first_name,
                                         history_object.coin_count,
                                         history_object.time_of_transaction.strftime("%d-%b"),
                                         history_object.is_expired,
                                         gift_image)
                    except:
                        pass
                stored_day = history_object.time_of_transaction.day

        return transaction_history_list[start:start + page_size]

    def get_remaining_balance(self, timestamp):
        page_size = 1
        transaction_history = CoinTransactions.objects.filter(Q(sender_id=self.user_id) | Q(receiver_id=self.user_id)
                                                              & Q(time_of_transaction__lte=timestamp)).order_by(
            '-time_of_transaction')[:page_size]
        remaining_balance = 0
        if len(transaction_history) > 0:
            transaction_obj = transaction_history[0]
            if self.user_id == transaction_obj.sender.id:
                remaining_balance = transaction_obj.sender_rem_balance
            else:
                remaining_balance = transaction_obj.receiver_rem_balance
        return remaining_balance

    def do_transaction(self):
        if self.sender.username == 'admin':
            sender_rem_balance = 9999999
            receiver_rem_balance = UserCoins(user_id=self.receiver.id).get_remaining_balance(datetime.now())
            sender_rem_balance = 9999999
        else:
            sender_rem_balance = UserCoins(user_id=self.sender.id).get_remaining_balance(datetime.now())
            receiver_rem_balance = UserCoins(user_id=self.receiver.id).get_remaining_balance(datetime.now())
            sender_rem_balance = sender_rem_balance - self.coin_count
        if sender_rem_balance >= 0:
            receiver_rem_balance = receiver_rem_balance + self.coin_count
            CoinTransactions(sender=self.sender, receiver=self.receiver, description=self.description,
                             coin_count=self.coin_count, sender_rem_balance=sender_rem_balance,
                             receiver_rem_balance=receiver_rem_balance).save()
            return True
        else:
            return False

    def get_all_coin_transactions(self):
        transaction_history = CoinTransactions.objects.filter(Q(sender_id=self.user_id) | Q(receiver_id=self.user_id)
                                                              ).order_by('-time_of_transaction')
        transaction_table = []
        transaction_heading = ["Sender", "Receiver", "Description", "Coin Count", "Transaction Time", "Is Expired"]
        transaction_table.append(transaction_heading)
        for history_object in transaction_history:
            temp_data = [history_object.sender.username, history_object.receiver.username, history_object.description,
                         history_object.coin_count, history_object.time_of_transaction.strftime("%d-%b-%Y %H:%M:%S"),
                         history_object.is_expired]
            transaction_table.append(temp_data)

        heading_table = Table([["Coin Transactions of User"],
                               [],
                               []])
        filePath = settings.MEDIA_ROOT + "/user_" + str(self.user_id.id) + "/"
        fileName = "coin_transaction.pdf"
        create_transaction_pdf(heading_table=heading_table, data=transaction_table, filePath=filePath,
                               fileName=fileName)

    def get_all_redeemtions(self):
        transaction_history = CoinRedeemTransaction.objects.filter(redeemed_by=self.user_id).order_by('-redeem_time')
        transaction_table = []
        transaction_heading = ["Redeemed By", "Coin Amount", "Cash Amount", "Redeem Time"]
        transaction_table.append(transaction_heading)
        for history_object in transaction_history:
            temp_data = [history_object.redeemed_by.username, history_object.coin_amount,
                         str(history_object.cash_amount) + " ₹",
                         history_object.redeem_time.strftime("%d-%b-%Y %H:%M:%S")]
            transaction_table.append(temp_data)

        heading_table = Table([["Redeemtion History of User"],
                               [],
                               []])
        filePath = settings.MEDIA_ROOT + "/user_" + str(self.user_id.id) + "/"
        fileName = "redeemtion_history.pdf"
        create_transaction_pdf(heading_table=heading_table, data=transaction_table, filePath=filePath,
                               fileName=fileName)


def get_all_gifts():
    return GiftManagement.objects.filter(is_active=True)


def get_all_stickers(type):
    # page_size = 20
    return StickerManagement.objects.filter(is_active=True, sticker_type=type)


def create_referral_code(user_obj, mobile, referral, device_id, device_token, dob, leg):
    name = user_obj.first_name
    dob_n1 = dob.split('-')
    dob_n = dob_n1[1] + '/' + dob_n1[2] + '/' + dob_n1[0]
    format = {
        'Request': f'{{MethodName:"getregistration",MemberName:"{user_obj.first_name}", "Mobile":"{mobile}", "ReferralID":"{referral}","DeviceId":"{device_id}", "devicetoken":"{device_token}", "Email":"{user_obj.email}", "Password":"123456", "FatherName":"test father", "DOB":"{dob_n}", "Leg":"{leg}"}}'}
    print(format)
    data = requests.post(url=settings.MLM_BASE, data=format)
    print('data=', data.text)
    ref = eval(data.text)
    print(ref)
    try:
        referral_code = ref['data']['refferal']
    except:
        data = {}
        data['code'] = 0
        data['message'] = "Failed to create referral code"
        data['error'] = True
        return Response(data=data)
    try:
        # referral_code = name.split(" ")[0][0:4].upper() + str(random.randint(1,9999))
        if len(ReferralId.objects.filter(referral_code=referral_code)) > 0:
            create_referral_code(user_obj, mobile, referral, device_id, device_token, dob, leg)
        else:
            ReferralId(user=user_obj, referral_code=referral_code).save()
    except:
        # referral_code = name[0:4].upper() + str(random.randint(1,9999))
        if len(ReferralId.objects.filter(referral_code=referral_code)) > 0:
            create_referral_code(user_obj, mobile, referral, device_id, device_token, dob, leg)
        else:
            ReferralId(user=user_obj, referral_code=referral_code).save()


def refer_user(referral_code, user_obj):
    referred_by = ReferralId.objects.filter(referral_code=referral_code)[0].user
    UserRefer(referred_by=referred_by, referred=user_obj).save()
    if referred_by.is_active == 1:
        coin_managment_obj = CoinManagement.objects.filter(key='friend_join')[0]
        UserCoins(sender=User.objects.filter(username="admin")[0], receiver=referred_by,
                  description=coin_managment_obj.key, coin_count=coin_managment_obj.value).do_transaction()
    coin_managment_obj = CoinManagement.objects.filter(key='friend_join')[0]
    UserCoins(sender=User.objects.filter(username="admin")[0], receiver=user_obj,
              description=coin_managment_obj.key, coin_count=coin_managment_obj.value).do_transaction()


