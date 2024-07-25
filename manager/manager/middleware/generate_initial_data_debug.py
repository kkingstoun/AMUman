import logging
import random
from datetime import timedelta

from django.contrib.auth.models import User as AuthUser
from django.core.exceptions import MiddlewareNotUsed
from django.utils import timezone

from manager.models import CustomUser, Job

log = logging.getLogger("rich")


class Generate:
    def __init__(self, get_response):
        self.get_response = get_response
        self.generate_users()
        self.generate_random_jobs()
        raise MiddlewareNotUsed("Generate is disabled after initial use.")

    def generate_users(self):
        if not CustomUser.objects.exists():
            test_user_auth = AuthUser.objects.create_user(
                username="test_user",
                password="pbkdf2_sha256$720000$tRDhakRL29XgyoKxQQBY1L$1AdKFRIyKe1F8WJfkoPy8H1M/Z9IdYZcbI7G6S3MuO4=",
            )
            test_user_auth.save()
            self.test_user = CustomUser(auth=test_user_auth, concurrent_jobs=10)
            self.test_user.save()
            admin = AuthUser.objects.get(username="admin")
            self.admin_user = CustomUser(auth=admin, concurrent_jobs=20)
            self.admin_user.save()

    def generate_random_jobs(self):
        if not Job.objects.exists():
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
                    path="/app/node/amuman_node/bench.mx3",
                    port=random.randint(8000, 8999),
                    submit_time=submit_time,
                    start_time=start_time,
                    user=random.choice([self.test_user, self.admin_user]),
                    end_time=end_time,
                    error_time=error_time,
                    priority=random.choice([choice.name for choice in Job.JobPriority]),
                    gpu_partition=random.choice(
                        [choice.name for choice in Job.GPUPartition]
                    ),
                    duration=random.randint(1, 120),
                    status=random.choice([choice.value for choice in [Job.JobStatus.PENDING, Job.JobStatus.INTERRUPTED]]),
                    node=None,
                    gpu=None,
                    output="Random output" if random.choice([True, False]) else None,
                    error="Random error" if random.choice([True, False]) else None,
                    flags="Random flags" if random.choice([True, False]) else None,
                )
                job.save()
            log.debug("Successfully generated 10 random job entries")

    def __call__(self, request):
        response = self.get_response(request)
        return response
