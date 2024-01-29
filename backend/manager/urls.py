from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from . import views

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)

urlpatterns = [
      
    path('task/', TaskListView.as_view(), name='task_list'),
    path('task/<action>/<int:task_id>/', TaskManagerView.as_view(), name='task_action_id'),
    path('task/<action>/', TaskManagerView.as_view(), name='task_action'),
    
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



]