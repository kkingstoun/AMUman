from django.core.cache import cache, caches
from django.db import models
from django.db.models import Case, IntegerField, Q, Value, When

from manager.components.run_job import RunJob
from manager.models import Gpu, Job


class QueueManager:
    """
    This class is responsible for managing the queue of jobs and assigning GPUs to jobs.

    Attributes:
        None

    Methods:
        ordered_jobs(self)
            Returns a list of jobs ordered by decreasing priority, decreasing GPU partition, and increasing submission time.

        waiting_gpus(self)
            Get the first available GPU from the waiting GPUs.

            The GPUs are ordered based on their speed, with fast GPUs coming first.

        schedule_jobs(self)
            For each job in the ordered jobs:
                Check if there is an available GPU.
                If there is, run the job on the GPU.
    """

    def __init__(self) -> None:
        # Ustawienie flagi
        cache.set("schedule_jobs", False)

    @property
    def ordered_jobs(self) -> models.QuerySet:
        """
        Returns a list of jobs ordered by decreasing priority, decreasing GPU partition, and increasing submission time.

        Returns:
            A list of jobs ordered by decreasing priority, decreasing GPU partition, and increasing submission time.
        """
        return Job.objects.filter(
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
            Gpu.objects.filter(status="Waiting")
            .annotate(speed_as_number=speed_order)
            .order_by("-speed_as_number")
        )

        return gpus.first()

    def pause_jobs(self):
        import time

        """
        Pause all jobs in the queue.
        """
        while caches["schedule_jobs"]:
            time.sleep(10)

    def schedule_jobs(self):
        """
        Schedule jobs to run on available GPUs.

        This method iterates over the ordered jobs and assigns them to available GPUs.
        If there are no available GPUs, the jobs will remain in the queue until a GPU becomes available.
        """
        for job in self.ordered_jobs:
            if not cache.get("schedule_jobs", default=False):
                available_gpu = self.waiting_gpus
                if available_gpu:
                    print(f"Run job {job.id} on GPU {available_gpu.id}")
                    cache.set("schedule_jobs", False, timeout=300)
                    rt = RunJob()
                    rt.run_job(job, available_gpu)
            else:
                self.pause_jobs()
