# -*- coding: UTF-8 -*-

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class CoreConfig(AppConfig):
    name = 'core'
    label = 'core'
    verbose_name = _("Core")
