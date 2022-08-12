from django.contrib import admin
from .models import *
from rangefilter.filter import DateRangeFilter
from django.conf import settings
from django.utils.safestring import mark_safe


class EffectsAndFiltersAdmin(admin.ModelAdmin):
    def file_thumbnail(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height="{height}" />'.format(
            url="http://" + settings.ALLOWED_HOSTS[1] + "/media/" + str(obj.file), width=50, height=50,
        )
        )

    search_fields = ('name',)
    list_display = ("name", 'file_thumbnail', 'type', 'is_active')
    fieldsets = (('Details' ,
                {
                    'fields': ("name", 'file_thumbnail', 'file', 'thumbnail', 'type', 'is_active'),
                }),)
    readonly_fields = ('file_thumbnail',)
    list_filter = ('type', 'is_active')


admin.site.register(EffectsAndFilters, EffectsAndFiltersAdmin)
