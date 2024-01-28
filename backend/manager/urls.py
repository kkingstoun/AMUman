from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from . import views

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)

urlpatterns = [
    
    #OLD LINK TO FIX:
    path('get_task/', views.get_task, name='get_task'),
    path('finish_task/', views.finish_task, name='finish_task'),
    # path('send_command/', views.send_command, name='send_command'),
    
    path('tasks/', task_list, name='task_list'),
    path('task/add_new_task/', TaskManagerView.as_view(), name='add_task_form'),
    path('task/edit/<int:task_id>/', TaskManagerView.as_view(), name='edit_task'),
    path('task/delete/<int:task_id>/', TaskManagerView.as_view(), name='delete_task'),
    
    
    path('task/<int:task_id>/pause/', views.pause_task, name='pause_task'),
    path('task/<int:task_id>/resume/', views.resume_task, name='resume_task'),
    path('task/<int:task_id>/priority/<int:priority>/', views.update_priority, name='update_priority'),
    
    
    
    
    # path('', include(router.urls)),
    # path('', views.index, name='index'),
    
    ####NODE-LIST####
    path('nodes/', NodeListView.as_view(), name='node_list'),
    path('nodes/refresh_all_nodes/', NodeListView.as_view(), name='refresh_all_nodes'),  # Lista wszystkich węzłów
    path('nodes/<int:node_id>/', NodeListView.as_view(), name='manage_node'),
    path('nodes/<int:node_id>/refresh_gpus/', NodeListView.as_view(), name='refresh_gpus'),
    path('nodes/<int:node_id>/refresh_gpus_ajax/', NodeListView.refresh_gpus_ajax, name='refresh_gpus_ajax'),

    path('gpus/', GpusListView.as_view(), name='gpus_list'),  # Lista wszystkich węzłów
   
    ####NODE-MANAGEMENT####
    path('node-management/', NodeManagementView.as_view(), name='node_management'),

    ####TASK-RUN####
    path('task/<int:task_id>/<str:action>', TaskRunView.as_view(), name='task_action'),


]