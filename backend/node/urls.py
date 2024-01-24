from django.urls import path
from .views import NodeReportView

urlpatterns = [
    path('report/', NodeReportView.as_view(), name='node-report'),
]
