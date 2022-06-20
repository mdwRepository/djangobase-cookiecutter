# -*- coding: UTF-8 -*-

from django.urls import include, path

from rest_framework.authtoken import views as token_view

from .views import TermsOfUseView, TermsOfUseAcceptView

urlpatterns = [
    path('api-token-auth/', token_view.obtain_auth_token),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('terms-of-use/', TermsOfUseView.as_view(), name='terms_of_use'),
    path('terms-of-use-accept/', TermsOfUseAcceptView.as_view(), name='terms_of_use_accept'),
]