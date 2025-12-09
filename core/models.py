from django.db import models
from django.contrib.auth.models import User

class Device(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='devices')
    device_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.device_id})"


class DeviceData(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="data")
    nitrogen = models.FloatField()
    potassium = models.FloatField()
    phosphorus = models.FloatField()
    temperature = models.FloatField()
    humidity = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Data for {self.device.name} at {self.timestamp:%Y-%m-%d %H:%M}"
