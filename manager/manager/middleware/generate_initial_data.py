import random
from datetime import timedelta

from django.contrib.auth.models import User as AuthUser
from django.core.exceptions import MiddlewareNotUsed
from django.utils import timezone

from manager.models import Job, ManagerSettings


class GenerateRandomJobsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.generate_random_jobs()
        raise MiddlewareNotUsed(
            "GenerateRandomJobsMiddleware is disabled after initial use."
        )

    def generate_random_jobs(self):
        if not Job.objects.exists():
            auth_user = AuthUser(
                username="test_user",
                password="pbkdf2_sha256$720000$tRDhakRL29XgyoKxQQBY1L$1AdKFRIyKe1F8WJfkoPy8H1M/Z9IdYZcbI7G6S3MuO4=",
            )
            auth_user.save()
            # self.user = User(auth_user=auth_user)
            # self.user.save()
            for _ in range(10):
                submit_time = timezone.now() - timedelta(days=random.randint(0, 10))
                start_time = submit_time + timedelta(minutes=random.randint(1, 60))
                end_time = start_time + timedelta(hours=random.randint(1, 3))
                error_time = (
                    None
                    if random.choice([True, False])
                    else start_time + timedelta(minutes=random.randint(1, 30))
                )

                job = Job(
                    path=f"/example/path/{random.randint(1, 100)}",
                    port=random.randint(8000, 8999),
                    submit_time=submit_time,
                    start_time=start_time,
                    user=auth_user.username,
                    end_time=end_time,
                    error_time=error_time,
                    priority=random.choice([choice.name for choice in Job.JobPriority]),
                    gpu_partition=random.choice(
                        [choice.name for choice in Job.GPUPartition]
                    ),
                    duration=random.randint(1, 120),
                    status=random.choice([choice.value for choice in Job.JobStatus]),
                    node=None,
                    gpu=None,
                    output="Random output" if random.choice([True, False]) else None,
                    error="Random error" if random.choice([True, False]) else None,
                    flags="Random flags" if random.choice([True, False]) else None,
                )
                job.save()
            print("Successfully generated 10 random job entries")

    def __call__(self, request):
        response = self.get_response(request)
        return response


class InitializeManagerSettingsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.initialize_default_settings()
        raise MiddlewareNotUsed(
            "InitializeManagerSettingsMiddleware is disabled after initial use."
        )

    def initialize_default_settings(self):
        if not ManagerSettings.objects.exists():
            ManagerSettings.objects.create(queue_watchdog=False)
            print("Successfully created default ManagerSettings entry")

    def __call__(self, request):
        response = self.get_response(request)
        return response
