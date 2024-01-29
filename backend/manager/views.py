from typing import Any
from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.urls import reverse

from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from common_models.models import *
from .components.forms import EditTaskForm, AddTaskForm
from .serializers import TaskSerializer
from .components.nodes_monitor import NodesMonitor

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from datetime import timedelta
import time
import json

# @csrf_exempt
# def add_task(request):
#     # Logika dodawania nowego zadania
#     if request.method == "POST":
#         task_path = request.POST.get("path")
#         if task_path:
#             priority = request.POST.get("priority", 0)
#             task = Task(path=task_path, priority=priority)
#             task.save()
#             return JsonResponse({"status": "success", "task_id": task.id})
#         else:
#             return JsonResponse({"status": "error", "message": "No path provided"})
#     else:
#         return JsonResponse(
#             {"status": "error", "message": "Only POST method is allowed"}
#         )


# @csrf_exempt
# def get_task(request):
#     if request.method == "GET":
#         task = Task.objects.filter(status="Waiting").order_by("id").first()
#         if task:
#             task.status = "Running"
#             task.start_time = timezone.now()  # Ustaw czas rozpoczęcia zadania
#             task.save()
#             return JsonResponse(
#                 {"status": "success", "task_id": task.id, "path": task.path}
#             )
#         else:
#             return JsonResponse({"status": "error", "message": "No waiting tasks"})
#     else:
#         return JsonResponse(
#             {"status": "error", "message": "Only GET method is allowed"}
#         )


