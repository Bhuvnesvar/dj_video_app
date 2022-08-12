from django.contrib import admin
from rangefilter.filter import DateRangeFilter
from .models import *
from django.utils.html import format_html
from django.conf import settings
from login_signup.models import *
from django_admin_listfilter_dropdown.filters import (
    DropdownFilter, ChoiceDropdownFilter, RelatedDropdownFilter)

class ReportTypeAdmin(admin.ModelAdmin):
    search_fields = ('name', 'description')
    list_display = ("name", 'description', "for_what", 'max_reports')


class ReportPostAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def post_content(self, obj):
        video_obj = obj.post
        length = len(video_obj.caption)
        if length >= 25:
            length = 25
        return format_html(
            '<a href="http://' + settings.ALLOWED_HOSTS[1] + '/admin/video/mediatable/{id}/change/"><img src="{url}" width="{width}" '
            'height="{height}" />{caption} </a>'
                .format(id=video_obj.id,
                        url="http://" + settings.ALLOWED_HOSTS[1] + "/media/" + str(video_obj.thumbnail),
                        width=50,
                        height=50,
                        caption="  " + video_obj.caption[0:length]))

    def reported_by_user(self,obj):
        user_obj = obj.reported_by
        app_user_obj = AppUser.objects.filter(user_id=user_obj)[0]
        if user_obj.is_staff is True:
            return format_html('<a href="http://' + settings.ALLOWED_HOSTS[1] + '/admin/auth/user/{id}/change/" '
                               'target="_blank">{username}</a>'.format(id=user_obj.id, username=user_obj.username))
        else:
            return format_html('<a href="http://' + settings.ALLOWED_HOSTS[1] + '/admin/login_signup/appuser/{id}/change/" '
                               'target="_blank">{username}</a>'.format(
                id=app_user_obj.id, username=app_user_obj.username))

    search_fields = ("post__caption","post__user_id__first_name","post__user_id__username","reported_by__username",
                      "reported_by__first_name")
    list_display = ("post_content", 'reported_by_user', "report_type", 'reporting_time')
    # readonly_fields =
    list_filter = ('report_type', ('reporting_time', DateRangeFilter), ("post__user_id__id", DropdownFilter) ,)


class ReportUserAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def the_reported_user(self, obj):
        user_obj = obj.reported_user
        app_user_obj = AppUser.objects.filter(user_id=user_obj)[0]
        return format_html(
            '<a href="http://' + settings.ALLOWED_HOSTS[1] + '/admin/login_signup/appuser/{id}/change/">{username}</a>'
                .format(id=app_user_obj.id,
                        username=app_user_obj.username))

    def reported_by_user(self, obj):
        user_obj = obj.reported_by
        app_user_obj = AppUser.objects.filter(user_id=user_obj)[0]
        return format_html(
            '<a href="http://' + settings.ALLOWED_HOSTS[1] + '/admin/login_signup/appuser/{id}/change/">{username}</a>'
                .format(id=app_user_obj.id,
                        username=app_user_obj.username))

    search_fields = ("reported_user__username","reported_user__first_name","reported_by__first_name","reported_by__username")
    list_display = ("the_reported_user", 'reported_by_user', 'reporting_time')
    # readonly_fields =
    list_filter = (('reporting_time', DateRangeFilter),)


admin.site.register(ReportTypes, ReportTypeAdmin)
admin.site.register(PostReportHistory, ReportPostAdmin)
admin.site.register(UserReportHistory, ReportUserAdmin)
