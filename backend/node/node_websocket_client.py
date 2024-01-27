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
    while True:
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
                        data = json.loads(message)  
                        if data.get("command") == "update_gpus":
                            await sync_to_async(execute_update_gpus)(node_id)
                        else:
                            pass
                            # print("Otrzymane dane:", data)
                    except websockets.ConnectionClosed:
                        print("\033[91mConnection to the WebSocket server closed.\033[0m")
                        for i in range(10, 0, -1):
                            print(f"\033[93mReconnecting in {i}...\033[0m", end=" ", flush=True)
                            await asyncio.sleep(1)
                        
                        break  # Zakończ pętlę, jeśli połączenie jest zamknięte
        except Exception as e:
            print(f"\033[91mWebSocket connection error: {e}\033[0m")
            
def execute_update_gpus(node_id):
    from node.functions.gpu_monitor import GPUMonitor
    GPUMonitor().submit_update_gpu_status(node_id)
    
def start_client():
    # print("asdasdas")
    asyncio.run(connect_to_master())
