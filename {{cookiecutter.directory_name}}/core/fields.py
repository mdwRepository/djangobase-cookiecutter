# -*- coding: UTF-8 -*-

from django.db import models


# ---------------------------------------------------------------------------#
# Custom Field Types                                                         #
# ---------------------------------------------------------------------------#

class CustomLargeTextField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 65000)
        super(CustomLargeTextField, self).__init__(*args, **kwargs)

    def db_type(self, connection):
        return 'text'


class CustomSmallTextField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 2048)
        super(CustomSmallTextField, self).__init__(*args, **kwargs)

    def db_type(self, connection):
        return 'text'
