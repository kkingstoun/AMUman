from django.db import models



class Nodes(models.Model):
    ip = models.CharField(max_length=15)
    port = models.CharField(max_length=5)
    gpu_info = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.ip}:{self.port}"