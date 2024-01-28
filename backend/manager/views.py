from typing import Any
from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse
from django.db.models import Q

from rest_framework import viewsets
from common_models.models import *
from .serializers import TaskSerializer
from .components.nodes_monitor import NodesMonitor
# Tymczasowe wyłączenie tokenów
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from rest_framework.views import APIView
from rest_framework.response import Response

# from .s import Nodes

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .components.forms import EditTaskForm, AddTaskForm

from django.urls import reverse
# @csrf_exempt

from datetime import timedelta

@csrf_exempt
def add_task(request):
    # Logika dodawania nowego zadania
    if request.method == "POST":
        task_path = request.POST.get("path")
        if task_path:
            priority = request.POST.get("priority", 0)
            task = Task(path=task_path, priority=priority)
            task.save()
            return JsonResponse({"status": "success", "task_id": task.id})
        else:
            return JsonResponse({"status": "error", "message": "No path provided"})
    else:
        return JsonResponse(
            {"status": "error", "message": "Only POST method is allowed"}
        )


@csrf_exempt
def get_task(request):
    if request.method == "GET":
        task = Task.objects.filter(status="waiting").order_by("id").first()
        if task:
            task.status = "running"
            task.start_time = timezone.now()  # Ustaw czas rozpoczęcia zadania
            task.save()
            return JsonResponse(
                {"status": "success", "task_id": task.id, "path": task.path}
            )
        else:
            return JsonResponse({"status": "error", "message": "No waiting tasks"})
    else:
        return JsonResponse(
            {"status": "error", "message": "Only GET method is allowed"}
        )


@csrf_exempt
def finish_task(request):
    if request.method == "POST":
        task_id = request.POST.get("task_id")
        if task_id:
            try:
                task = Task.objects.get(id=task_id, status="running")
                task.status = "finished"
                task.end_time = timezone.now()  # Ustaw czas zakończenia zadania
                task.save()
                return JsonResponse({"status": "success", "message": "Task finished"})
            except Task.DoesNotExist:
                return JsonResponse(
                    {"status": "error", "message": "Task not found or not running"}
                )
        else:
            return JsonResponse({"status": "error", "message": "No task ID provided"})
    else:
        return JsonResponse(
            {"status": "error", "message": "Only POST method is allowed"}
        )


def index(request):
    tasks = Task.objects.all()
    return render(request, "scheduler/index.html", {"tasks": tasks})


@csrf_exempt
def pause_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.status = "paused"
    task.save()
    return redirect("index")  # Powrót do strony głównej


@csrf_exempt
def resume_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if task.status == "paused":
        task.status = "waiting"
        task.save()
    return redirect("index")


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


def task_list(request):
    
    waiting_tasks = Task.objects.filter(status='waiting')
    active_tasks = Task.objects.filter(status='running')
    finished_tasks = Task.objects.filter(status='finished')
    
    tasks = Task.objects.all()
    for task in tasks:
        task.est = format_timedelta(task.est) if task.est else None

    return render(request, "manager/task_list.html", {"tasks": waiting_tasks,"active_tasks": active_tasks})

def format_timedelta(td):
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"




# @csrf_exempt
# async def send_command(request):
#     # Pobierz wiadomość od klienta
#     # Prześlij wiadomość do głównego serwera
#     channel_layer = get_channel_layer()
#     await channel_layer.group_send(
#         "nodes_group",
#         {
#             "type": "node.command",
#             "command": "update_gpus",
#         }
#     )
#     return JsonResponse({"message": "Uknown action."})

