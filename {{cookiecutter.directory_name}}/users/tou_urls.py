from django.urls import include, path

from .views import TermsOfUseView, TermsOfUseAcceptView

urlpatterns = [
    path('terms-of-use/', TermsOfUseView.as_view(), name='terms_of_use'),
    path('terms-of-use-accept/', TermsOfUseAcceptView.as_view(), name='terms_of_use_accept'),
]
