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
    list_display = ('id', 'device_id', 'uuid', 'get_node_display', 'model', 'get_speed_display', 'util', 'is_running_amumax', 'get_status_display', 'last_update')
    ordering = ["-device_id"]
    
    def get_node_display(self, obj):
        return obj.node.name  # Zakładając, że model Node ma pole name
    get_node_display.short_description = 'Node'

    def get_speed_display(self, obj):
        return obj.get_speed_display()
    get_speed_display.short_description = 'Speed'

    def get_status_display(self, obj):
        return obj.get_status_display()
    get_status_display.short_description = 'Status'

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