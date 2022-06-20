# -*- coding: UTF-8 -*-

import logging

from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

log = logging.getLogger(__name__)


class CustomUserManager(BaseUserManager):

    def get_by_natural_key(self, username):
        case_insensitive_username_field = '{}__iexact'.format(self.model.USERNAME_FIELD)
        return self.get(**{case_insensitive_username_field: username})

    def create_user(self, email, password, **extra_fields):

        if not email:
            raise ValueError(_('An e-mail address must be provided.'))

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff flag.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser flag.'))
        return self.create_user(email, password, **extra_fields)
