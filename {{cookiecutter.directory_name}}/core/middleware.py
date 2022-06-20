# -*- coding: UTF-8 -*-

import logging

from django.shortcuts import redirect
from django.urls import reverse

logging.basicConfig(format='%(name)s-%(levelname)s-%(asctime)s-%(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class HideAdminForUnauthorizedUsersMiddleware:
    """
    Hide admin area from unauthorized users.
    - unauthenticated users are redirected to login
    - unauthorized logged in users are redirected to homepage
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith(reverse('admin:index')):
            if not request.user.is_authenticated:
                return redirect(reverse('login'))
            else:
                if not (request.user.is_staff and request.user.is_active):
                    return redirect('/')
        return self.get_response(request)
