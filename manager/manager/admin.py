from django.contrib import admin

from .models import *


@admin.register(Task)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'path', 'node_name', 'port', 'submit_time', 'start_time', 'end_time', 'error_time', 'priority', 'gpu_partition', 'est', 'status', 'assigned_node_id', 'assigned_gpu_id', 'output', 'error', 'flags')
    ordering = ['-submit_time']
