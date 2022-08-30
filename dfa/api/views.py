from django.http import QueryDict
from django.shortcuts import render
from drf_yasg.inspectors import SwaggerAutoSchema
from rest_framework import viewsets, mixins, status

# Create your views here.
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from api.models import User, Photo
from api.serializers import UserSerializer, PhotoSerializer, UserRegisterSerializer
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class UserViewSet(viewsets.ModelViewSet):
    swagger_schema = SwaggerAutoSchema
    permission_classes = [AllowAny]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)

    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegisterSerializer
        return UserSerializer


class PhotoViewSet(viewsets.ModelViewSet):
    swagger_schema = SwaggerAutoSchema
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Photo.objects.filter(user__id=self.request.user.id)

    def get_serializer_class(self):
        return PhotoSerializer

    def create(self, request, *args, **kwargs):
        if isinstance(request.data, QueryDict):  # optional
            request.data._mutable = True
        request.data['user'] = self.request.user.id
        return super().create(request, *args, **kwargs)


class DeleteAllPhotos(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = None

    def create(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
            Photo.objects.all().delete()
            return Response(dict(result=1))
        return Response(status=status.HTTP_403_FORBIDDEN)


