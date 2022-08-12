from django.contrib import admin
from .models import ChannelList, Stars, StarManagement, ChannelXUser
from rangefilter.filter import DateRangeFilter
import datetime
from login_signup.models import *
from coins_and_gifts.models import *
from coins_and_gifts.class_and_functions import *
from django.contrib.admin import SimpleListFilter
from django_admin_listfilter_dropdown.filters import (
    DropdownFilter, ChoiceDropdownFilter, RelatedDropdownFilter)
from django.utils.html import format_html
from django.conf import settings


# Register your models here.
class CustomChannelList(admin.ModelAdmin):
    search_fields = ('channel_name',)
    list_display = ("channel_name", 'channel_description')


class CustomStars(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        star_user_obj = Stars.objects.get(id=obj.id)
        if star_user_obj.approved is False:
            if obj.approved is True:
                coin_management_obj = CoinManagement.objects.filter(key='star')[0]
                UserCoins(sender=User.objects.filter(username="admin")[0], receiver=star_user_obj.user_id,
                          description=coin_management_obj.key, coin_count=coin_management_obj.value).do_transaction()
        super().save_model(request, obj, form, change)

    def approve_star(modeladmin, request, queryset):
        for star_obj in queryset:
            star_obj.approved = True
            star_obj.approval_time = datetime.now()
            star_obj.save()
            user_obj = star_obj.user_id
            ChannelXUser(channel_id=None, user_id=user_obj).save()
            coin_management_obj = CoinManagement.objects.filter(key='star')[0]
            UserCoins(sender=User.objects.filter(username="admin")[0], receiver=user_obj,
                      description=coin_management_obj.key, coin_count=coin_management_obj.value).do_transaction()
    approve_star.short_description = "Approve"

    def remove_star(modeladmin, request, queryset):
        for star_obj in queryset:
            star_obj.approved = False
            star_obj.save()
            user_obj = star_obj.user_id
            ChannelXUser.objects.filter(user_id=user_obj)[0].delete()
    remove_star.short_description = "Disapprove"

    def user(self, obj):
        app_user = AppUser.objects.filter(user_id=obj.user_id)[0]
        return format_html('<a href="http://' + settings.ALLOWED_HOSTS[1] +
        '/admin/login_signup/appuser/{}/change/">{}</a>'.format(app_user.id, app_user.username))

    search_fields = ('user_id__username',)
    list_display = ("user", 'approved', 'approval_time')
    # readonly_fields = ("user_id", 'approval_time')
    list_filter = ('approved', ('approval_time', DateRangeFilter))
    actions = (approve_star, remove_star)


class CustomStarManagement(admin.ModelAdmin):
    list_display = ("key", 'value')


class ByChannel(SimpleListFilter):
    title = 'Channel' # or use _('country') for translated title
    parameter_name = 'channel_name'
    template = 'django_admin_listfilter_dropdown/dropdown_filter.html'

    def lookups(self, request, model_admin):
        tuple_list = []
        count = 0
        for channel in ChannelList.objects.all():
            channel_name = channel.channel_name
            tuple_list.append((str(count), channel_name))
            count += 1
        return tuple(tuple_list)

    def queryset(self, request, queryset):
        expected_value = self.value()
        if expected_value != None:
            includes = []
            channel_list = list(ChannelList.objects.all())
            channel = channel_list[int(expected_value)]
            for channel_user_obj in queryset:
                if channel_user_obj.channel_id.id == channel.id:
                    includes.append(channel_user_obj.id)
            return queryset.filter(pk__in=includes)
        else:
            return queryset



class ChannelXUserManagement(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def save_model(self, request, obj, form, change):
        channel_user_obj = ChannelXUser.objects.get(id=obj.id)
        if channel_user_obj.channel_id is None:
            if obj.channel_id is not None:
                obj.approved = True
                coin_management_obj = CoinManagement.objects.filter(key='channel_alloting')[0]
                UserCoins(sender=User.objects.filter(username="admin")[0], receiver=channel_user_obj.user_id,
                          description=coin_management_obj.key, coin_count=coin_management_obj.value).do_transaction()
        super().save_model(request, obj, form, change)

    def approve_star(modeladmin, request, queryset):
        for star_obj in queryset:
            star_obj.approved = True
            star_obj.approval_time = datetime.now()
            star_obj.save()
            # user_obj = star_obj.user_id
            # ChannelXUser(channel_id=None, user_id=user_obj).save()
            # coin_management_obj = CoinManagement.objects.filter(key='star')[0]
            # UserCoins(sender=User.objects.filter(username="admin")[0], receiver=user_obj,
            #           description=coin_management_obj.key, coin_count=coin_management_obj.value).do_transaction()
    approve_star.short_description = "Approve"

    def remove_star(modeladmin, request, queryset):
        for star_obj in queryset:
            star_obj.approved = False
            # star_obj.approval_time = None
            star_obj.save()
            # user_obj = star_obj.user_id
            # ChannelXUser.objects.filter(user_id=user_obj)[0].delete()
    remove_star.short_description = "Disapprove"
    def user_id(self, obj):
            return format_html('<a href="http://' + settings.ALLOWED_HOSTS[1] + '/admin/login_signup/appuser/{}/change/">{}</a>'.format(obj.user_id.id,obj.user_id.username))
    search_fields = ('user_id__username', 'channel_id__channel_name')
    list_display = ("user_id", 'channel_id', 'approved', 'approval_time')
    list_filter = (ByChannel, 'approved', ('approval_time', DateRangeFilter))
    readonly_fields = ('approval_time',)
    actions = (approve_star, remove_star)
    fieldsets = (
        ('Details', {
            'fields': ("channel_id", 'user_id', "approved", "approval_time",)
        }),
    )


admin.site.register(ChannelXUser, ChannelXUserManagement)
admin.site.register(ChannelList, CustomChannelList)
admin.site.register(Stars, CustomStars)
admin.site.register(StarManagement, CustomStarManagement)
