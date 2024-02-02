from django.apps import AppConfig
from rich.logging import RichHandler
import logging
import websockets
import requests

class MasterConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "manager"

    # logging.basicConfig(
    #     level="DEBUG",
    #     format="%(message)s",
    #     datefmt="[%X]",
    #     handlers=[
    #         RichHandler(rich_tracebacks=True, tracebacks_suppress=[websockets, requests])
    #     ],
    # )
    # log = logging.getLogger("rich")
    # logging.getLogger("websockets").setLevel(logging.WARNING)
    # logging.getLogger("urllib3").setLevel(logging.WARNING)