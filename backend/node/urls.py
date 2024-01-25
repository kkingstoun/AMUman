from django.urls import path
from .views import NodeReportView
from . import views

urlpatterns = [
    path('report/', NodeReportView.as_view(), name='node-report'),
    path('get_gpu_status/', views.get_gpu_status, name='get_gpu_status'),
    # path('receive_task/', views.receive_task, name='receive_task'),
]
