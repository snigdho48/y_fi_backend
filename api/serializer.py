from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from api.models import *
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate

User = settings.AUTH_USER_MODEL


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        token['user_groups'] = [group.name for group in user.groups.all()]
        return token

    def validate(self, attrs,):
        username = self.initial_data.get('username', '')
        email = attrs.get("email")
        device_id = self.initial_data.get('device_id','') 
        device_name = self.initial_data.get('device_name','') 
        device_os = self.initial_data.get('device_os','')
        device_brand = self.initial_data.get('device_brand','')
        password = attrs.get("password")
        if not email:
            raise serializers.ValidationError({"error": "Email is required"})

        if not password:
            raise serializers.ValidationError({"error": "Password is required"})
        
        # Check if user exists by email
        user = CustomUser.objects.filter(email=email).first()
        print(user)

        if not user:
            # Create the user with a hashed password
            user = CustomUser.objects.create_user(username=username, email=email, password=password)

            # Assign the user to a default group (optional)
            group, _ = Group.objects.get_or_create(name='user')
            user.groups.add(group)
            user.save()
            userprofile = UserProfile.objects.create(user=user, device_id=device_id, device_name=device_name, device_os=device_os, device_brand=device_brand)
            userprofile.save()
            
            
        user = authenticate(email=email, password=password)
        print(user.email)

        if not user:
            raise serializers.ValidationError({"error": "Invalid credentials"})

        # Generate token
        data = super().validate(attrs)
        data['username'] = user.username
        data['email'] = user.email
        data['user_group'] = user.groups.all().first().name if user.groups.exists() else None
        data['token'] = str(data['access'])
        data.pop('access')

        return data


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField()
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'password', 'email')
        
class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = UserProfile
        fields = ('uuid', 'user', 'device_id', 'phone_number', 'device_name', 'device_os','device_brand', 'created_at', 'updated_at')
        
class PartnerProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), source='user', write_only=True)
    username = serializers.CharField(required=False,write_only=True,source='user.username')
    userpassword = serializers.CharField(write_only=True,source='user.password')
    email = serializers.EmailField(write_only=True,source='user.email')
    user = UserSerializer(read_only=True)
    class Meta:
        model = PartnerProfile
        fields = ('uuid', 'user','user_id','username','userpassword','email', 'venue_name','code', 'address', 'phone_number', 'ssid', 'code', 'password', 'created_at', 'updated_at')
        
class CustomPartnerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = PartnerProfile
        fields = ('uuid', 'user', 'venue_name')
        
class CustomUserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = UserProfile
        fields = ('uuid', 'user')

class ConnectedHistorySerializer(serializers.ModelSerializer):
    user = CustomPartnerProfileSerializer()
    partner = CustomPartnerProfileSerializer()
    class Meta:
        model = ConnectedHistory
        fields = ('uuid', 'user', 'partner', 'connected_at', 'ip', 'device_os', 'device_name','device_id', 'created_at')