# @csrf_exempt
# def finish_task(request):
#     if request.method == "POST":
#         task_id = request.POST.get("task_id")
#         if task_id:
#             try:
#                 task = Task.objects.get(id=task_id, status="Running")
#                 task.status = "Finished"
#                 task.end_time = timezone.now()  # Ustaw czas zakończenia zadania
#                 task.save()
#                 return JsonResponse({"status": "success", "message": "Task finished"})
#             except Task.DoesNotExist:
#                 return JsonResponse(
#                     {"status": "error", "message": "Task not found or not running"}
#                 )
#         else:
#             return JsonResponse({"status": "error", "message": "No task ID provided"})
#     else:
#         return JsonResponse(
#             {"status": "error", "message": "Only POST method is allowed"}
#         )
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class NodeListView(APIView):
    def get(self, request, *args, **kwargs):
        path = request.path_info.split("/")[-2]
        if path == "refresh_all_nodes":
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
        return render(
            request, "manager/node_manage.html", {"gpus": gpus, "node_id": node_id}
        )

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
    #     return redirect(reverse("manage_node", kwargs={"node_id": node_id}))

    def refresh_gpus_ajax(request, node_id):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "nodes_group",
            {
                "type": "node.command",
                "command": "update_gpus",
                "node_id": node_id,
            },
        )
        time.sleep(3)
        node = get_object_or_404(Nodes, id=node_id)
        if not node:
            return Response({"error": "Node not found."}, status=404)

        gpus = Gpus.objects.filter(node_id=node)
        if not gpus:
            return Response({"error": "No GPUs found for the given node."}, status=404)

        gpus_data = [
            {
                "id": gpu.id,
                "brand_name": gpu.brand_name,
                "gpu_speed": gpu.gpu_speed,
                "gpu_util": gpu.gpu_util,
                "is_running_amumax": gpu.is_running_amumax,
                "gpu_info": gpu.gpu_info,
                "status": gpu.status,
                "node_id": node_id,
                "last_update": gpu.last_update.strftime("%Y-%m-%d %H:%M:%S")
                if gpu.last_update
                else None,
            }
            for gpu in gpus
        ]

        return JsonResponse({"gpus": gpus_data})


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

    def get_gpu_performance_category(self, gpu_model):
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
                "is_running_amumax": is_running_amumax,
                "gpu_speed": str(self.get_gpu_performance_category(brand_name)),
                "status": status,
                "last_update": timezone.now(),
            },
        )

        if created:
            return Response(
                {"message": "Gpu assigned sucessfull.", "gpu_uudid": gpu_uuid},
                status=200,
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
            gpu.gpu_speed = str(
                self.get_gpu_performance_category(request.data.get("brand_name"))
            )
            gpu.gpu_util = request.data.get("gpu_util")
            gpu.is_running_amumax = request.data.get("is_running_amumax")
            gpu.gpu_info = request.data.get("gpu_info")
            gpu.status = request.data.get("status")
            gpu.last_update = timezone.now()
            gpu.save()
            return Response(
                {"message": "Gpu status updated.", "id": gpu.id}, status=200
            )
        except Gpus.DoesNotExist:
            # Tutaj możesz obsłużyć sytuację, gdy rekord GPU nie istnieje.
            # Możesz zwrócić błąd lub po prostu nie robić nic.
            return Response({"message": "Gpu not found."}, status=404)


class GpusListView(APIView):
    def get(self, request, *args, **kwargs):
        action = request.data.get("action")
        gpus = Gpus.objects.all()
        return render(request, "manager/gpus_list.html", {"gpus": gpus})


class TaskManagerView(APIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]

    def get(self, request, action, *args, **kwargs):
        task_id = kwargs.get("task_id")
        methods = {
            "edit": self.edit_task,
            "get_task": self.get_task,
            "delete": self.delete_task,
            "run": self.run_task,
            "cancel": self.cancel_task,
            "redo": self.redo_task,
            "add_task": self.add_task_form,
        }

        if action in methods:
            return methods[action](request, task_id=task_id)
        else:
            # Redirect or return JSON response for invalid action
            if request.accepted_renderer.format == "json":
                return Response({"error": "Invalid action"}, status=400)
            else:
                return redirect("task_list")

    def post(self, request, *args, **kwargs):
        action = kwargs.get("action")
        if action == "add_task":
            return self.add_task_form(request)
        elif action == "edit_task":
            return self.edit_task(request, task_id=kwargs.get("task_id"))
        elif action == "get_task":
            return self.get_task(request, task_id=kwargs.get("task_id"))
        else:
            if request.accepted_renderer.format == "json":
                return Response({"error": "Invalid action"}, status=400)
            else:
                return redirect("task_list")

    @csrf_exempt
    def get_task(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        serializer = TaskSerializer(task)
        return JsonResponse(serializer.data)

    @csrf_exempt
    def edit_task(self, request, task_id=None):
        from django.forms.models import model_to_dict

        task = get_object_or_404(Task, pk=task_id)
        if request.method == "POST":
            if request.headers.get("Content-Type") == "application/json":
                data = json.loads(request.body.decode("utf-8"))
                for key in data:
                    if key in model_to_dict(task):
                        setattr(task, key, data[key])
                task.save(update_fields=data.keys())
                return JsonResponse(
                    {"message": "Task updated successfully!"}, status=200
                )
            else:
                form = EditTaskForm(request.POST, instance=task)
                if form.is_valid():
                    form.save()
                    if (
                        request.accepted_renderer.format == "json"
                        or request.content_type == "application/json"
                    ):
                        return JsonResponse(
                            {"message": "Task updated successfully!"}, status=200
                        )
                    elif request.accepted_renderer.format == "html":
                        messages.success(
                            request, "Task updated successfully!", extra_tags="primary"
                        )
                        return redirect("task_list")
                    else:
                        return redirect("task_list")
        else:
            form = EditTaskForm(instance=task)
        if request.accepted_renderer.format == "json":
            return Response(form.errors, status=400)
        else:
            return render(
                request, "manager/edit_task.html", {"form": form, "task": task}
            )

    @csrf_exempt
    def delete_task(self, request, task_id=None):
        task = get_object_or_404(Task, pk=task_id)
        task.delete()
        if request.accepted_renderer.format == "json":
            return Response({"message": "Task deleted successfully"})
        elif request.accepted_renderer.format == "html":
            messages.success(
                request, "Task canceled successfully!", extra_tags="primary"
            )
            return redirect("task_list")
        else:
            return redirect("task_list")

    def select_gpu_for_task(self):
        return Gpus.objects.filter(status="Waiting").first()

    def get_priority_task(self):
        return Task.objects.filter(status="Waiting").order_by("-priority").first()

    def run_task(self, request, task_id=None):
        try:
            task = (
                self.get_priority_task()
                if task_id is None
                else get_object_or_404(Task, id=task_id)
            )
            gpu = self.select_gpu_for_task()
            if not gpu:
                message = "No available GPUs."
                if request.accepted_renderer.format == "json":
                    return Response({"error": message}, status=400)
                elif request.accepted_renderer.format == "html":
                    messages.success(request, message, extra_tags="danger")
                    return redirect("task_list")
                else:
                    return redirect(
                        "task_list"
                    )  ############ PROPABLY IT"s the same as above

            task.assigned_gpu_id = gpu.no
            task.assigned_node_id = f"{gpu.node_id.ip}"
            task.status = "Pending"
            task.submit_time = timezone.now()
            task.save()

            gpu.status = "Running"
            gpu.task_id = task
            gpu.last_update = timezone.now()
            gpu.save()

            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "nodes_group",
                {
                    "type": "node.command",
                    "command": "run_task",
                    "node_id": gpu.node_id.id,
                    "task_id": task.id,
                },
            )
            time.sleep(2)
            message = f"Task {task_id} is pending on {gpu.node_id.id}/{gpu.no}."
            if request.accepted_renderer.format == "json":
                return Response({"message": message})
            elif request.accepted_renderer.format == "html":
                messages.success(request, message, extra_tags="primary")
                return redirect("task_list")
            else:
                return redirect("task_list")
        except Exception as e:
            message = f"The task {task_id} has not been started. Error: {e}"
            if request.accepted_renderer.format == "json":
                return Response({"error": message}, status=400)
            elif request.accepted_renderer.format == "html":
                messages.success(request, message, extra_tags="danger")
                return redirect("task_list")
            else:
                return redirect("task_list")

    def cancel_task(self, request, task_id=None):
        try:
            task = get_object_or_404(Task, id=task_id)
            task.assigned_gpu_id = None
            task.assigned_node_id = None
            task.submit_time = None
            task.start_time = None
            task.port = None
            task.status = "Waiting"
            task.save()

            gpu = get_object_or_404(Gpus, task_id=task)
            gpu.status = "Waiting"
            gpu.task_id = None
            gpu.last_update = timezone.now()
            gpu.save()

            try:
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    "nodes_group",
                    {
                        "type": "node.command",
                        "command": "cancel_task",
                        "node_id": gpu.node_id.id,
                        "task_id": task.id,
                    },
                )
            except Exception as e:
                message = f"The task {task_id} canceladtion has not been canceled due to websocket problem. Error: {e}"
                if request.accepted_renderer.format == "json":
                    return Response({"error": message}, status=400)
                elif request.accepted_renderer.format == "html":
                    messages.success(request, message, extra_tags="danger")
                    return redirect("task_list")
                else:
                    return redirect("task_list")

            message = "Task cancelled."
            if request.accepted_renderer.format == "json":
                return Response({"message": message})
            elif request.accepted_renderer.format == "html":
                messages.success(request, message, extra_tags="primary")
                return redirect("task_list")
            else:
                return redirect("task_list")
        except Exception as e:
            message = f"Task has not been canceled. Error: {e}"
            if request.accepted_renderer.format == "json":
                return Response({"error": message}, status=400)
            elif request.accepted_renderer.format == "html":
                messages.success(request, message, extra_tags="danger")
                return redirect("task_list")
            else:
                return redirect("task_list")

    def redo_task(self, request, task_id=None):
        # Logic to redo the task
        # ...

        if request.accepted_renderer.format == "json":
            return Response({"message": f"Task {task_id} redo initiated"})
        else:
            return HttpResponse(f"Task {task_id} redo initiated")

    def add_task_form(self, request, task_id=None):
        if request.method == "GET":
            form = AddTaskForm()
            if request.accepted_renderer.format == "json":
                # W przypadku odpowiedzi JSON, zwracamy pustą strukturę formularza
                serializer = TaskSerializer(data=request.data)
                return Response(serializer.data)
            else:
                # W przypadku odpowiedzi HTML, renderujemy formularz HTML
                return render(request, "manager/task_form.html", {"form": form})

        elif request.method == "POST":
            # Obsługa żądania POST dla tworzenia nowego zadania
            if request.accepted_renderer.format == "json":
                data = JSONParser().parse(request)
                serializer = TaskSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=201)
                return Response(serializer.errors, status=400)
            else:
                form = AddTaskForm(request.POST)
                if form.is_valid():
                    form.save()
                    return redirect("task_list")
                else:
                    return render(request, "manager/task_form.html", {"form": form})


class TaskListView(APIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]

    def get(self, request):
        waiting_tasks = Task.objects.filter(
            Q(status="Waiting")
            | Q(status="Waiting")
            | Q(status="Interrupted")
            | Q(status=None)
        )
        pending_tasks = Task.objects.filter(
            Q(status="Pending") | Q(status="Running") | Q(status=None)
        )

        tasks = Task.objects.all()
        data = {
            "tasks": waiting_tasks,
            # "tasks": tasks,
            "active_tasks": pending_tasks,
        }

        if request.accepted_renderer.format == "json":
            return Response(data)

        return Response(data, template_name="manager/task_list.html")
