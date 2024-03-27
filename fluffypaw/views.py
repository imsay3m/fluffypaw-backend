from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = User.objects.all()
    serializer_class = UserSerializer
