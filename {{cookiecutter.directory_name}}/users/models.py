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


# ---------------------------------------------------------------------------#
# Authentication                                                             #
# ---------------------------------------------------------------------------#


# LDAP authentication if activated
{% if cookiecutter.ldap_authentication == 'y' -%}

import re

from django.core.cache import cache
from django_auth_ldap.backend import LDAPBackend


class CustomLDAPBackend(LDAPBackend):
    default_settings = {
        "LOGIN_COUNTER_KEY": "CUSTOM_LDAP_LOGIN_ATTEMPT_COUNT",
        "LOGIN_ATTEMPT_LIMIT": 5,
        "RESET_TIME": 30 * 60,
        "USERNAME_REGEX": r"^.*$",
    }

    def authenticate_ldap_user(self, ldap_user, password):

        if self.exceeded_login_attempt_limit():
            # Or you can raise a 403 if you do not want
            # to continue checking other auth backends
            print("Login attempts exceeded.")
            return None
        self.increment_login_attempt_count()
        user = ldap_user.authenticate(password)
        if user and self.username_matches_regex(user.username):
            # set default values for LDAP users
            user.auth_type = 'LDAP'
            user.is_staff = True
            user.email_confirmed = True
            user.save()
        return user

    @property
    def login_attempt_count(self):
        return cache.get_or_set(
            self.settings.LOGIN_COUNTER_KEY, 0, self.settings.RESET_TIME
        )

    def increment_login_attempt_count(self):

        try:
            cache.incr(self.settings.LOGIN_COUNTER_KEY)
        except ValueError:
            cache.set(self.settings.LOGIN_COUNTER_KEY, 1, self.settings.RESET_TIME)

    def exceeded_login_attempt_limit(self):
        return self.login_attempt_count >= self.settings.LOGIN_ATTEMPT_LIMIT

    def username_matches_regex(self, username):
        return re.match(self.settings.USERNAME_REGEX, username)

{%- endif %}
