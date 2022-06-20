from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny

from ..models import CustomUser
from .serializers import CreateCustomUserSerializer, CustomUserSerializer


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    """
    Updates and retrieves user accounts
    """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class UserCreateViewSet(mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    """
    Creates user accounts
    """
    queryset = CustomUser.objects.all()
    serializer_class = CreateCustomUserSerializer
    permission_classes = (AllowAny,)