from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect

from rest_framework import viewsets
from common_models.models import *
from .serializers import TaskSerializer

# Tymczasowe wyłączenie tokenów
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from rest_framework.views import APIView
from rest_framework.response import Response

# from .s import Nodes

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .components.form import TaskForm


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


@csrf_exempt
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task.delete()
    return redirect("task_list")


def update_priority(request, task_id, priority):
    task = get_object_or_404(Task, id=task_id)
    task.priority = priority
    task.save()
    return redirect("index")


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


def task_list(request):
    tasks = Task.objects.all()
    return render(request, "master/task_list.html", {"tasks": tasks})


def edit_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("task_list")
    else:
        form = TaskForm(instance=task)
    return render(request, "master/edit_task.html", {"form": form})


@csrf_exempt
def send_command(request):
    command = request.POST.get("command", "default_command")
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "nodes_group",
        {
            "type": "node.command",
            "command": command,
        },
    )
    return JsonResponse({"status": "command_sent", "command": command})


class NodeListView(APIView):
    def get(self, request, *args, **kwargs):
        node_id = kwargs.get("node_id")
        action = request.query_params.get("action")
        if node_id and action == "remove":
            return self.remove_node(request, node_id)
        elif node_id and action == "manage":
            return self.manage_node(request, node_id)
        else:
            # Logika dla wyświetlania listy węzłów, jeśli nie ma node_id lub akcji
            nodes = Nodes.objects.all()
            return render(request, "master/node_list.html", {"nodes": nodes})

    def remove_node(self, request, node_id):
        # Logika do usunięcia węzła i zakończenia połączenia
        node = get_object_or_404(Nodes, id=node_id)
        node.delete()
        nodes = Nodes.objects.all()
        return render(request, "master/node_list.html", {"nodes": nodes})

    def assign_gpus(self, request, node_id):
        # Logika do przypisania węzłów GPU
        node = get_object_or_404(Nodes, id=node_id)

        # Zaktualizuj informacje o GPU dla węzła, jeśli potrzeba
        return Response({"message": f"GPU przypisane do Node {node_id}."}, status=200)

    def manage_node(self, request, node_id):
        # Logika do wyświetlenia szczegółów i zarządzania konkretnym węzłem
        gpu_list = Gpus.objects.all()
        for gpu in gpu_list:
            print(f"ID: {gpu.id}")
            print(f"GPU ID: {gpu.gpu_id}")
            print(f"Brand Name: {gpu.brand_name}")
            print(f"GPU Speed: {gpu.gpu_speed}")
            print(f"GPU Util: {gpu.gpu_util}")
            print(f"Is Running Amumax: {gpu.is_running_amumax}")
            print(f"GPU Info: {gpu.gpu_info}")
            print(f"Status: {gpu.status}")
            print(f"Last Update: {gpu.last_update}")
            print("\n")  # Dodaj pusty wiersz między rekordami

        gpus = Gpus.objects.filter(node_id=node_id)

        return render(request, "master/node_manage.html", {"gpus": gpus})


class NodeManagementView(APIView):
    @csrf_exempt
    def post(self, request, format=None):
        action = request.data.get("action")

        if action == "assign_new_node":
            return self.assign_new_node(request)
        elif action == "assign_gpu":
            return self.assign_gpu(request)
        elif action == "update_node_status":
            return self.update_node_status(request)
        elif action == "update_node_gpus_status":
            return self.update_node_gpus_status(request)
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
                {"message": "Node status updated.", "id": node.id}, status=200
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

    def assign_gpu(self, request):
        temp_node_id = request.data.get("node_id")
        node_id = get_object_or_404(Nodes, id=temp_node_id)
        brand_name = request.data.get("brand_name")
        gpu_speed = request.data.get("gpu_speed")
        gpu_util = request.data.get("gpu_util")
        gpu_info = request.data.get("gpu_info")
        status = request.data.get("status")
        gpu_id = request.data.get("gpu_id")

        gpu, created = Gpus.objects.get_or_create(
            node_id=node_id,
            gpu_id=gpu_id,
            defaults={
                "gpu_id": gpu_id,
                "brand_name": brand_name,
                "gpu_speed": self.get_gpu_performance_category(brand_name),
                "gpu_info": gpu_info,
                "status": status,
                "last_update": timezone.now(),
            },
        )

        if created:
            return Response(
                {"message": "Node assigned sucessfull.", "id": gpu_id}, status=201
            )

        else:
            gpu.brand_name = brand_name
            gpu.gpu_speed = str(self.get_gpu_performance_category(brand_name)),
            gpu.gpu_util = gpu_util
            gpu.gpu_info = gpu_info
            gpu.status = status
            gpu.last_update = timezone.now()
            gpu.save()
            return Response(
                {"message": "Node status updated.", "id": gpu.id}, status=200
            )

    def update_node_status(self, request):
        pass

    def update_node_gpus_status(self, request):
        pass
