from django.contrib import admin

from .models import *


admin.site.register(CustomGroup)
admin.site.register(CustomUser)

{% if cookiecutter.tou_enabled == 'y' -%}

class TermsOfUseAcceptedAdmin(admin.ModelAdmin):
    readonly_fields = ('user', 'signed_at_time', 'tou_version')

    def has_add_permission(self, request, obj=None):
        return False

admin.site.register(TermsOfUse)
admin.site.register(TermsOfUseAccepted, TermsOfUseAcceptedAdmin)

{%- endif %}