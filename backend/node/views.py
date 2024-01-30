from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from .functions.gpu_monitor import GPUMonitor
from django.views.decorators.csrf import csrf_exempt
from django.apps import apps
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# from .singleton import CurrentJob
from rest_framework.parsers import JSONParser
from io import BytesIO
from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse
from common_models.models import *


from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

class NodeReportView(APIView):
    def post(self, request, format=None):
        # Tutaj logika zgłaszania obecności
        data = {
            'ip': request.data.get('ip', 'Brak IP'),
            'port': request.data.get('port', 'Brak portu'),
            'gpu_info': request.data.get('gpu_info', 'Brak informacji o GPU'),
        }
        return Response(data)
 
@csrf_exempt
def get_gpu_status(request): 
    if request.method == 'POST':
        gpu_index = request.POST.get('gpu_index', None)
        print(f"GPU_INDEX {gpu_index},{type(gpu_index)}")
        if gpu_index is not None and gpu_index != "":
            gpu_index = int(gpu_index)

        gpu_status = request.gpu_monitor.check_gpu_status(gpu_index=gpu_index)
        return JsonResponse(gpu_status)
    else:
        return JsonResponse({'error': 'You have to use POST METHOD'}, status=400)
 
class NodeMessageReceiver(APIView):
    def get(self, request, *args, **kwargs):
        message = request.data.get("message")
        print(f"Message received from manager: {message}")
        return Response({"status": "received"})   
    
class TaskRunView(APIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]

    def get(self, request, action, *args, **kwargs):
        task_id = kwargs.get("task_id")
        methods = {
            "edit": self.edit_task,
            "delete": self.delete_task,
            "run": self.run_task,
            "cancel": self.cancel_task,
            "redo": self.redo_task,
            "add_task": self.add_task_form
        }

        if action in methods:
            return methods[action](request, task_id=task_id)
        else:
            # Redirect or return JSON response for invalid action
            if request.accepted_renderer.format == "json":
                return Response({"error": "Invalid action"}, status=400)
            else:
                return redirect("task_list")
            
from django.db.models import Q   
     
class TaskListView(APIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    def get(self, request):
        waiting_tasks = Task.objects.filter(
            Q(status="Waiting") | Q(status="Waiting") | Q(status="Interrupted") | Q(status=None)
        )
        pending_tasks = Task.objects.filter(
            Q(status="Pending") | Q(status="Running") | Q(status=None)
        )

        tasks = Task.objects.all()
        data = {
            "tasks": waiting_tasks,
            # "tasks": tasks,
            "active_tasks": pending_tasks
        }

        if request.accepted_renderer.format == "json":
            return Response(data)

        return Response(data, template_name="node/task_list.html")
