import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone
import pytz

def get_current_time():
    return timezone.now().astimezone(pytz.timezone('Asia/Dhaka'))


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    id = models.AutoField(primary_key=True, editable=False)  # Unique primary key
    username = models.CharField(max_length=150, unique=False,null=True,blank=True)  # Not unique
    email = models.EmailField(blank=True, null=True,unique=True)  # Not unique
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.username or self.email or str(self.pk)


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
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='partner_profile')
    venue_name = models.CharField(max_length=255,null=True,blank=True)
    address = models.TextField(null=True,blank=True)
    phone_number = models.CharField(max_length=15, null=True,blank=True)
    ssid = models.CharField(max_length=255,null=True,blank=True)
    code = models.CharField(max_length=255,null=True,blank=True)
    password = models.CharField(max_length=255,null=True,blank=True)
    # How long an end-user session may stay on this Wi‑Fi (minutes); partner-configurable.
    session_duration_minutes = models.PositiveIntegerField(default=30)
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

class PartnerApp(models.Model):
    app = models.FileField(upload_to='apps/partner/')
    count = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=get_current_time)
    
    def __str__(self):
        return self.created_at.strftime('%Y-%m-%d %H:%M:%S')
ADSIZES = [
    ('320x50', '320x50'),
    ('300x250', '300x250'),
    ('320x100', '320x100'),
    ('1024x768', '1024x768'),
    
]

LOCATIONS=[
    ('login', 'login'),
    ('home', 'home'),
    ('connecting', 'connecting'),
    ('connected', 'connected'),
    ('reconnect', 'reconnect'),
    ('registration', 'registration'),
    ('dashboard', 'dashboard'),
    ('list', 'list'),
]
class Adsmodel(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    adSize=models.CharField(max_length=255,choices=ADSIZES)
    location=models.CharField(max_length=255,choices=LOCATIONS)
    adUrl=models.URLField(max_length=255)
    adLanding= models.URLField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=get_current_time,editable=False)
    
    
    def __str__(self):
        return self.adSize
    
class AdsViewHistory(models.Model):
    partner = models.ForeignKey(PartnerProfile, on_delete=models.CASCADE, related_name='ads_view_histories',null=True,blank=True)
    ads = models.ForeignKey(Adsmodel, on_delete=models.CASCADE, related_name='ads_view_histories')
    count = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=get_current_time,editable=False)
    users= models.ManyToManyField('Adusers',related_name='ads_view_histories')
    
    def __str__(self):
        return self.ads.adSize
    
class Adusers(models.Model):
    device_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=get_current_time,editable=False)
    
    def __str__(self):
        return self.device_id
    
class VenuDetails(models.Model):
    partner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='venu_data')
    latitude = models.DecimalField(max_digits=10, decimal_places=8)
    longitude = models.DecimalField(max_digits=11, decimal_places=8)
    created_at = models.DateTimeField(default=get_current_time,editable=False)
    
    def __str__(self):
        return self.partner.username


class ContactMessage(models.Model):
    """Website / app store contact form submissions (unauthenticated)."""
    name = models.CharField(max_length=200)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(default=get_current_time, editable=False)
    user_agent = models.CharField(max_length=512, blank=True, null=True)
    source_ip = models.GenericIPAddressField(blank=True, null=True)

    def __str__(self):
        return f'{self.email} @ {self.created_at}'
