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
class MyTokenObtainPartnerPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        token['user_groups'] = [group.name for group in user.groups.all()]
        token['partner_id'] = user.id
        return token

    def validate(self, attrs,):
        email = attrs.get("email")
        password = attrs.get("password")
        if not email:
            raise serializers.ValidationError({"error": "Email is required"})

        if not password:
            raise serializers.ValidationError({"error": "Password is required"})
        
        # Check if user exists by email            
        
        user = authenticate(email=email, password=password)

        if not user:
            raise serializers.ValidationError({"error": "Invalid credentials"})

        # Generate token
        data = super().validate(attrs)
        data['username'] = user.username
        data['email'] = user.email
        data['user_group'] = user.groups.all().first().name if user.groups.exists() else None
        data['token'] = str(data['access'])
        data.pop('access')
        # Add partner_profile_id if exists
        data['partner_id'] = user.id if user.groups.filter(name='partner').exists() else None
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
    user_id = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), source='user', write_only=True, required=False)
    username = serializers.CharField(required=False, write_only=True)
    userpassword = serializers.CharField(write_only=True, required=False)
    email = serializers.EmailField(write_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = PartnerProfile
        fields = ("id", 'uuid', 'user', 'user_id', 'username', 'userpassword', 'email', 'venue_name', 'code', 'address', 'phone_number', 'ssid', 'password', 'created_at', 'updated_at')

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
        
class CustomConnectedHistorySerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), write_only=True)
    partner = serializers.PrimaryKeyRelatedField(queryset=PartnerProfile.objects.all(), write_only=True)
    class Meta:
        model = ConnectedHistory
        fields = ('uuid', 'user', 'partner', 'ip', 'device_os', 'device_name','device_id','device_brand', 'created_at')
    
class ReleaseAppSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReleaseApp
        fields = '__all__'
        
class CustomPartnerProfileSerializerRegister(serializers.ModelSerializer):
    user=serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), write_only=True)
    class Meta:
        model = PartnerProfile
        fields = ('uuid', 'user', 'venue_name', 'address', 'phone_number', 'ssid', 'code', 'password','code', 'created_at', 'updated_at')
        
class VenudataViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartnerProfile
        fields = ('ssid','password', 'code', 'created_at', 'updated_at')
        
class AdsmodelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adsmodel
        fields = ('adSize', 'adUrl', 'adLanding', 'created_at')
        
class AdsViewHistorySerializer(serializers.ModelSerializer):
    user_count = serializers.SerializerMethodField(read_only=True)
    unique_user = serializers.SerializerMethodField(read_only=True)
    partner_username = serializers.SerializerMethodField(read_only=True)
    partner = serializers.PrimaryKeyRelatedField(queryset=PartnerProfile.objects.all(), write_only=True)
    
    class Meta:
        model = AdsViewHistory
        fields = ('ads', 'count', 'partner', 'partner_username', 'created_at', 'user_count', 'unique_user')
        
    def get_user_count(self, obj):
        return obj.users.count()
    
    def get_unique_user(self, obj):
        return obj.users.values_list('device_id',flat=True).distinct().count()
        
    def get_partner_username(self, obj):
        if obj.partner:
            return obj.partner.user.username
        return None