from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from api.models import *
from django.contrib.auth.models import Group


User = settings.AUTH_USER_MODEL

from django.contrib.auth.models import User, Group
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        user_groups = [group.name for group in user.groups.all()]
        token['user_groups'] = user_groups
        return token

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        user = User.objects.filter(username=username).first()

        if not user:
            user = User.objects.create_user(username=username, password=password, email=f"{username}@example.com")
            
            default_group, _ = Group.objects.get_or_create(name="user")
            user.groups.add(default_group)

        # Authenticate the user
        data = super().validate(attrs)
        data['username'] = user.username
        data['email'] = user.email
        data['user_group'] = user.groups.all().first().name if user.groups.exists() else None
        data['token'] = str(data['access'])
        data.pop('access')

        return data



class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField()
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'password', 'email')