from django.contrib import admin
from .models import *

# Register your models here.
from django.contrib.auth.admin import UserAdmin

admin.site.site_header = "Y Fi Backend"
admin.site.site_title = "Y Fi Backend"
admin.site.index_title = "Y Fi Backend"

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('id', 'email', 'username', 'is_active', 'is_staff')
    search_fields = ('email', 'username')
    ordering = ('id',)