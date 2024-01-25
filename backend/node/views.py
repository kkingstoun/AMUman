from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from .functions.gpu_monitor import GPUMonitor
from django.views.decorators.csrf import csrf_exempt
from django.apps import apps

# from .singleton import CurrentJob
from rest_framework.parsers import JSONParser
from io import BytesIO

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
