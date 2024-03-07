import logging
import time

from django.core.cache import cache
from django.db.models import Case, IntegerField, Value, When

from manager.models import Gpu, Job

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

        return Gpu.objects.filter(status=Gpu.GPUStatus.PENDING.value).annotate(speed_as_number=speed_order).order_by("-speed_as_number").first()


    def schedule_jobs(self):
        """
        Schedule jobs to run on available GPUs. Wait and retry if no GPUs are available.
        """
        while True:
            for job in self.ordered_jobs:
                available_gpu = self.pending_gpus
                if available_gpu:
                    print(f"Running job {job.id} on GPU {available_gpu.id}")
                    # Tutaj implementujemy logikę uruchamiania zadania na wybranym GPU.
                    # Następnie aktualizujemy statusy zadań i GPU odpowiednio.
                    # Przykład aktualizacji statusu (zakładając, że statusy są odpowiednio obsługiwane w modelach):
                    job.status = Job.JobStatus.RUNNING # Przykładowa aktualizacja statusu zadania
                    job.gpu = available_gpu
                    job.save()

                    available_gpu.status = Gpu.GPUStatus.RUNNING.value  # Przykładowa aktualizacja statusu GPU
                    available_gpu.save()
                    break  # Wyjdź z pętli for, aby ponownie rozpocząć od nowych zadań w kolejce
                else:
                    # Jeśli nie ma dostępnych GPU, logujemy i czekamy
                    log.warning("No available GPUs. Waiting 30 seconds to retry...")
                    time.sleep(30)
                    break  # Wyjdź z pętli for, aby ponownie sprawdzić dostępność GPU po odczekaniu

            # Tutaj możemy dodać warunek wyjścia z nieskończonej pętli, na przykład:
            # if nie_ma_więcej_zadań_do_harmonogramu:
            #     break
            if not self.ordered_jobs.exists():
                # Jeśli nie ma więcej zadań oczekujących, kończymy planowanie
                print("No pending jobs left to schedule. Exiting scheduler.")
                break
