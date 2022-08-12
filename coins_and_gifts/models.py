from django.db import models
from django.contrib.auth.models import User
import os

class CoinTransactions(models.Model):
    class Meta:
        verbose_name_plural = "Coin Transactions"
    sender = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False, related_name="sender_id")
    receiver = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False, related_name="receiver_id")
    description = models.CharField(max_length=100, null=False)
    coin_count = models.IntegerField(null=False)
    sender_rem_balance = models.IntegerField(null=False)
    receiver_rem_balance = models.IntegerField(null=False)
    time_of_transaction = models.DateTimeField(auto_now_add=True)
    is_expired = models.BooleanField(default=False, null=False)


class CoinManagement(models.Model):
    class Meta:
        verbose_name_plural = "Coin Management"
    key = models.CharField(max_length=50, null=False)
    value = models.IntegerField(null=False)

    def __str__(self):
        return self.key


class GiftManagement(models.Model):
    class Meta:
        verbose_name_plural = "Gift Management"
    gift_name = models.CharField(max_length=50, null=False)
    gift = models.FileField(upload_to='gifts/', null=False)
    coin_cost = models.IntegerField(null=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.gift_name


class GiftTransactions(models.Model):
    class Meta:
        verbose_name_plural = "Gift Transactions"
    sender = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False, related_name="gift_sender")
    receiver = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False, related_name="gift_receiver")
    gift_id = models.ForeignKey(GiftManagement, on_delete=models.DO_NOTHING, null=False)
    attached_message = models.CharField(max_length=140, null=True, default=None)
    time_of_gifting = models.DateTimeField(auto_now_add=True)
    is_expired = models.BooleanField(default=False, null=False)


class AudioCategories(models.Model):
    class Meta:
        verbose_name_plural = "Audio Categories"

    def get_upload_path(instance, filename):
        return os.path.join("audio_categories", filename)

    audio_thumbnail = models.ImageField(null=True, upload_to=get_upload_path, default="audio_categories/default_audio.png")
    audio_category = models.CharField(max_length=40, null=False)
    description = models.CharField(max_length=140, null=False)

    def __str__(self):
        return self.audio_category


class AudioManagement(models.Model):
    class Meta:
        verbose_name_plural = "Audio Management"
    audio_name = models.CharField(max_length=50, null=False)
    audio = models.FileField(upload_to='audios/', null=False)
    coin_cost = models.IntegerField(null=False, default=0)
    audio_category = models.ForeignKey(AudioCategories, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.audio_name


class CoinRedeemTransaction(models.Model):
    class Meta:
        verbose_name_plural = "Coin Redeem Transactions"
    redeemed_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False)
    coin_amount = models.IntegerField(null=False)
    cash_amount = models.IntegerField(null=False)
    redeem_time = models.DateTimeField(auto_now_add=True)

class headingandpoints(models.Model):
    class Meta:
        verbose_name_plural = "Heading And Points"
    heading=models.CharField(max_length=100, null=False)
    points = models.CharField(max_length=500, null=False)


class ReferralId(models.Model):
    class Meta:
        verbose_name_plural = "Referral Code of Users"
    user = models.OneToOneField(User,on_delete=models.DO_NOTHING)
    referral_code = models.CharField(max_length=15, null=False)

    def __str__(self):
        return self.referral_code


class UserRefer(models.Model):
    class Meta:
        verbose_name_plural = "Referred User"
    referred_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="referred_by")
    referred = models.OneToOneField(User, on_delete=models.DO_NOTHING, related_name="referred")

    def __str__(self):
        return self.referred


class StickerManagement(models.Model):
    class Meta:
        verbose_name_plural = "Sticker Management"
    STICKER_CHOICES = (
        ('H', 'Hashtags'),
        ('C', 'Cities'),
        ('B', 'Badges'),
    )

    sticker_name = models.CharField(max_length=50, null=False)
    sticker = models.FileField(upload_to='stickers/', null=False)
    sticker_type = models.CharField(max_length=1, choices=STICKER_CHOICES, default="H")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.sticker_name

