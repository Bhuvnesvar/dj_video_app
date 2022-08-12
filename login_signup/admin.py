from django.contrib import admin
from .models import AppUser, UserCrossFollower
from django.contrib.auth.models import User
from rangefilter.filter import DateRangeFilter
from .models import *
from django.utils.safestring import mark_safe
from django.conf import settings
from star_and_channels.class_and_functions import *
from reported.class_and_functions import *
from coins_and_gifts.class_and_functions import *
from video.class_and_functions import *
from .class_and_functions import *
from datetime import datetime
from django.utils.html import format_html
from django.contrib.auth import hashers
from django.contrib.admin import SimpleListFilter
from django_admin_listfilter_dropdown.filters import (DropdownFilter, ChoiceDropdownFilter, RelatedDropdownFilter)
from django.contrib.admin.sites import AdminSite
from django.utils.translation import ugettext_lazy
from django.http import HttpResponseRedirect

admin.site.site_header = "AZARO Admin Panel"
admin.site.site_title = "AZARO"
admin.site.index_title = "Welcome to AZARO Admin Panel"


class is_star_filter(SimpleListFilter):
    title = 'Is Star'  # or use _('country') for translated title
    parameter_name = 'star'

    def lookups(self, request, model_admin):
        return (
            (True, 'Star'),
            (False, 'Not Star')
        )

    def queryset(self, request, queryset):
        expected_value = self.value()
        excludes = []
        for app_user_obj in queryset:
            if expected_value != None:
                if str(check_is_star(app_user_obj.user_id)) != expected_value:
                    excludes.append(app_user_obj.id)
            return queryset.exclude(pk__in=excludes)


class Social_filter(SimpleListFilter):
    title = 'Social Link'  # or use _('country') for translated title
    parameter_name = 'social'

    def lookups(self, request, model_admin):
        return (
            ('Facebook', 'Facebook'),
            ('Google', 'Google'),
            ('Both', 'Both'),
        )

    def queryset(self, request, queryset):
        expected_value = self.value()
        excludes = []
        for app_user_obj in queryset:
            if expected_value != None:
                if expected_value == "Facebook":
                    usr_obj = app_user_obj.user_id
                    try:
                        obj = Social_Login.objects.filter(user_id=usr_obj)[0]
                        if obj.facebook is not True:
                            excludes.append(app_user_obj.id)
                    except:
                        excludes.append(app_user_obj.id)
                if expected_value == "Google":
                    usr_obj = app_user_obj.user_id
                    try:
                        obj = Social_Login.objects.filter(user_id=usr_obj)[0]
                        if obj.google is not True:
                            excludes.append(app_user_obj.id)
                    except:
                        excludes.append(app_user_obj.id)
                if expected_value == "Both":
                    usr_obj = app_user_obj.user_id
                    try:
                        obj = Social_Login.objects.filter(user_id=usr_obj)[0]
                        if obj.google is not True and obj.facebook is not True:
                            excludes.append(app_user_obj.id)
                    except:
                        excludes.append(app_user_obj.id)
        return queryset.exclude(pk__in=excludes)


class is_active_filter(SimpleListFilter):
    title = 'Active/Inactive(deleted)'  # or use _('country') for translated title
    parameter_name = 'active'

    def lookups(self, request, model_admin):
        return (
            (True, 'Active'),
            (False, 'Deleted')
        )

    def queryset(self, request, queryset):
        expected_value = self.value()
        excludes = []
        for app_user_obj in queryset:
            if expected_value != None:
                user_obj = User.objects.get(id=app_user_obj.user_id_id)
                if str(user_obj.is_active) != expected_value:
                    excludes.append(app_user_obj.id)
        return queryset.exclude(pk__in=excludes)


class age_filter(SimpleListFilter):
    title = 'Age Group'  # or use _('country') for translated title
    parameter_name = 'age_group'

    def lookups(self, request, model_admin):
        return (
            ('1', '<16'),
            ('2', '16-20'),
            ('3', '21-30'),
            ('4', '31-50'),
            ('5', '>50')
        )

    def queryset(self, request, queryset):
        expected_value = self.value()
        excludes = []
        if expected_value != None:
            for app_user_obj in queryset:
                if app_user_obj.age != None:
                    if app_user_obj.age < 16 and expected_value == '1':
                        excludes.append(app_user_obj.id)
                    elif app_user_obj.age > 16 and app_user_obj.age < 21 and expected_value == '2':
                        excludes.append(app_user_obj.id)
                    elif app_user_obj.age > 20 and app_user_obj.age < 31 and expected_value == '3':
                        excludes.append(app_user_obj.id)
                    elif app_user_obj.age > 30 and app_user_obj.age < 51 and expected_value == '4':
                        excludes.append(app_user_obj.id)
                    elif app_user_obj.age > 50 and expected_value == '5':
                        excludes.append(app_user_obj.id)
            return queryset.filter(pk__in=excludes)
        else:
            return queryset


class AppUserAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def name(self, obj):
        return obj.user_id.first_name

    def change_active_status(self, obj):
        return format_html(
            '<a href="http://' + settings.ALLOWED_HOSTS[
                1] + '/admin/auth/user/{}/change/" target="_blank">click here</a> to block '
                     'the user which is equivalent to deleting the user.'.format(obj.user_id_id))

    def followers(self, obj):
        user_obj = User.objects.get(id=obj.user_id_id)
        return format_html(
            '<a href="http://' + settings.ALLOWED_HOSTS[
                1] + '/admin/login_signup/usercrossfollower/?user_id__id__exact={}">{}</a>'
            .format(user_obj.id, get_followers_count(user_obj)))

    def Referral_Id(self, obj):
        user_obj = User.objects.get(id=obj.user_id_id)
        ref_obj = ReferralId.objects.get(user=user_obj)
        try:
            return ref_obj.referral_code
        except:
            return False

    def Referral_Count(self, obj):
        user_obj = User.objects.get(id=obj.user_id_id)
        ref_obj = UserRefer.objects.filter(referred_by=user_obj).count()
        return format_html(
            '<a href="http://' + settings.ALLOWED_HOSTS[1] +
            '/admin/coins_and_gifts/userrefer/?referred_by__id__exact={}">{}</a>'.format(user_obj.id, ref_obj))

    def followings(self, obj):
        user_obj = User.objects.get(id=obj.user_id_id)
        return format_html(
            '<a href="http://' + settings.ALLOWED_HOSTS[
                1] + '/admin/login_signup/usercrossfollower/?followed_by__id__exact={}">{}</a>'
            .format(user_obj.id, get_followings_count(user_obj)))

    def user_who_blocked_this_user(self, obj):
        user_obj = User.objects.get(id=obj.user_id_id)
        return format_html(
            '<a href="http://' + settings.ALLOWED_HOSTS[
                1] + '/admin/login_signup/userxblockeduser/?user_id__id__exact={}">{}</a>'
            .format(user_obj.id, get_blocked_user_count(user_obj)))

    #
    def videos_viewed_by_this_user(self, obj):
        user_obj = obj.user_id
        return format_html(
            '<a href="http://' + settings.ALLOWED_HOSTS[
                1] + '/admin/video/mediaxlikexviews/?viewed_by__id__exact={}">{}</a>'
            .format(user_obj.id, viewed_by_count(user_obj)))

    def videos_liked_by_this_user(self, obj):
        user_obj = obj.user_id
        return format_html(
            '<a href="http://' + settings.ALLOWED_HOSTS[
                1] + '/admin/video/mediaxlikexviews/?viewed_by__id__exact={}&liked=true">{}</a>'
            .format(user_obj.id, liked_by_count(user_obj)))

    def videos_commented_by_this_user(self, obj):
        user_obj = obj.user_id
        return format_html(
            '<a href="http://' + settings.ALLOWED_HOSTS[1] + '/admin/video/comments/?commented_by__id__exact={}">{}</a>'
            .format(user_obj.id, commented_by_count(user_obj)))

    #

    def user_blocked_by_this_user(self, obj):
        user_obj = User.objects.get(id=obj.user_id_id)
        return format_html(
            '<a href="http://' + settings.ALLOWED_HOSTS[
                1] + '/admin/login_signup/userxblockeduser/?blocked_by__id__exact={}">{}</a>'
            .format(user_obj.id, get_blocked_by_count(user_obj)))

    def user_reports(self, obj):
        user_obj = User.objects.get(id=obj.user_id_id)
        return format_html(
            '<a href="http://' + settings.ALLOWED_HOSTS[
                1] + '/admin/reported/userreporthistory/?reported_user__id__exact={}">{}</a>'
            .format(user_obj.id, get_self_report_count(user_obj)))

    def video_reports(self, obj):
        user_obj = User.objects.get(id=obj.user_id_id)
        return format_html(
            '<a href="http://' + settings.ALLOWED_HOSTS[
                1] + '/admin/reported/postreporthistory/?post__user_id__id={}">{}</a>'
            .format(user_obj.id, get_video_report_count(user_obj)))

    def is_active(self, obj):
        usr_obj = User.objects.get(id=obj.user_id_id)
        return usr_obj.is_active

    def mail(self, obj):
        usr_obj = User.objects.get(id=obj.user_id_id)
        return usr_obj.email

    def is_star(self, obj):
        usr_obj = User.objects.get(id=obj.user_id_id)
        return check_is_star(usr_obj)

    def number_of_videos(self, obj):
        user_obj = User.objects.get(id=obj.user_id_id)
        return format_html(
            '<a href="http://' + settings.ALLOWED_HOSTS[
                1] + '/admin/video/mediatable/?user_id__exact={}">{}</a>'.format(user_obj.id,
                                                                                 get_video_count(user_obj)))

    def total_likes(self, obj):
        user_obj = User.objects.get(id=obj.user_id_id)
        return get_user_like_count(user_obj)

    def total_views(self, obj):
        user_obj = User.objects.get(id=obj.user_id_id)
        return get_user_view_count(user_obj)

    def coin_balance(self, obj):
        usr_obj = User.objects.get(id=obj.user_id_id)
        user_coin_obj = UserCoins(user_id=usr_obj)
        user_coin_obj.get_all_coin_transactions()
        return format_html(
            '<a href="http://' + settings.ALLOWED_HOSTS[
                1] + '/media/user_{id}/coin_transaction.pdf" target="_blank">{rem_bal}'
                     '</a>'.format(id=usr_obj.id,
                                   rem_bal=UserCoins(user_id=usr_obj).get_remaining_balance(datetime.now())))

    def money_balance(self, obj):
        usr_obj = User.objects.get(id=obj.user_id_id)
        return str(UserCoins(user_id=usr_obj).get_remaining_balance(datetime.now()) / 1000) + " ₹"

    def facebook(self, obj):
        usr_obj = User.objects.get(id=obj.user_id_id)
        try:
            obj = Social_Login.objects.filter(user_id=usr_obj)[0]
            return bool(obj.facebook)
        except:
            return None

    def google(self, obj):
        usr_obj = User.objects.get(id=obj.user_id_id)
        try:
            obj = Social_Login.objects.filter(user_id=usr_obj)[0]
            return bool(obj.google)
        except:
            return None

    def redeemtion_history(self, obj):
        usr_obj = User.objects.get(id=obj.user_id_id)
        user_coin_obj = UserCoins(user_id=obj.user_id)
        user_coin_obj.get_all_redeemtions()
        return format_html(
            '<a href="http://' + settings.ALLOWED_HOSTS[
                1] + '/media/user_{id}/redeemtion_history.pdf" target="_blank">click here'
                     '</a>'.format(id=usr_obj.id))

    def channel(self, obj):
        user_obj = User.objects.get(id=obj.user_id_id)
        return get_category(user_obj)

    def display_photo(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height="{height}" />'.format(
            url="http://" + settings.ALLOWED_HOSTS[1] + "/media/" + str(obj.display_picture),
            width=100,
            height=100,
        )
        )

    def cover_photo(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height="{height}" />'.format(
            url="http://" + settings.ALLOWED_HOSTS[1] + "/media/" + str(obj.cover_picture),
            width=250,
            height=100,
        )
        )

    def username_(self, obj):
        if len(obj.username) > 16:
            return mark_safe('<a href={url}>{username}</a>'.format(
                url="http://" + settings.ALLOWED_HOSTS[1] + "/admin/login_signup/appuser/" + str(obj.id) + "/change/",
                username=obj.username[:13] + "..."))
        return mark_safe('<a href={url}>{username}</a>'.format(
            url="http://" + settings.ALLOWED_HOSTS[1] + "/admin/login_signup/appuser/" + str(obj.id) + "/change/",
            username=obj.username))

    def block_user(modeladmin, request, queryset):
        for app_user_obj in queryset:
            user_obj = User.objects.filter(username=app_user_obj.username)[0]
            user_obj.is_active = False
            user_obj.save()

    block_user.short_description = "Block these users"

    def unblock_user(modeladmin, request, queryset):
        for app_user_obj in queryset:
            user_obj = User.objects.filter(username=app_user_obj.username)[0]
            user_obj.is_active = True
            user_obj.save()

    unblock_user.short_description = "Unblock these users"

    def response_change(self, request, obj, post_url_continue=None):
        """
        This makes the response go to the newly created
        model's change page without using reverse
        """
        if obj.id is not None:
            user_obj = User.objects.get(id=obj.user_id.id)
            if user_obj.username != obj.mobile_no:
                print("MOBILE CHANGE " + str(user_obj.username) + " " + str(obj.mobile_no))
                user_obj.username = obj.mobile_no
                user_obj.save()
            else:
                print("MOBILE NOT CHANGE " + str(user_obj.username) + " " + str(obj.mobile_no))

        return HttpResponseRedirect(redirect_to="http://" + settings.ALLOWED_HOSTS[1] + "/admin/login_signup/appuser/")

    search_fields = ('username', 'user_id__first_name')
    is_active.boolean = True
    is_star.boolean = True

    readonly_fields = ("username", 'name', "display_photo", "cover_photo", "about", 'gender', "city",
                       'date_of_birth', 'state', "address", "twitter_handle", "user_link", "location", 'website',
                       'is_star', 'channel', 'is_active', 'mail', 'coin_balance', 'money_balance', 'number_of_videos'
                       , 'total_likes', 'total_views', "followers", 'followings', "user_blocked_by_this_user",
                       'user_who_blocked_this_user', "user_reports", 'video_reports', 'redeemtion_history',
                       'change_active_status', "videos_commented_by_this_user", "videos_liked_by_this_user",
                       "videos_viewed_by_this_user", 'Referral_Id', 'Referral_Count')

    def get_readonly_fields(self, request, obj=AppUser):
        if obj.is_phone_verified == True:
            return ("username", 'name', "display_photo", "cover_photo", "about", 'gender', "city",
                    'date_of_birth', 'state', "address", "twitter_handle", "user_link", "location", 'website',
                    'is_star', 'channel', 'is_active', 'mail', 'coin_balance', 'money_balance', 'number_of_videos'
                    , 'total_likes', 'total_views', "followers", 'followings', "user_blocked_by_this_user",
                    'user_who_blocked_this_user', "user_reports", 'video_reports', 'redeemtion_history',
                    'change_active_status', "videos_commented_by_this_user", "videos_liked_by_this_user",
                    "videos_viewed_by_this_user", 'Referral_Id', 'Referral_Count',)
        else:
            return super(AppUserAdmin, self).get_readonly_fields(request, obj)

    fieldsets = (
        ('Basic Details', {
            'fields': (("username", 'name', 'mail', "mobile_no", 'is_phone_verified'),
                       ("display_photo", "cover_photo"),
                       "about",
                       ('date_of_birth', 'gender', "city", 'state', 'is_star', 'channel', 'is_active',
                        'change_active_status'),)
        }),
        ('More Details', {
            'classes': ('collapse',),
            'fields': ("address", "twitter_handle", "user_link", "location", 'website'),
        }),
        ('Coin Details', {
            'classes': ('collapse',),
            'fields': ("coin_balance", 'money_balance', 'redeemtion_history',),
        }),
        ('Video Details', {
            'classes': ('collapse',),
            'fields': (("number_of_videos", "videos_viewed_by_this_user"),
                       ('total_likes', "videos_liked_by_this_user"),
                       ('total_views', "videos_commented_by_this_user"),),
        }),
        ('Follower and Following Details', {
            'classes': ('collapse',),
            'fields': ("followers", 'followings',),
        }),
        ('Referral Details', {
            'classes': ('collapse',),
            'fields': ('Referral_Id', 'Referral_Count'),
        }),
        ('Blocked User and Blocked By User Details', {
            'classes': ('collapse',),
            'fields': ("user_blocked_by_this_user", 'user_who_blocked_this_user',),
        }),
        ('Report Details', {
            'classes': ('collapse',),
            'fields': ("user_reports", 'video_reports',),
        }),
    )
    list_filter = (
        is_star_filter, is_active_filter, age_filter, 'gender', ("city", DropdownFilter), ('state', DropdownFilter),
        ('date_joined', DateRangeFilter), Social_filter)
    list_display = (
        "username_", "name", 'gender', 'age', "city", 'state', 'date_joined', 'is_phone_verified', 'is_active',
        'facebook',
        'google')
    actions = (block_user, unblock_user)


class CustomUserAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        # if obj.id is not None:
        #     user_obj = User.objects.get(id=obj.id)
        #     video_obj_list = get_all_videos(user_obj)
        #     if user_obj.is_active is True:
        #         if obj.is_active is False:
        #             app_user_obj = AppUser.objects.filter(user_id=obj)[0]
        #             obj.username = "[deleted_user]" + obj.username
        #             app_user_obj.username = "[deleted_user]" + app_user_obj.username
        #             app_user_obj.mobile_no = "[deleted_user]" + app_user_obj.mobile_no
        #             app_user_obj.save()
        #             for video_obj in video_obj_list:
        #                 video_obj.is_available = False
        #                 video_obj.save()
        #     else:
        #         if obj.is_active is True:
        #             app_user_obj = AppUser.objects.filter(user_id=obj)[0]
        #             obj.username = obj.username.split("[deleted_user]")[-1]
        #             app_user_obj.username = app_user_obj.username.split("[deleted_user]")[-1]
        #             app_user_obj.mobile_no = app_user_obj.mobile_no.split("[deleted_user]")[-1]
        #             app_user_obj.save()
        #             for video_obj in video_obj_list:
        #                 video_obj.is_available = True
        #                 video_obj.save()
        if obj.id is not None:
            user_obj = User.objects.get(id=obj.id)
            video_obj_list = get_all_videos(user_obj)
            if user_obj.is_active is True:
                if obj.is_active is False:
                    for video_obj in video_obj_list:
                        video_obj.is_available = False
                        video_obj.save()
            else:
                if obj.is_active is True:
                    for video_obj in video_obj_list:
                        video_obj.is_available = True
                        video_obj.save()
            if user_obj.password != obj.password:
                obj.password = hashers.make_password(obj.password)
        else:
            obj.password = hashers.make_password(obj.password)
        super().save_model(request, obj, form, change)

    def has_delete_permission(self, request, obj=None):
        return False

    def redeemtion_history(self, usr_obj):
        # usr_obj = User.objects.get(id=obj.user_id_id)
        user_coin_obj = UserCoins(user_id=usr_obj)
        try:
            user_coin_obj.get_all_redeemtions()
        except:
            return None
        return format_html(
            '<a href="http://' + settings.ALLOWED_HOSTS[
                1] + '/media/user_{id}/redeemtion_history.pdf" target="_blank">click here'
                     '</a>'.format(id=usr_obj.id))

    def coin_balance(self, usr_obj):
        # usr_obj = User.objects.get(id=obj.user_id_id)
        user_coin_obj = UserCoins(user_id=usr_obj)
        try:
            user_coin_obj.get_all_coin_transactions()
        except:
            return None
        return format_html(
            '<a href="http://' + settings.ALLOWED_HOSTS[
                1] + '/media/user_{id}/coin_transaction.pdf" target="_blank">{rem_bal}'
                     '</a>'.format(id=usr_obj.id,
                                   rem_bal=UserCoins(user_id=usr_obj).get_remaining_balance(datetime.now())))

    def profile_link(self, user_obj):
        try:
            app_user_obj = AppUser.objects.filter(user_id=user_obj)[0]
            return format_html(
                '<a href="http://' + settings.ALLOWED_HOSTS[
                    1] + '/admin/login_signup/appuser/{id}/change/" target="_blank">View Profile'
                         '</a>'.format(id=app_user_obj.id))
        except:
            return None

    def block_user(self, request, queryset):
        for user_obj in queryset:
            if user_obj.is_active is True:
                # app_user_obj = AppUser.objects.filter(user_id=user_obj)[0]
                # user_obj.username = "[deleted_user]" + user_obj.username
                # app_user_obj.username = "[deleted_user]" + app_user_obj.username
                # app_user_obj.mobile_no = "[deleted_user]" + app_user_obj.mobile_no
                video_obj_list = get_all_videos(user_obj)
                for video_obj in video_obj_list:
                    video_obj.is_available = False
                    video_obj.save()
                user_obj.is_active = False
                user_obj.save()
                # app_user_obj.save()

    block_user.short_description = "Delete these users"

    def unblock_user(self, request, queryset):
        for user_obj in queryset:
            if user_obj.is_active is False:
                # app_user_obj = AppUser.objects.filter(user_id=user_obj)[0]
                # user_obj.username = user_obj.username.split("[deleted_user]")[-1]
                # app_user_obj.username = app_user_obj.username.split("[deleted_user]")[-1]
                # app_user_obj.mobile_no = app_user_obj.mobile_no.split("[deleted_user]")[-1]
                video_obj_list = get_all_videos(user_obj)
                for video_obj in video_obj_list:
                    video_obj.is_available = True
                    video_obj.save()
                user_obj.is_active = True
                user_obj.save()
                # app_user_obj.save()

    unblock_user.short_description = "Undelete these users"

    def add_to_staff(self, request, queryset):
        for user_obj in queryset:
            user_obj.is_staff = True
            user_obj.save()

    add_to_staff.short_description = "Add user to staff"

    def remove_from_staff(self, request, queryset):
        for user_obj in queryset:
            user_obj.is_staff = False
            user_obj.save()

    remove_from_staff.short_description = "Remove user from staff"

    def get_readonly_fields(self, request, obj=None):
        if obj:
            if obj.is_staff is False:
                return ["username", 'date_joined', 'last_login', "coin_balance", 'redeemtion_history', "password",
                        "first_name", 'profile_link']
            else:
                return ["username", 'date_joined', 'last_login', "coin_balance", 'redeemtion_history', 'profile_link']
        else:
            return ["coin_balance", 'redeemtion_history', 'profile_link']

    fieldsets = (
        ('Basic Details', {
            'fields': ('profile_link', "username", 'first_name', "email", 'date_joined', 'last_login', 'is_active',
                       'password'),
        }),
        ('Permission And Groups', {
            'classes': ('collapse',),
            'fields': ("is_superuser", 'is_staff', 'groups', 'user_permissions',),
        }),
        ('Coins And Reedemtions', {
            'classes': ('collapse',),
            'fields': ("coin_balance", 'redeemtion_history',),
        }),
    )
    search_fields = ('username',)
    list_filter = ('is_active', 'is_staff', ('date_joined', DateRangeFilter))
    # readonly_fields = ("coin_balance", 'redeemtion_history',)
    list_display = ("username", 'email', 'first_name', 'is_active', 'is_staff')
    actions = (block_user, unblock_user, add_to_staff, remove_from_staff)


class UserCrossFollowerAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def followed_user(self, obj):
        app_user_obj = AppUser.objects.get(user_id=obj.user_id)
        return format_html(
            '<a href="http://' + settings.ALLOWED_HOSTS[1] + '/admin/login_signup/appuser/{}/change/">{}</a>'
            .format(app_user_obj.id, obj.user_id.username))

    def followed_by_user(self, obj):
        app_user_obj = AppUser.objects.get(user_id=obj.followed_by)
        return format_html(
            '<a href="http://' + settings.ALLOWED_HOSTS[1] + '/admin/login_signup/appuser/{}/change/">{}</a>'
            .format(app_user_obj.id, obj.followed_by.username))

    list_filter = (('followed_at', DateRangeFilter),)
    list_display = ("followed_user", 'followed_by_user', 'followed_at')
    readonly_fields = ("user_id", 'followed_by', 'followed_at',)


class UserXBlockedUserAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def blocked_user(self, obj):
        app_user_obj = AppUser.objects.get(user_id=obj.user_id)
        return format_html(
            '<a href="http://' + settings.ALLOWED_HOSTS[1] + '/admin/login_signup/appuser/{}/change/">{}</a>'
            .format(app_user_obj.id, obj.user_id.username))

    def blocked_by_user(self, obj):
        app_user_obj = AppUser.objects.get(user_id=obj.blocked_by)
        return format_html(
            '<a href="http://' + settings.ALLOWED_HOSTS[1] + '/admin/login_signup/appuser/{}/change/">{}</a>'
            .format(app_user_obj.id, obj.blocked_by.username))

    list_filter = (('blocked_at', DateRangeFilter),)
    list_display = ("blocked_user", 'blocked_by_user', 'blocked_at')
    readonly_fields = ("user_id", 'blocked_by', 'blocked_at',)


class EventAdminSite(AdminSite):
    def get_app_list(self, request):
        """
        Return a sorted list of all the installed apps that have been
        registered in this site.
        """
        ordering = {
            "Login_Signup": 1,
            "Coins_And_Gifts": 2,
            "Effects_And_Filters": 3,
            "Reported": 4,
            "Star_And_Channels": 5,
            "Video": 6,
            "Authentication and Authorization": 7,
        }
        app_dict = self._build_app_dict(request)
        # a.sort(key=lambda x: b.index(x[0]))
        # Sort the apps alphabetically.
        app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())

        # Sort the models alphabetically within each app.
        for app in app_list:
            app['models'].sort(key=lambda x: ordering[x['name']])

        return app_list


admin.site.register(AppUser, AppUserAdmin)
admin.site.register(UserXBlockedUser, UserXBlockedUserAdmin)
admin.site.register(UserCrossFollower, UserCrossFollowerAdmin)
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
