from django.urls import include, path

from rest_framework.authtoken import views as token_view

urlpatterns = [
    path('api-token-auth/', token_view.obtain_auth_token),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
