import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import pytz

def get_current_time():
    return timezone.now().astimezone(pytz.timezone('Asia/Dhaka'))

class CustomUser(AbstractUser):
    id = models.AutoField(primary_key=True, editable=False)  # Unique primary key
    username = models.CharField(max_length=150, unique=False,null=True,blank=True)  # Not unique
    email = models.EmailField(blank=True, null=True,unique=True)  # Not unique

    USERNAME_FIELD = 'email'  # Authenticate using username
    REQUIRED_FIELDS = []  # Required fields for user creation

    def __str__(self):
        return self.username


class UserProfile(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    device_id = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    device_name = models.CharField(max_length=100, blank=True, null=True)
    device_os = models.CharField(max_length=100, blank=True, null=True)
    device_brand = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(default=get_current_time, editable=False)
    updated_at = models.DateTimeField(default=get_current_time, editable=False)

    def __str__(self):
        return self.user.username

class PartnerProfile(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='partner_profile')
    venue_name = models.CharField(max_length=255,null=True,blank=True)
    address = models.TextField(null=True,blank=True)
    phone_number = models.CharField(max_length=15, null=True,blank=True)
    ssid = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=get_current_time, editable=False)
    updated_at = models.DateTimeField(default=get_current_time, editable=False)
    
    def __str__(self):
        return f'{self.venue_name} - {self.user.username}'

    
class ConnectedHistory(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='connected_histories')
    partner = models.ForeignKey(PartnerProfile, on_delete=models.CASCADE, related_name='connected_histories')
    ip = models.GenericIPAddressField(null=True,blank=True)
    device_os = models.CharField(max_length=100)
    device_name = models.CharField(max_length=100)
    device_brand = models.CharField(max_length=100)
    device_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=get_current_time)
    
    def __str__(self):
        return f'{self.user.username} - {self.partner.venue_name}'
    
class ReleaseApp(models.Model):
    app = models.FileField(upload_to='apps/')
    count = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=get_current_time)
    
    def __str__(self):
        return self.created_at.strftime('%Y-%m-%d %H:%M:%S')

    