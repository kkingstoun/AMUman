from django.contrib import admin

from .models import Gpu, Job, ManagerSettings, Node, UserProfile

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
# from .forms import CustomUserChangeForm

@admin.register(Job)
class PostAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Job._meta.fields]
    ordering = ["-submit_time"]


@admin.register(Node)
class NodesAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Node._meta.fields]
    ordering = ["-ip"]


@admin.register(Gpu)
class GpusAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Gpu._meta.fields]
    ordering = ["-device_id"]


@admin.register(ManagerSettings)
class ManagerSettingsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ManagerSettings._meta.fields]
    ordering = ["-queue_watchdog"]
    
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'UserProfile'

class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline, )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)