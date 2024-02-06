import json
import time

from asgiref.sync import async_to_sync

# from .components.nodes_monitor import NodesMonitor
from channels.layers import get_channel_layer
from manager.models import Gpus, ManagerSettings, Nodes, Task
from django.contrib import messages
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from manager.components.scheduler import ThreadedScheduler

from .components.forms import AddTaskForm, EditTaskForm, SettingsForm
from .components.queue import QueueManager
from .components.run_task import RunTask
from .serializers import TaskSerializer

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
            # n_monitor = NodesMonitor()
            # n_monitor.send_update_command()
            nodes = Nodes.objects.all()
            return Response({"message": "GPU przypisane do Node."}, status=200)

        else:
            node_id = kwargs.get("node_id")
            action = request.query_params.get("action")
            if node_id and action == "remove":
                return self.remove_node(request, node_id)
            elif node_id and action == "manage":
                return self.manage_node(request, node_id)
            # elif node_id and action == "refresh_gpus":
            #     return self.refresh_gpus(request, node_id)
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
        gpu_count = Gpus.objects.filter(node_id=node_id).count()
        return render(
            request,
            "manager/node_manage.html",
            {"gpus": gpus, "node_id": node_id, "gpu_count": gpu_count},
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
        name = request.data.get("node_name")

        node, created = Nodes.objects.get_or_create(
            name=name,
            defaults={
                "status": "Connected",
                "gpu_info": gpu_info,
                "last_seen": timezone.now(),
            },
        )

        if created:
            return Response(
                {"message": "Node assigned sucessfull.", "id": node.id}, status=200
            )
        else:
            # Aktualizuj istniejący węzeł
            node.gpu_info = gpu_info
            node.ip = ip
            node.connection_status = "Connected"
            node.name = name
            node.last_seen = timezone.now()
            node.save()
            return Response(
                {"message": "Node status updated.", "id": str(node.id)}, status=201
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

        with transaction.atomic():  # Używamy transakcji, aby zapewnić spójność danych
            # Sprawdzamy, czy istnieje już GPU o danym UUID
            existing_gpu = Gpus.objects.filter(gpu_uuid=gpu_uuid).first()

            if existing_gpu:
                old_node = existing_gpu.node_id
                Nodes.objects.filter(
                    id=old_node.id
                ).delete()  # Usuwamy wszystkie GPU powiązane ze starym węzłem
                old_node.delete()  # Następnie usuwamy stary węzeł

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
            "edit_task": self.edit_task,
            "get_task": self.get_task,
            "delete_task": self.delete_task,
            "run_task": self.run_task,
            "cancel_task": self.cancel_task,
            "redo_task": self.redo_task,
            "add_task": self.add_task,
            "task_output": self.task_output,
            "run_schedule": self.run_schedule,
            "stop_schedule": self.stop_schedule,
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
            return self.add_task(request)
        elif action == "edit_task":
            return self.edit_task(request, task_id=kwargs.get("task_id"))
        elif action == "get_task":
            return self.get_task(request, task_id=kwargs.get("task_id"))
        elif action == "run_task":
            return self.run_task(request, task_id=kwargs.get("task_id"))
        else:
            if request.accepted_renderer.format == "json":
                return Response({"error": "Invalid action"}, status=400)
            else:
                return redirect("task_list")

    @csrf_exempt
    def run_schedule(self, request, task_id):
        scheduler = ThreadedScheduler.get_instance()  # Pobierz instancję schedulera
        self.qm = QueueManager()
        scheduler.every(10).seconds.do(self.qm.schedule_tasks)
        scheduler.start()  # Uruchom scheduler, jeśli nie jest już uruchomiony
        return HttpResponse("Scheduler started.")

    @csrf_exempt
    def stop_schedule(self, request, task_id):
        scheduler = ThreadedScheduler.get_instance()  # Pobierz instancję schedulera
        scheduler.stop()  # Zatrzymaj scheduler
        return JsonResponse({"message": "Scheduler stopped!"}, status=200)

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
    def task_output(self, request, task_id=None):
        try:
            data = Task.objects.get(id=task_id)
            print(data.path)  # Assuming 'path' is an attribute of the Task model
        except Task.DoesNotExist:
            print("Task does not exist")
        if request.accepted_renderer.format == "json":
            return Response(data)

        return render(request, "manager/task_output.html", {"task": data})

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

    @csrf_exempt
    def run_task(self, request, task_id=None, gpu_id=None):
        task_data = (
            request.data
            if request.content_type == "application/json"
            else request.POST.dict()
        )
        task_id = task_data.get("task_id", task_id)
        task = get_object_or_404(Task, pk=task_id)

        gpu = Gpus.objects.filter(status="Waiting").first()
        if not gpu:
            return self.handle_response(request, "No available GPUs.", "danger", 400)

        self.rt = RunTask()
        self.rt.run_task(task=task, gpu=gpu, request=request)

    def handle_response(self, request, message, tag, status_code=200):
        if (
            request.accepted_renderer.format == "json"
            or request.content_type == "application/json"
        ):
            response_content = (
                {"message": message} if status_code == 200 else {"error": message}
            )
            return Response(response_content, status=status_code)
        else:
            # Add message for HTML response
            from django.contrib import messages

            if tag == "success":
                messages.success(request, message)
            elif tag == "danger":
                messages.error(request, message)
            else:
                messages.info(request, message)
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

    def add_task(self, request, *args, **kwargs):
        if request.method == "GET":
            form = AddTaskForm()
            return render(request, "manager/task_form.html", {"form": form})

        elif request.method == "POST":
            if request.content_type == "application/json":
                # Handle JSON data
                data = JSONParser().parse(request)
                serializer = TaskSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse(serializer.data, status=201)
                else:
                    return JsonResponse(serializer.errors, status=400)
            else:
                # Handle form data
                form = AddTaskForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Task added successfully!")
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
        finished_tasks = Task.objects.filter(Q(status="Finished"))
        # tasks = Task.objects.all()
        data = {
            "tasks": waiting_tasks,
            # "tasks": tasks,
            "finished_tasks": finished_tasks,
            "active_tasks": pending_tasks,
        }

        if request.accepted_renderer.format == "json":
            return Response(data)

        return Response(data, template_name="manager/task_list.html")


def print_work(what_to_say: str):
    print(what_to_say)


@csrf_exempt
def settings_view(request):
    # Załóżmy, że istnieje tylko jeden obiekt ustawień, więc używamy `first()`
    settings_instance = ManagerSettings.objects.first()
    if request.method == "POST":
        form = SettingsForm(request.POST, instance=settings_instance)
        if form.is_valid():
            form.save()
            queue_watchdog_value = form.cleaned_data["queue_watchdog"]
            if queue_watchdog_value == True:
                try:
                    scheduler = (
                        ThreadedScheduler.get_instance()
                    )  # Pobierz instancję schedulera
                    scheduler.every(1).seconds.do(QueueManager().schedule_tasks)
                    scheduler.start()  # Uruchom scheduler, jeśli nie jest już uruchomiony
                except Exception as e:
                    print(e)
            else:
                try:
                    scheduler = (
                        ThreadedScheduler.get_instance()
                    )  # Pobierz instancję schedulera
                    scheduler.stop()  # Uruchom scheduler, jeśli nie jest już uruchomiony
                except Exception as e:
                    print(e)

            # Tutaj możesz dodać obsługę odpowiedzi JSON, jeśli jest potrzebna
            messages.success(
                request, "Settings updated successfully!", extra_tags="primary"
            )
            return redirect(
                "settings_view"
            )  # Zakładam, że 'settings_view' to nazwa URL widoku ustawień
    else:
        form = SettingsForm(instance=settings_instance)

    return render(request, "manager/manager_settings.html", {"form": form})


class ConsoleView(APIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]

    def get(self, request):
        return Response(template_name="manager/console.html")

    def post(self, request):
        pass
        # Logic to handle POST request
        # ...
