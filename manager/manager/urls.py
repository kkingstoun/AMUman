from django.urls import path

from . import views
from . import views_frontend

urlpatterns = [

    path('messages/', views.MessageListView.as_view(), name='message-list'),
    path('messages/create/', views.MessageCreateView.as_view(), name='message-create'),
    path('tasks/', views_frontend.TaskListView.as_view(), name='task-list'),
]
