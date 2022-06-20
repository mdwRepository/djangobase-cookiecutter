# -*- coding: UTF-8 -*-

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView

from .models import TermsOfUse, TermsOfUseAccepted


class TermsOfUseView(TemplateView):
    template_name = 'users/terms_of_use.html'

    def get_context_data(self, **kwargs):
        context = super(TermsOfUseView, self).get_context_data(**kwargs)
        return context


class TermsOfUseAcceptView(View):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TermsOfUseAcceptView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        tou = TermsOfUse.get_current_tou(self)
        return render(request,
                      'users/terms_of_use_accept.html',
                      {
                          'next': request.GET.get('next'),
                          'tou': tou,
                          'logout_url': reverse('logout')
                      }
                      )

    def post(self, request, *args, **kwargs):
        tou = TermsOfUse.get_current_tou(self)
        # redirect to next location or root
        # redirect_to = request.REQUEST.get('next', '/')
        accepted_tou = TermsOfUseAccepted(
            user=self.request.user,
            tou_version=tou
        )
        print(accepted_tou)
        accepted_tou.save()
        return HttpResponseRedirect('/')
