from django.urls import include, path

from rest_framework.authtoken import views as token_view

from .views import user_login, user_logout

urlpatterns = [
    path('login/', user_login, name='user_login'),
    path('logout/', user_logout, name='user_logout'),
    path('api-token-auth/', token_view.obtain_auth_token),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
