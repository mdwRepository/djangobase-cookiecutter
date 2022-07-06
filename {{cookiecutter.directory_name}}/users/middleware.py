# -*- coding: UTF-8 -*-

import logging

from django.shortcuts import redirect
from django.urls import reverse

logging.basicConfig(format='%(name)s-%(levelname)s-%(asctime)s-%(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

{% if cookiecutter.tou_enabled == 'y' -%}

class TermsOfUseAcceptedMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        ignored_paths = [
            reverse('user_login'),
            reverse('user_logout'),
            reverse('tou:terms_of_use'),
            reverse('tou:terms_of_use_accept'),
        ]
        user = request.user
        if user.is_superuser == True:
            return self.get_response(request)
        elif user == 'AnonymousUser':
            return self.get_response(request)
        else:
            if user.is_authenticated == True and user.current_tou_accepted == False:
                if request.path not in ignored_paths:
                    return redirect(reverse('tou:terms_of_use_accept'))
            return self.get_response(request)

{%- endif %}
