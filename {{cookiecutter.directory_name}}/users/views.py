# -*- coding: UTF-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout

from . forms import form_user_login


# ---------------------------------------------------------------------------#
# Login / Logout                                                             #
# ---------------------------------------------------------------------------#

def user_login(request):
    if request.method == 'POST':
        form = form_user_login(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user and user.is_active:
                login(request, user)
                return HttpResponseRedirect(request.GET.get('next', '/'))
            return HttpResponse('user does not exist')
    else:
        form = form_user_login()
        return render(request, 'users/user_login.html', {'form': form})


def user_logout(request):
    logout(request)
    return render(request, "users/user_logout.html")


# ---------------------------------------------------------------------------#
# Terms Of Use                                                               #
# ---------------------------------------------------------------------------#

# Terms Of Use if activated
{% if cookiecutter.tou_enabled == 'y' -%}

from django.contrib.auth.decorators import login_required
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
{%- endif %}
