import logging
import time

from django.core.cache import cache
from django.db.models import Case, IntegerField, Value, When

from manager.models import Gpu, Job

from .run_job import run_job

log = logging.getLogger("rich")


class QueueManager:
    """
    This class is responsible for managing the queue of jobs and assigning GPUs to jobs.
    """

    def __init__(self) -> None:
        # Initialize scheduling control flag in cache
        cache.set("schedule_jobs", True)

    @property
    def ordered_jobs(self):
        """
        Returns a list of jobs ordered by decreasing priority, decreasing GPU partition, and increasing submission time.
        """
        return Job.objects.filter(
            status__in=[Job.JobStatus.PENDING.value, Job.JobStatus.INTERRUPTED.value]
        ).order_by("-priority", "-gpu_partition", "submit_time")

    @property
    def pending_gpus(self):
        """
        Get the first available GPU from the waiting GPUs.
        """
        speed_order = Case(
            When(speed=Gpu.GPUSpeed.FAST.value, then=Value(3)),
            When(speed=Gpu.GPUSpeed.NORMAL.value, then=Value(2)),
            When(speed=Gpu.GPUSpeed.SLOW.value, then=Value(1)),
            default=Value(0),
            output_field=IntegerField(),
        )

        return (
            Gpu.objects.filter(status=Gpu.GPUStatus.PENDING.value)
            .annotate(speed_as_number=speed_order)
            .order_by("-speed_as_number")
            .first()
        )

    def schedule_jobs(self):
        """
        Schedule jobs to run on available GPUs. Wait and retry if no GPUs are available.
        """
        log.debug("Starting job scheduling...")
        while True:
            for job in self.ordered_jobs:
                available_gpu = self.pending_gpus
                if available_gpu:
                    run_job(job=job, gpu=available_gpu)
                    # Exit the for loop to start over with new tasks in the queue
                else:
                    # If no GPUs are available, log and wait
                    log.warning("No available GPUs. Waiting 30 seconds to retry...")
                    time.sleep(30)
                    break  # Exit the for loop to recheck GPU availability after waiting

            # Here we can add a condition to exit the infinite loop, for example:
            # if no_more_tasks_to_schedule:
            #     break
            if not self.ordered_jobs.exists():
                # If there are no more pending jobs, we finish scheduling
                log.debug("No pending jobs left to schedule. Exiting scheduler.")
                break
