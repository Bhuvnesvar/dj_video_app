from django.contrib import admin
from .models import *
from rangefilter.filter import DateRangeFilter
from django.utils.html import format_html
from login_signup.models import *
from django.utils.safestring import mark_safe
from django.conf import settings
from django_admin_listfilter_dropdown.filters import (
    DropdownFilter, ChoiceDropdownFilter, RelatedDropdownFilter
)
from django.forms import ValidationError
from django.contrib import messages
import os


class CoinTransactionsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def sender_user(self,obj):
        user_obj = obj.sender
        if user_obj.is_staff is True:
            return format_html('<a href="http://' + settings.ALLOWED_HOSTS[1] + '/admin/auth/user/{id}/change/" '
                               'target="_blank">{username}</a>'.format(id=user_obj.id, username=user_obj.username))
        else:
            return format_html('<a href="http://' + settings.ALLOWED_HOSTS[1] + '/admin/login_signup/appuser/{id}/change/" '
                               'target="_blank">{username}</a>'.format(
                id=AppUser.objects.filter(user_id=user_obj)[0].id, username=user_obj.username))

    def receiver_user(self, obj):
        user_obj = obj.receiver
        if user_obj.is_staff is True:
            return format_html('<a href="http://' + settings.ALLOWED_HOSTS[1] + '/admin/auth/user/{id}/change/" '
                               'target="_blank">{username}</a>'.format(id=user_obj.id, username=user_obj.username))
        else:
            return format_html('<a href="http://' + settings.ALLOWED_HOSTS[1] + '/admin/login_signup/appuser/{id}/change/" '
                               'target="_blank">{username}</a>'.format(
                id=AppUser.objects.filter(user_id=user_obj)[0].id, username=user_obj.username))

    search_fields = ('sender__username', 'receiver__username')
    list_display = ("sender_user", 'receiver_user', "description", 'coin_count', 'sender_rem_balance', 'receiver_rem_balance',
                    'time_of_transaction', 'is_expired')
    readonly_fields = ("sender", 'receiver', "description", 'coin_count', 'sender_rem_balance', 'receiver_rem_balance',
                       'time_of_transaction', 'is_expired')
    list_filter = ('is_expired', "description", ('time_of_transaction', DateRangeFilter),)


class AudioManagementAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False

    # def clean(self):
    #     try:
    #         if str(obj.audio).split(".")[-1] == "aac":
    #             pass
    #         else:
    #             raise ValidationError('Only .aac codec file supported')
    #     except IndexError:
    #         raise ValidationError('Only .aac codec file supported')

    def save_model(self, request, obj, form, change):
        try:
            if str(obj.audio).split(".")[-1] == "aac":
                super().save_model(request, obj, form, change)
            elif str(obj.audio).split(".")[-1] == "mp3":
                super().save_model(request, obj, form, change)
            elif str(obj.audio).split(".")[-1] == "wav":
                super().save_model(request, obj, form, change)
            else:
                pass
                messages.set_level(request, messages.ERROR)
                messages.error(request, 'Only .aac (Advanced Audio Coding),.mp3 and .wav files supported. please upload .aac audio formats.')
        except :
            messages.set_level(request, messages.ERROR)
            messages.error(request, 'Only .aac (Advanced Audio Coding),.mp3 and .wav files supported. please upload .aac audio formats.')

    search_fields = ('audio_name',)
    list_display = ("audio_name", 'audio', "audio_category", "is_active",)
    fieldsets = (
        ('Audio Details', {'fields': ("audio_name", 'audio', "audio_category", "is_active",)},),
    )
    list_filter = ("audio_category", "is_active",)


class AudioCategoryAdmin(admin.ModelAdmin):
    search_fields = ('audio_category',)
    list_display = ("audio_category", 'description')


class GiftManagementAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        try:
            if str(obj.gift).split(".")[-1] == "gif" or str(obj.gift).split(".")[-1] == "png":
                super().save_model(request, obj, form, change)
            else:
                pass
                messages.set_level(request, messages.ERROR)
                messages.error(request, 'Only .png or .gif file supported no jpg, mp4 etc. please upload .png or .gif image formats.')
        except :
            messages.set_level(request, messages.ERROR)
            messages.error(request, 'Only .png or .gif file supported no jpg, mp4 etc. please upload .png or .gif image formats.')

    def gift_image(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height="{height}" />'.format(
            url="http://" + settings.ALLOWED_HOSTS[1] + "/media/" + str(obj.gift),
            width=50,
            height=50,
        )
        )

    search_fields = ('gift_name',)
    list_display = ("gift_name", 'gift_image', "coin_cost")


class GiftTransactionsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def sender_user(self,obj):
        user_obj = obj.sender
        if user_obj.is_staff is True:
            return format_html('<a href="http://' + settings.ALLOWED_HOSTS[1] + '/admin/auth/user/{id}/change/" '
                               'target="_blank">{username}</a>'.format(id=user_obj.id, username=user_obj.username))
        else:
            return format_html('<a href="http://' + settings.ALLOWED_HOSTS[1] + '/admin/login_signup/appuser/{id}/change/" '
                               'target="_blank">{username}</a>'.format(
                id=AppUser.objects.filter(user_id=user_obj)[0].id, username=user_obj.username))

    def receiver_user(self, obj):
        user_obj = obj.receiver
        if user_obj.is_staff is True:
            return format_html('<a href="http://' + settings.ALLOWED_HOSTS[1] + '/admin/auth/user/{id}/change/" '
                               'target="_blank">{username}</a>'.format(id=user_obj.id, username=user_obj.username))
        else:
            return format_html('<a href="http://' + settings.ALLOWED_HOSTS[1] + '/admin/login_signup/appuser/{id}/change/" '
                               'target="_blank">{username}</a>'.format(
                id=AppUser.objects.filter(user_id=user_obj)[0].id, username=user_obj.username))

    def gift_image(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height="{height}" />'.format(
            url="http://" + settings.ALLOWED_HOSTS[1] + "/media/" + str(obj.gift_id.gift),
            width=50,
            height=50,
        )
        )

    search_fields = ('sender__username', 'receiver__username',)
    list_display = ('sender_user', 'receiver_user', "gift_image", "time_of_gifting")
    readonly_fields = ('sender_user', 'receiver_user', "gift_image", "attached_message", "time_of_gifting", "is_expired")
    list_filter = (("gift_id", RelatedDropdownFilter), ('time_of_gifting', DateRangeFilter))


class CoinManagementAdmin(admin.ModelAdmin):
    search_fields = ('key',)
    list_display = ("key", 'value')


class CoinRedeemTransactionAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    search_fields = ('redeemed_by__username',)
    list_display = ('redeemed_by', 'coin_amount', "cash_amount", "redeem_time",)
    readonly_fields = ('redeemed_by', 'coin_amount', "cash_amount", "redeem_time",)
    list_filter = (('redeem_time', DateRangeFilter),)


class headingandpointsAdmin(admin.ModelAdmin):


    # search_fields = ('redeemed_by__username',)
    list_display = ('heading', 'points',)
    # readonly_fields = ('redeemed_by', 'coin_amount', "cash_amount", "redeem_time",)
    # list_filter = (('redeem_time', DateRangeFilter),)


class ReferralIdAdmin(admin.ModelAdmin):
    def user_profile(self,obj):
        user_obj = obj.user
        if user_obj.is_staff is True:
            return format_html('<a href="http://' + settings.ALLOWED_HOSTS[1] + '/admin/auth/user/{id}/change/" '
                               'target="_blank">{username}</a>'.format(id=user_obj.id, username=user_obj.username))
        else:
            return format_html('<a href="http://' + settings.ALLOWED_HOSTS[1] + '/admin/login_signup/appuser/{id}/change/" '
                               'target="_blank">{username}</a>'.format(
                id=AppUser.objects.filter(user_id=user_obj)[0].id, username=user_obj.username))

    search_fields = ('user__username', 'user__first_name')
    list_display = ("user_profile", 'referral_code')
    readonly_fields = ("user_profile", 'referral_code')


class UserReferAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def referred_by_user(self,obj):
        user_obj = obj.referred_by
        if user_obj.is_staff is True:
            return format_html('<a href="http://' + settings.ALLOWED_HOSTS[1] + '/admin/auth/user/{id}/change/" '
                               'target="_blank">{username}</a>'.format(id=user_obj.id, username=user_obj.username))
        else:
            return format_html('<a href="http://' + settings.ALLOWED_HOSTS[1] + '/admin/login_signup/appuser/{id}/change/" '
                               'target="_blank">{username}</a>'.format(
                id=AppUser.objects.filter(user_id=user_obj)[0].id, username=user_obj.username))

    def referred_user(self,obj):
        user_obj = obj.referred
        if user_obj.is_staff is True:
            return format_html('<a href="http://' + settings.ALLOWED_HOSTS[1] + '/admin/auth/user/{id}/change/" '
                               'target="_blank">{username}</a>'.format(id=user_obj.id, username=user_obj.username))
        else:
            return format_html('<a href="http://' + settings.ALLOWED_HOSTS[1] + '/admin/login_signup/appuser/{id}/change/" '
                               'target="_blank">{username}</a>'.format(
                id=AppUser.objects.filter(user_id=user_obj)[0].id, username=user_obj.username))

    search_fields = ('referred_by__username', 'referred_by__first_name', 'referred__username', 'referred__first_name')
    list_display = ("referred_by_user", 'referred_user')
    readonly_fields = ("referred_by_user", 'referred_user')
    # list_filter = ("referred_by",)


class StickerManagementAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False

    def activate_sticker(modeladmin, request, queryset):
        for sticker_obj in queryset:
            sticker_obj.is_active = True
            sticker_obj.save()
    activate_sticker.short_description = "Activate/Undelete Sticker"

    def deactivate_sticker(modeladmin, request, queryset):
        for sticker_obj in queryset:
            sticker_obj.is_active = False
            sticker_obj.save()
    deactivate_sticker.short_description = "De-activate/Delete Sticker"

    def save_model(self, request, obj, form, change):
        try:
            if str(obj.sticker).split(".")[-1] == "gif" or str(obj.sticker).split(".")[-1] == "png":
                super().save_model(request, obj, form, change)
            else:
                pass
                messages.set_level(request, messages.ERROR)
                messages.error(request, 'Only .png or .gif file supported no jpg, mp4 etc. please upload .png or .gif image formats.')
        except :
            messages.set_level(request, messages.ERROR)
            messages.error(request, 'Only .png or .gif file supported no jpg, mp4 etc. please upload .png or .gif image formats.')

    def sticker_view(self, obj):
        if obj:
            return mark_safe('<img src="{url}" width="{width}" height="{height}" />'.format(
                url="http://" + settings.ALLOWED_HOSTS[1] + "/media/" + str(obj.sticker),
                width=100,
                height=100,
            )
            )
        else:
            return None

    readonly_fields = ('sticker_view',)
    fieldsets = (
        ('Sticker Details',
         {'fields': ("sticker_name", 'sticker_view', 'sticker', "sticker_type", "is_active",)}
         ,),
    )
    list_display = ("id", "sticker_name", 'sticker_view', "sticker_type", "is_active",)
    list_filter = ("is_active", "sticker_type",)
    search_fields = ("id", 'sticker_name',)
    actions = (activate_sticker, deactivate_sticker)



admin.site.register(UserRefer, UserReferAdmin)
admin.site.register(StickerManagement, StickerManagementAdmin)
admin.site.register(ReferralId, ReferralIdAdmin)
admin.site.register(CoinManagement, CoinManagementAdmin)
admin.site.register(GiftManagement, GiftManagementAdmin)
admin.site.register(GiftTransactions, GiftTransactionsAdmin)
admin.site.register(CoinTransactions, CoinTransactionsAdmin)
admin.site.register(CoinRedeemTransaction, CoinRedeemTransactionAdmin)
admin.site.register(AudioCategories, AudioCategoryAdmin)
admin.site.register(AudioManagement, AudioManagementAdmin)
admin.site.register(headingandpoints, headingandpointsAdmin)
