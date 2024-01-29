from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from .functions.gpu_monitor import GPUMonitor
from django.views.decorators.csrf import csrf_exempt
from django.apps import apps
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from node.models import Local

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
    def post(self, request, *args, **kwargs):
        message = request.data.get("message")
        print(f"Message received from manager: {message}")
        return Response({"status": "received"})   
    
# @require_POST
# def receive_task(request):
#     try:
#         stream = BytesIO(request.body)
#         data = JSONParser().parse(stream)
#         serializer = TaskSerializer(data=data)

#         if serializer.is_valid():
#             task = serializer.save()  # Deserializacja do obiektu Task
#             # Zapisz lub przetwarzaj zadanie
#             return JsonResponse({'status': 'success', 'message': 'Task received successfully.'})
#         return JsonResponse({'status': 'error', 'message': 'Invalid task data'}, status=400)
#     except Exception as e:
#         return JsonResponse({'status': 'error', 'message': str(e)})
# async def send_message(request):
#     # Pobierz wiadomość od klienta
#     message = request.POST.get("message", "")

#     # Prześlij wiadomość do głównego serwera
#     channel_layer = get_channel_layer()
#     async_to_sync(channel_layer.group_send)(
#         "nodes_group",
#         {
#             "type": "node.command",
#             "command": message,
#         }
#     )
#     import websockets
#     uri = "ws://localhost:8001/ws/node/"  # Adres serwera WebSocket
#     async with websockets.connect(uri) as websocket:
#         # Możesz tutaj wysłać jakieś dane lub po prostu nasłuchiwać
#         await websocket.send(json.dumps({"message": "Hello from Node!"}))
#         while True:
#             message = await websocket.recv()
#             print(f"Otrzymano wiadomość: {message}")
         
    
    # return JsonResponse({"status": "success"})
    
    
    
    

class TaskRunView(APIView):
    def get(self, request, task_id=None,action=None):
        # Wybór odpowiedniej akcji na podstawie ścieżki
        if action == 'run':
            return self.run_task(task_id,request)
        elif action == 'cancel':
            return self.cancel_task(task_id,request)
        elif action == 'redo':
            return self.redo_task(task_id,request)
        else:
            return self.get_task_list(request)
        
    async def get_task_list(self,request):
        node_id = await sync_to_async(Local.objects.get, thread_sensitive=True)(id=1)
        waiting_tasks = Task.objects.filter(status='pending',node_id=node_id)
        # finished_tasks = Task.objects.filter(status='finished')
        
        tasks = Task.objects.all()
        for task in tasks:
            task.est = format_timedelta(task.est) if task.est else None

        return render(request, "manager/task_list.html", {"tasks": waiting_tasks,"active_tasks": active_tasks})

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
        task.assigned_gpu_id = f"N{gpu.node_id.id}/G{gpu.id}"
        task.assigned_node_id = f"{gpu.node_id.ip}"  # Convert gpu.node_id to a string
        task.status = 'Running'
        task.save()

        gpu.status = 'Bussy'
        gpu.task_id = str(task.id)  # Convert task.id to a string
        gpu.save()

        # Logika uruchomienia zadania na GPU

        return self.get_task_list(request)

    def cancel_task(self,task_id, request=None):
        task = Task.objects.get(id=task_id)
        task.assigned_gpu_id = None
        task.assigned_node_id = None
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