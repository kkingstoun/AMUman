import asyncio
import websockets
import json
from asgiref.sync import sync_to_async

async def get_node_id():
    from node.models import Local
    local_list = Local.objects.all()
    # print("LOCAL LIST:", local_list )
    for local in local_list: 
        pass
        # print("NODE ID:", local.node_id)

    node_setting = Local.objects.get(id=1)
    return node_setting.node_id

    
async def connect_to_master():
    # print("CONNECT")
    uri = "ws://localhost:8000/ws/node/"
    try:
        async with websockets.connect(uri) as websocket:
            await websocket.send(json.dumps({"message": "Hello from Node!"}))
            while True:
                try:
                    try:
                        node_id = await get_node_id()
                    except:
                        node_id = None
                    message = await websocket.recv()
                    print(message)
                    print(type(message))
                    data = json.loads(message)  
                    print(data)
                    if data.get("command") == "update_gpus":
                        print(f"Aktualizacja GPU od {node_id}")
                        await sync_to_async(test)(node_id)
                    else:
                        print("Otrzymane dane:", data)
                except websockets.ConnectionClosed:
                    print("Połączenie z serwerem WebSocket zostało zamknięte.")
                    break  # Zakończ pętlę, jeśli połączenie jest zamknięte
    except Exception as e:
        print(f"Błąd połączenia WebSocket: {e}")
        
def test(node_id):
    from node.functions.gpu_monitor import GPUMonitor
    GPUMonitor().update_gpu_status(node_id)
    
def start_client():
    # print("asdasdas")
    asyncio.run(connect_to_master())
