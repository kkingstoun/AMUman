from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect

from rest_framework import viewsets
from common_models.models import Task
from .serializers import TaskSerializer

#Tymczasowe wyłączenie tokenów
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Nodes


from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .components.form import TaskForm


@csrf_exempt
def add_task(request):
    # Logika dodawania nowego zadania
    if request.method == 'POST':
       task_path = request.POST.get('path')
       if task_path:
            priority = request.POST.get('priority', 0)
            task = Task(path=task_path, priority=priority)
            task.save()
            return JsonResponse({'status': 'success', 'task_id': task.id})
       else:
           return JsonResponse({'status': 'error', 'message': 'No path provided'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Only POST method is allowed'})

@csrf_exempt
def get_task(request):
    if request.method == 'GET':
        task = Task.objects.filter(status='waiting').order_by('id').first()
        if task:
            task.status = 'running'
            task.start_time = timezone.now()  # Ustaw czas rozpoczęcia zadania
            task.save()
            return JsonResponse({'status': 'success', 'task_id': task.id, 'path': task.path})
        else:
            return JsonResponse({'status': 'error', 'message': 'No waiting tasks'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Only GET method is allowed'})
    
@csrf_exempt
def finish_task(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        if task_id:
            try:
                task = Task.objects.get(id=task_id, status='running')
                task.status = 'finished'
                task.end_time = timezone.now()  # Ustaw czas zakończenia zadania
                task.save()
                return JsonResponse({'status': 'success', 'message': 'Task finished'})
            except Task.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Task not found or not running'})
        else:
            return JsonResponse({'status': 'error', 'message': 'No task ID provided'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Only POST method is allowed'})


def index(request):
    tasks = Task.objects.all()
    return render(request, 'scheduler/index.html', {'tasks': tasks})


@csrf_exempt
def pause_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.status = 'paused'
    task.save()
    return redirect('index')  # Powrót do strony głównej

@csrf_exempt
def resume_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if task.status == 'paused':
        task.status = 'waiting'
        task.save()
    return redirect('index')

@csrf_exempt
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task.delete()
    return redirect('task_list')  


def update_priority(request, task_id, priority):
    task = get_object_or_404(Task, id=task_id)
    task.priority = priority
    task.save()
    return redirect('index')


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    
    
def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'master/task_list.html', {'tasks': tasks})

def edit_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'master/edit_task.html', {'form': form})


class AssignNewNodeView(APIView):
    @csrf_exempt
    def post(self, request, format=None):
        node, created = Node.objects.get_or_create(
            ip=request.data.get('ip'),
            port=request.data.get('port'),
            defaults={'gpu_info': request.data.get('gpu_info')}
        )
        if created:
            return Response({'message': 'Node zarejestrowany pomyślnie.'}, status=201)
        return Response({'message': 'Node już istnieje.'}, status=200)
    
    
@csrf_exempt
def send_command(request):
    command = request.POST.get('command', 'default_command')
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "nodes_group",
        {
            "type": "node.command",
            "command": command,
        }
    )
    print("DUPA")
    return JsonResponse({"status": "command_sent", "command": command})
