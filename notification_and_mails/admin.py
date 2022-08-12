from django.contrib import admin
from datetime import datetime
from .models import *
from rangefilter.filter import DateRangeFilter
from django.utils.html import format_html
from django.conf import settings
from login_signup.models import *
from django_admin_listfilter_dropdown.filters import (
    DropdownFilter, ChoiceDropdownFilter, RelatedDropdownFilter)

class NotificationTemplatesAdmin(admin.ModelAdmin):
    search_fields = ('notification_type',)
    list_display = ("notification_type", 'notification_template',)


class NotificationHistoryAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def user(self,obj):
        user_obj = obj.user_id
        if user_obj.is_staff is True:
            return format_html('<a href="http://' + settings.ALLOWED_HOSTS[1] + '/admin/auth/user/{id}/change/" '
                               'target="_blank">{username}</a>'.format(id=user_obj.id, username=user_obj.username))
        else:
            return format_html('<a href="http://' + settings.ALLOWED_HOSTS[1] + '/admin/login_signup/appuser/{id}/change/" '
                               'target="_blank">{username}</a>'.format(
                id=AppUser.objects.filter(user_id=user_obj)[0].id, username=user_obj.username))


    search_fields = ('user_id__username',)
    list_display = ('user', "title", "message", "time")
    list_filter = ("title", ('time', DateRangeFilter))


class EmailTemplatesAdmin(admin.ModelAdmin):
    search_fields = ('email_type',)
    list_display = ("email_type", 'email_template')


class EmailHistoryAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def user(self,obj):
        user_obj = obj.user_id
        if user_obj.is_staff is True:
            return format_html('<a href="http://' + settings.ALLOWED_HOSTS[1] + '/admin/auth/user/{id}/change/" '
                               'target="_blank">{username}</a>'.format(id=user_obj.id, username=user_obj.username))
        else:
            return format_html('<a href="http://' + settings.ALLOWED_HOSTS[1] + '/admin/login_signup/appuser/{id}/change/" '
                               'target="_blank">{username}</a>'.format(
                id=AppUser.objects.filter(user_id=user_obj)[0].id, username=user_obj.username))

    search_fields = ('user_id__username',)
    list_display = ("user", 'email', "email_time")
    list_filter = ("email", ('email_time', DateRangeFilter))


class TermAndConditionAndPolicyAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        MAX_OBJECTS = 2
        if self.model.objects.count() >= MAX_OBJECTS:
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        return False

    def body_data(self, obj):
        return obj.body[:100]

    search_fields = ('title',)
    list_display = ("title", 'body_data',)


admin.site.register(NotificationTemplates, NotificationTemplatesAdmin)
admin.site.register(NotificationHistory, NotificationHistoryAdmin)
admin.site.register(EmailTemplates, EmailTemplatesAdmin,)
admin.site.register(EmailHistory, EmailHistoryAdmin)
admin.site.register(TermAndConditionAndPolicy, TermAndConditionAndPolicyAdmin)
