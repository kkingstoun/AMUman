from django.urls import path

from . import views, views_frontend

urlpatterns = [
    path('messages/', views.MessageListView.as_view(), name='message-list'),
    path('messages/create/', views.MessageCreateView.as_view(), name='message-create'),
    path('tasks/', views_frontend.TasksListView.as_view(), name='task-list'),
    path('nodes/', views_frontend.NodesListView.as_view(), name='nodes-list'),
    path('gpus/', views_frontend.GpusListView.as_view(), name='task-list'),
    path("console/", views_frontend.ConsoleView.as_view(), name="console"),
    path("settings/", views_frontend.SettingsView.as_view(), name="managersettings"),
    
    path('tasks/<int:pk>/edit/', views_frontend.TaskUpdateView.as_view(), name='task-edit'),
    path('tasks/<int:task_id>/remove/', views_frontend.TasksListView.as_view(), name='task-remove'),
    path('tasks/<int:task_id>/output/', views_frontend.TasksListView.as_view(), name='task-output'),
    path('tasks/<int:task_id>/run/', views_frontend.TasksListView.as_view(), name='task-run'),
    path('tasks/add/', views_frontend.TasksAddView.as_view(), name='task-run'),
]