class NodeListView(APIView):
    def get(self, request, *args, **kwargs):
        path = request.path_info.split("/")[-2]
        if path =="refresh_all_nodes":
            n_monitor = NodesMonitor()
            n_monitor.send_update_command()
            nodes = Nodes.objects.all()
            return Response({"message": f"GPU przypisane do Node."}, status=200)

        else:
            node_id = kwargs.get("node_id")
            action = request.query_params.get("action")
            if node_id and action == "remove":
                return self.remove_node(request, node_id)
            elif node_id and action == "manage":
                return self.manage_node(request, node_id)
            elif node_id and action == "refresh_gpus":
                return self.refresh_gpus(request, node_id)
            else:
                nodes = Nodes.objects.all()
                return render(request, "manager/node_list.html", {"nodes": nodes})

    def remove_node(self, request, node_id):
        # Logika do usunięcia węzła i zakończenia połączenia
        node = get_object_or_404(Nodes, id=node_id)
        node.delete()
        nodes = Nodes.objects.all()
        return render(request, "manager/node_list.html", {"nodes": nodes})

    def assign_gpus(self, request, node_id):
        # Logika do przypisania węzłów GPU
        node = get_object_or_404(Nodes, id=node_id)

        # Zaktualizuj informacje o GPU dla węzła, jeśli potrzeba
        return Response({"message": f"GPU przypisane do Node {node_id}."}, status=200)

    def manage_node(self, request, node_id):
        # Logika do wyświetlenia szczegółów i zarządzania konkretnym węzłem
        gpu_list = Gpus.objects.all()
        gpus = Gpus.objects.filter(node_id=node_id)
        return render(request, "manager/node_manage.html", {"gpus": gpus,"node_id":1})

        
    # def refresh_gpus(self,request, node_id):
    #     channel_layer = get_channel_layer()
    #     async_to_sync(channel_layer.group_send)(
    #         "nodes_group",
    #         {
    #             "type": "node.command",
    #             "command": "update_gpus",
    #             "node_id":node_id,
    #         }
    #     )
    #     gpus = Gpus.objects.filter(node_id=node_id)
    #     # Przekierowanie z powrotem do strony zarządzania nodem
    #     return redirect(reverse('manage_node', kwargs={'node_id': node_id}))

    def refresh_gpus_ajax(request, node_id):
        
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "nodes_group",
            {
                "type": "node.command",
                "command": "update_gpus",
                "node_id":node_id,
            }
        )
        
        gpus = Gpus.objects.filter(node_id=node_id)
        gpus_data = [
            {
                'id': gpu.id,
                'brand_name': gpu.brand_name,
                'gpu_speed': gpu.gpu_speed,
                'gpu_util': gpu.gpu_util,
                'is_running_amumax': gpu.is_running_amumax,
                'gpu_info': gpu.gpu_info,
                'status': gpu.status,
                'node_id':node_id,
                'last_update': gpu.last_update.strftime('%Y-%m-%d %H:%M:%S') if gpu.last_update else None
            }
            for gpu in gpus
        ]
        
        return JsonResponse({'gpus': gpus_data})

