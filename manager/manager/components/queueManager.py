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
        job_order = Case(
            When(priority=Job.JobPriority.URGENT.value, then=Value(2)),
            When(priority=Job.JobPriority.NORMAL.value, then=Value(1)),
            default=Value(0),
            output_field=IntegerField(),
        )
        return (
            Job.objects.filter(status__in=[Job.JobStatus.PENDING.value, Job.JobStatus.INTERRUPTED.value, Job.JobStatus.CALC_ERROR.value])
            .annotate(priority_as_number=job_order)
            .order_by("-priority_as_number")
            .first()
        )

    @property
    def connection_lost_jobs(self):

        return (
            Job.objects.filter(status__in=[Job.JobStatus.CONNECTION_LOST.value])
        )

    @property
    def pending_gpus(self):
        return Gpu.objects.filter(status=Gpu.GPUStatus.PENDING.value).order_by("speed_score").first()


    def prepare_job(self):
        """
        Schedule jobs to run on available GPUs. Wait and retry if no GPUs are available.
        """
        #log.warning("test")
        conn_lost_job = self.connection_lost_jobs

        for job in conn_lost_job:
            run_job(job=job, gpu=job.gpu)

        job = self.ordered_jobs
        if job:
            available_gpu = self.pending_gpus
            if available_gpu:
                    run_job(job=job, gpu=available_gpu)
                # Exit the for loop to start over with new tasks in the queue
            else:
                # If no GPUs are available, log and wait
                log.warning("No available GPUs. Waiting 30 seconds to retry...")
                time.sleep(30)

            # Here we can add a condition to exit the infinite loop, for example:
            # if no_more_tasks_to_schedule:
            #     break
        else:
            # If there are no more pending jobs, we finish scheduling
            log.debug("No pending jobs left to schedule. Exiting scheduler.")
            # break
