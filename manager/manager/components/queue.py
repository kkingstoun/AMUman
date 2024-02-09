from django.core.cache import cache, caches
from django.db import models
from django.db.models import Case, IntegerField, Q, Value, When

from manager.components.run_task import RunTask
from manager.models import Gpus, Task


class QueueManager:
    """
    This class is responsible for managing the queue of tasks and assigning GPUs to tasks.

    Attributes:
        None

    Methods:
        ordered_tasks(self)
            Returns a list of tasks ordered by decreasing priority, decreasing GPU partition, and increasing submission time.

        waiting_gpus(self)
            Get the first available GPU from the waiting GPUs.

            The GPUs are ordered based on their speed, with fast GPUs coming first.

        schedule_tasks(self)
            For each task in the ordered tasks:
                Check if there is an available GPU.
                If there is, run the task on the GPU.
    """

    def __init__(self) -> None:
        # Ustawienie flagi
        cache.set("schedule_tasks", False)

    @property
    def ordered_tasks(self) -> models.QuerySet:
        """
        Returns a list of tasks ordered by decreasing priority, decreasing GPU partition, and increasing submission time.

        Returns:
            A list of tasks ordered by decreasing priority, decreasing GPU partition, and increasing submission time.
        """
        return Task.objects.filter(
            Q(status="Waiting") | Q(status="Interrupted")
        ).order_by("-priority", "-gpu_partition", "submit_time")

    @property
    def waiting_gpus(self):
        """
        Get the first available GPU from the waiting GPUs.

        The GPUs are ordered based on their speed, with fast GPUs coming first.

        Returns:
            The first available GPU, or None if no GPUs are available.
        """
        speed_order = Case(
            When(gpu_speed="Fast", then=Value(3)),
            When(gpu_speed="Normal", then=Value(2)),
            When(gpu_speed="Slow", then=Value(1)),
            default=Value(0),
            output_field=IntegerField(),
        )

        gpus = (
            Gpus.objects.filter(status="Waiting")
            .annotate(speed_as_number=speed_order)
            .order_by("-speed_as_number")
        )

        return gpus.first()

    def pause_tasks(self):
        import time

        """
        Pause all tasks in the queue.
        """
        while caches["schedule_tasks"] == True:
            time.sleep(10)

    def schedule_tasks(self):
        """
        Schedule tasks to run on available GPUs.

        This method iterates over the ordered tasks and assigns them to available GPUs.
        If there are no available GPUs, the tasks will remain in the queue until a GPU becomes available.
        """
        for task in self.ordered_tasks:
            if cache.get("schedule_tasks", default=False) == False:
                available_gpu = self.waiting_gpus
                if available_gpu:
                    print(f"Run task {task.id} on GPU {available_gpu.id}")
                    cache.set("schedule_tasks", False, timeout=300)
                    rt = RunTask()
                    rt.run_task(task, available_gpu)
            else:
                self.pause_tasks()
