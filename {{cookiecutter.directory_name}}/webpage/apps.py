# -*- coding: UTF-8 -*-

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class WebpageConfig(AppConfig):
    name = 'webpage'
    label = 'webpage'
    verbose_name = _("Webpage")
