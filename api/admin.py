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
    
admin.site.register(CustomUser, CustomUserAdmin)
    
class UserProfileAdmin(admin.ModelAdmin):
    model = UserProfile
    list_display = ('id', 'user', 'phone_number', 'device_name','device_brand', 'device_os', 'created_at', 'updated_at')
    search_fields = ('user__username', 'device_os', 'device_name','device_brand')
    ordering = ('-created_at',)
    
admin.site.register(UserProfile, UserProfileAdmin)

class PartnerProfileAdmin(admin.ModelAdmin):
    model = PartnerProfile
    list_display = ('id', 'user', 'venue_name','code', 'ssid', 'password', 'address', 'phone_number', 'created_at', 'updated_at')
    search_fields = ('user__username', 'venue_name','code', 'address', 'ssid')
    ordering = ('-created_at',)
    
admin.site.register(PartnerProfile, PartnerProfileAdmin)
    
class ConnectedHistoryAdmin(admin.ModelAdmin):
    model = ConnectedHistory
    list_display = ('id', 'user', 'partner', 'ip', 'device_os', 'device_name','device_brand', 'created_at')
    search_fields = ('user__username', 'partner__venue_name', 'ip', 'device_os', 'device_name','device_brand')
    ordering = ('-created_at',)
    
admin.site.register(ConnectedHistory, ConnectedHistoryAdmin)