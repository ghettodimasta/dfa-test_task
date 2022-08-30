from rest_framework import serializers
from django.contrib.auth.hashers import make_password, check_password

from api.models import User, Photo


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class PhotoSerializer(serializers.ModelSerializer):
    img = serializers.ImageField(required=True, use_url=True,max_length=None),

    class Meta:
        model = Photo
        fields = '__all__'