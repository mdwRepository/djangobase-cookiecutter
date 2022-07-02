# -*- coding: UTF-8 -*-

from django.conf.urls import url
from django.urls import include

urlpatterns = [
    url('', include(('users.user_urls', 'users'), namespace='users')),
]


# ---------------------------------------------------------------------------#
# Terms Of Use                                                               #
# ---------------------------------------------------------------------------#

# Terms Of Use if activated
{% if cookiecutter.tou_enabled == 'y' -%}

urlpatterns += [
    url('', include(('users.tou_urls', 'users'), namespace='users')),
]

{%- endif %}