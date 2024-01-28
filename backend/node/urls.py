from django.urls import path
from .views import NodeReportView
from . import views

urlpatterns = [
    path('report/', NodeReportView.as_view(), name='node-report'),
    path('get_gpu_status/', views.get_gpu_status, name='get_gpu_status'),
    path('receive-message/', views.NodeMessageReceiver.as_view(), name='receive-message'),
    # path("send_message/", views.send_message, name="send_message"),

    # path('receive_task/', views.receive_task, name='receive_task'),
    path('tasks/<int:task_id>/<str:action>', views.TaskRunView.as_view(), name='task_action'),
    path('', views.TaskRunView.as_view(), name='task_list'),
]
