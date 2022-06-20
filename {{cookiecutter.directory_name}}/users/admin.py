# -*- coding: UTF-8 -*-

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from guardian.admin import GuardedModelAdmin
from tabbed_admin import TabbedModelAdmin

from .models import *


admin.site.register(CustomGroup)


@admin.register(CustomUser)
class UserAdmin(UserAdmin, TabbedModelAdmin, GuardedModelAdmin):
    list_display = (
        'username', 'first_name', 'last_name', 'email', 'auth_type', 'is_staff', 'is_active',
        'email_confirmed', 'current_tou_accepted', 'date_joined', 'last_login')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    # list_filter = ('person__name', 'username',)
    list_filter = (
        'auth_type', 'is_staff', 'is_active', 'email_confirmed', 'current_tou_accepted',)
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions',)

    tab_overview = (
        (None, {
            'fields': ('username', 'password')
        }),
        (_('Personal info'), {
            'fields': ('first_name', 'last_name', 'email', 'email_confirmed', 'current_tou_accepted')
        }),
        (_('Important dates'), {
            'fields': ('last_login', 'date_joined')
        }),
    )
    tab_permissions = (
        (_('Status'), {
            'fields': (('is_active', 'is_staff', 'is_superuser'),)
        }),
        (_('Groups'), {
            'fields': ('groups',)
        }),
        (_('User Level Permissions'), {
            'fields': ('user_permissions',)
        }),
    )
    tabs = [
        (_('Overview'), tab_overview),
        (_('Global Permissions'), tab_permissions)
    ]

    readonly_fields = ["date_joined", "last_login", "current_tou_accepted"]


{% if cookiecutter.tou_enabled == 'y' -%}

class TermsOfUseAcceptedAdmin(admin.ModelAdmin):
    readonly_fields = ('user', 'signed_at_time', 'tou_version')

    def has_add_permission(self, request, obj=None):
        return False

admin.site.register(TermsOfUse)
admin.site.register(TermsOfUseAccepted, TermsOfUseAcceptedAdmin)

{%- endif %}