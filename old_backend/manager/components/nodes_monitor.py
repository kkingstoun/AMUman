# import asyncio
# from channels.layers import get_channel_layer


# class NodesMonitor:
#     def __init__(self):
#         pass

#     async def send_update_command(self):
#         try:
#             cl = get_channel_layer()
#             await cl.group_send(
#                 "nodes_group",
#                 {
#                     "type": "node.command",
#                     "command": "update_node_status",
#                 }
#             )
#         except Exception as e:
#             print(f"Cannot send update reqest throug websocket: {e}")