class NodeManagementView(APIView):
    @csrf_exempt
    def post(self, request, format=None):
        action = request.data.get("action")

        if action == "assign_new_node":
            return self.assign_new_node(request)
        elif action == "update_node_status":
            return self.update_node_status(request)
        elif action == "assign_node_gpu":
            return self.assign_node_gpu(request)
        elif action == "update_node_gpu_status":
            return self.update_node_gpu_status(request)
        else:
            return Response({"message": "Uknown action."}, status=400)

    def assign_new_node(self, request):
        ip = request.data.get("ip")
        port = request.data.get("port")
        gpu_info = request.data.get("gpu_info")

        node, created = Nodes.objects.get_or_create(
            ip=ip,
            port=port,
            defaults={"gpu_info": gpu_info, "last_seen": timezone.now()},
        )

        if created:
            return Response(
                {"message": "Node assigned sucessfull.", "id": node.id}, status=201
            )
        else:
            # Aktualizuj istniejący węzeł
            node.gpu_info = gpu_info
            node.last_seen = timezone.now()
            node.save()
            return Response(
                {"message": "Node status updated.", "id": node.id}, status=201
            )

    def get_gpu_performance_category(self,gpu_model):
        gpu_performance = {
            "NVIDIA GeForce GTX 960": "slow",
            "NVIDIA GeForce GTX 970": "slow",
            "NVIDIA GeForce GTX 980": "slow",
            "NVIDIA GeForce GTX 980 Ti": "slow",
            "NVIDIA GeForce GTX 1050": "slow",
            "NVIDIA GeForce GTX 1050 Ti": "slow",
            "NVIDIA GeForce GTX 1060": "medium",
            "NVIDIA GeForce GTX 1070": "medium",
            "NVIDIA GeForce GTX 1070 Ti": "medium",
            "NVIDIA GeForce GTX 1080": "medium",
            "NVIDIA GeForce GTX 1080 Ti": "medium",
            "NVIDIA GeForce RTX 2060": "medium",
            "NVIDIA GeForce RTX 2070": "fast",
            "NVIDIA GeForce RTX 2080": "fast",
            "NVIDIA GeForce RTX 2080 Ti": "fast",
            "NVIDIA GeForce RTX 3060": "medium",
            "NVIDIA GeForce RTX 3060 Ti": "medium",
            "NVIDIA GeForce RTX 3070": "fast",
            "NVIDIA GeForce RTX 3070 Ti": "fast",
            "NVIDIA GeForce RTX 3080": "fast",
            "NVIDIA GeForce RTX 3080 Ti": "fast",
            "NVIDIA GeForce RTX 3090": "fast",
            "NVIDIA GeForce RTX 4070": "fast",
            "NVIDIA GeForce RTX 4070 Ti": "fast",
            # Dodaj więcej modeli zgodnie z potrzebą
        }
        return gpu_performance.get(gpu_model, "Unknown")

    def assign_node_gpu(self, request):
        

        temp_node_id = request.data.get("node_id")
        node_id = get_object_or_404(Nodes, id=temp_node_id)
        brand_name = request.data.get("brand_name")
        gpu_speed = request.data.get("gpu_speed")
        gpu_util = request.data.get("gpu_util")
        gpu_info = request.data.get("gpu_info")
        status = request.data.get("status")
        is_running_amumax = request.data.get("is_running_amumax")  
        gpu_uuid = request.data.get("gpu_uuid")

        gpu, created = Gpus.objects.get_or_create(
            node_id=node_id,
            gpu_uuid=gpu_uuid,
            defaults={
                "brand_name": brand_name,
                "gpu_speed": self.get_gpu_performance_category(brand_name),
                "gpu_info": gpu_info,
                "gpu_util": gpu_util,
                "is_running_amumax":    is_running_amumax,
                "gpu_speed": str(self.get_gpu_performance_category(brand_name)),
                "status": status,
                "last_update": timezone.now(),
            },
        )

        if created:
            return Response(
                {"message": "Gpu assigned sucessfull.", "gpu_uudid": gpu_uuid}, status=200
            )

        else:
            gpu.brand_name = brand_name
            gpu.gpu_speed = str(self.get_gpu_performance_category(brand_name))
            gpu.gpu_util = gpu_util
            gpu.gpu_info = gpu_info
            gpu.status = status
            gpu.is_running_amumax = is_running_amumax
            gpu.last_update = timezone.now()
            gpu.save()
            return Response(
                {"message": "Gpu status updated.", "gpu_uudid": gpu_uuid}, status=201
            )

    def update_node_status(self, request):
        pass

    def update_node_gpu_status(self, request):
        try:
            gpu_uuid = request.data.get("gpu_uuid")
            node_id = request.data.get("node_id")

            gpu = Gpus.objects.get(node_id=node_id, gpu_uuid=gpu_uuid)
            gpu.brand_name = request.data.get("brand_name")
            gpu.gpu_speed = str(self.get_gpu_performance_category(request.data.get("brand_name")))
            gpu.gpu_util = request.data.get("gpu_util")
            gpu.is_running_amumax = request.data.get("is_running_amumax")
            gpu.gpu_info = request.data.get("gpu_info")
            gpu.status =  request.data.get("status")
            gpu.last_update = timezone.now()
            gpu.save()
            return Response(
                {"message": "Gpu status updated.", "id": gpu.id}, status=200
            )
        except Gpus.DoesNotExist:
            # Tutaj możesz obsłużyć sytuację, gdy rekord GPU nie istnieje.
            # Możesz zwrócić błąd lub po prostu nie robić nic.
            return Response(
                {"message": "Gpu not found."}, status=404
            )

