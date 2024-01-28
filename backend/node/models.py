from django.db import models

# Create your models here.
class Local(models.Model):
    id=models.IntegerField(primary_key=True)
    node_id = models.CharField(max_length=15, unique=True)  # Przykładowy format IPv4
    managerNmUrl = models.CharField(max_length=15,default='http://localhost:8000/manager/node-management/')  # Przykładowy format IPv4
    managerWsUrl = models.CharField(max_length=15,default="ws://localhost:8000/ws/node/")  # Przykładowy format IPv4
    
    def __str__(self):
        return f"{self.node_id}"