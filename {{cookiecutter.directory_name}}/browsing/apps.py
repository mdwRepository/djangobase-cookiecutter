# -*- coding: UTF-8 -*-

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class BrowsingConfig(AppConfig):
    name = 'browsing'
    label = 'browsing'
    verbose_name = _("Browsing")
