from celery import shared_task
from .management.commands.runnode import Command as RunNodeCommand

@shared_task(bind=True)
def run_node_at_startup(self):
    run_node_command = RunNodeCommand()
    run_node_command.handle()
