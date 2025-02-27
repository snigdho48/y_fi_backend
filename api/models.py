import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone
import pytz


def get_current_time():
    return timezone.now().astimezone(pytz.timezone('Asia/Dhaka'))
# Create your models here.


class CustomUser(AbstractUser):
    id = models.AutoField(primary_key=True, editable=False)  # Unique primary key
    username = models.CharField(max_length=150)  # Not unique
    email = models.EmailField(blank=True, null=True)  # Not unique

    USERNAME_FIELD = 'username'  # Authenticate using username
    REQUIRED_FIELDS = []  # No additional required fields

    def __str__(self):
        return self.username