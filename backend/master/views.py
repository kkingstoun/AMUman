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
    return JsonResponse({"status": "command_sent", "command": command})



def node_list(request):
    nodes = Nodes.objects.all()
    return render(request, 'master/node_list.html', {'nodes': nodes})

class NodeManagementView(APIView):
    @csrf_exempt
    def post(self, request, format=None):
        action = request.data.get('action')

        if action == 'assign_new_node':
            return self.assign_new_node(request)
        elif action == 'assign_gpus':
            return self.assign_gpus(request)
        elif action == 'update_node_status':
            return self.update_node_status(request)
        elif action == 'update_node_gpus_status':
            return self.update_node_gpus_status(request)
        else:
            return Response({'message': 'Uknown action.'}, status=400)
        
    def assign_new_node(self, request):
        ip = request.data.get('ip')
        port = request.data.get('port')
        gpu_info = request.data.get('gpu_info')

        node, created = Nodes.objects.get_or_create(
            ip=ip,
            port=port,
            defaults={'gpu_info': gpu_info, 'last_seen': timezone.now()}
        )

        if created:
            return Response({'message': 'Node assigned sucessfull.'}, status=201)
        else:
            # Aktualizuj istniejący węzeł
            node.gpu_info = gpu_info
            node.last_seen = timezone.now()
            node.save()
            return Response({'message': 'Node status updated.'}, status=200)
        
    def assign_gpus(self, request):
        pass
    
    def update_node_status(self, request):
        pass
    
    def update_node_gpus_status(self, request):
        pass