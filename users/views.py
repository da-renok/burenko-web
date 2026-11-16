import logging

from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import AllowAny

from .serializers import RegisterSerializer

logger = logging.getLogger(__name__)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        logger.info("Зареєстровано користувача: %s", user.username)
