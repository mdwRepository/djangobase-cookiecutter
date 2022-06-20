# -*- coding: UTF-8 -*-

import datetime
import logging

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, Group
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager

log = logging.getLogger(__name__)


# ---------------------------------------------------------------------------#
# User Management                                                            #
# ---------------------------------------------------------------------------#

class CustomUser(AbstractUser):
    """
       mdwRepository Custom User
    """

    objects = CustomUserManager()

    # Only used by guardian
    birth_date = models.DateField(
        null=True,
        blank=True,
    )
    # Authentication Type (LDAP, django, ...)
    # if ldap or db
    auth_type = models.CharField(
        _("auth_type"),
        null=True,
        blank=True,
        max_length=30,
        default='local',
        help_text=_("auth_type_help")
    )
    # date the user joined this application
    date_joined = models.DateTimeField(
        default=timezone.now,
        editable=False
    )

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['id']

    def __unicode__(self):
        return self.username

    @property
    def get_full_name(self):
        if self.first_name and self.last_name:
            return '%s, %s' % (self.last_name, self.first_name)
        else:
            return self.username

    @property
    def get_full_name_first_last(self):
        if self.first_name and self.last_name:
            return '%s %s' % (self.first_name, self.last_name)
        else:
            return self.username

    @property
    def get_full_name_with_username(self):
        if self.first_name and self.last_name:
            return '%s %s (%s)' % (self.first_name, self.last_name, self.username)
        else:
            return self.username


# create anonymous user for public objects (django-guardian based permission on object level)
def get_custom_anon_user(CustomUser):
    return CustomUser(
        username='AnonymousUser',
        birth_date=datetime.date(1410, 7, 15),
        current_tou_accepted=True,
    )


class CustomGroup(Group):
    """
       mdwRepository Group
    """

    class Meta:
        verbose_name = _('Group')
        verbose_name_plural = _('Groups')
        ordering = ['id']
