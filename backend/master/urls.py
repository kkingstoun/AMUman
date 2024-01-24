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
    path('task/<int:task_id>/pause/', views.pause_task, name='pause_task'),
    path('task/<int:task_id>/resume/', views.resume_task, name='resume_task'),
    path('task/<int:task_id>/delete/', views.delete_task, name='delete_task'),
    path('task/<int:task_id>/priority/<int:priority>/', views.update_priority, name='update_priority'),

    path('', include(router.urls)),
    # path('', views.index, name='index'),
    
    ####ADD NEW NODES####
    path('assign_new_node/', AssignNewNodeView.as_view(), name='assign-new-node'),
]