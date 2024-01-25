from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from . import views

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)

urlpatterns = [
    path('add_task/', views.add_task, name='add_task'),
    path('get_task/', views.get_task, name='get_task'),
    path('finish_task/', views.finish_task, name='finish_task'),
    path('send_command/', views.send_command, name='send_command'),
    path('task/<int:task_id>/pause/', views.pause_task, name='pause_task'),
    path('task/<int:task_id>/resume/', views.resume_task, name='resume_task'),
    path('tasks/delete/<int:task_id>/', delete_task, name='delete_task'),
    path('tasks/edit/<int:task_id>/', edit_task, name='edit_task'),
    path('task/<int:task_id>/priority/<int:priority>/', views.update_priority, name='update_priority'),
    path('tasks/', task_list, name='task_list'),
    path('nodes/', node_list, name='node_list'),
    path('', include(router.urls)),
    # path('', views.index, name='index'),
    
    ####NODE-MANAGEMENT####
    path('node-management/', NodeManagementView.as_view(), name='node_management'),
]