class GpusListView(APIView):
    def get(self, request, *args, **kwargs):
        action = request.data.get("action")
        gpus = Gpus.objects.all()
        return render(request, "manager/gpus_list.html", {"gpus": gpus})
    

class TaskManagerView(APIView):

    def get(self, request, *args, **kwargs):
        path = request.path_info.split("/")[-3]
        task_id = kwargs.get("task_id")
        if path == "edit":
            # Return the response from the edit_task method
            return self.edit_task(request, task_id=task_id)
        elif path == "delete":
            # Return the response from the edit_task method
            return self.delete_task(request, task_id=task_id)
        else:
            form = AddTaskForm()
            return render(request, 'manager/task_form.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = AddTaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("task_list")
        else:
            return render(request, 'manager/task_form.html', {'form': form})
        
    @csrf_exempt
    def edit_task(self, request, task_id):
        task = get_object_or_404(Task, pk=task_id)
        if request.method == "POST":
            form = EditTaskForm(request.POST, instance=task)
            if form.is_valid():
                form.save()
                return redirect("task_list")
        else:
            form = EditTaskForm(instance=task)
        
        return render(request, "manager/edit_task.html", {"form": form})

    @csrf_exempt
    def delete_task(self, request, task_id):
        task = get_object_or_404(Task, pk=task_id)
        task.delete()
        return redirect("task_list")


class TaskRunView(APIView):
    def get(self, request, task_id,action):
        # Wybór odpowiedniej akcji na podstawie ścieżki
        if action == 'run':
            return self.run_task(task_id,request)
        elif action == 'cancel':
            return self.cancel_task(task_id,request)
        elif action == 'redo':
            return self.redo_task(task_id,request)
        else:
            return HttpResponse("Invalid action", status=400)
    def get_task_list(self,request):
        waiting_tasks = Task.objects.filter(status='waiting')
        pending_tasks = Task.objects.filter(
                            Q(status='pending') | Q(status='running')
                        )
        # finished_tasks = Task.objects.filter(status='finished')
        
        tasks = Task.objects.all()
        for task in tasks:
            task.est = format_timedelta(task.est) if task.est else None

        return render(request, "manager/task_list.html", {"tasks": waiting_tasks,"active_tasks": pending_tasks})

    def select_gpu_for_task(self):
        # Przykładowa funkcja do wyboru GPU na podstawie wymagań zadania
        # Tutaj można dodać bardziej złożoną logikę dopasowania GPU do zadania
        return Gpus.objects.filter(status=0).first()
    
    def get_priority_task(self):
    # Przykładowa funkcja do wyboru najwyższego priorytetu zadania
        return Task.objects.filter(status='waiting').order_by('-priority').first()

    def run_task(self, task_id, request = None):
        task = self.get_priority_task() if task_id is None else Task.objects.get(id=task_id)
        if not task:
            return HttpResponse("No task available or specified task does not exist.", status=404)

        gpu = self.select_gpu_for_task()
        if not gpu:
            return HttpResponse("No available GPUs.", status=503)

        # Przydzielenie GPU do zadania i aktualizacja statusów
        task.assigned_gpu = f"N{gpu.node_id.id}/G{gpu.id}"
        task.assigned_node = f"{gpu.node_id.ip}"  # Convert gpu.node_id to a string
        task.status = 'pending'
        task.save()

        gpu.status = 'Bussy'
        gpu.task_id = str(task.id)  # Convert task.id to a string
        gpu.save()

        # Logika uruchomienia zadania na GPU

        return self.get_task_list(request)

    def cancel_task(self,task_id, request=None):
        task = Task.objects.get(id=task_id)
        task.assigned_gpu = None
        task.assigned_node = None
        task.status = 'waiting'
        task.save()

        gpu = Gpus.objects.get(id=task_id)
        gpu.status = 0
        gpu.task_id = None
        gpu.save()
        
        if request:
            return self.get_task_list(request)
        else:        
            return HttpResponse(f"Task {task_id} canceled.")


    def redo_task(self, task_id,request=None):
        # Logika ponownego uruchamiania zadania
        return HttpResponse(f"Task {task_id} redo initiated.")