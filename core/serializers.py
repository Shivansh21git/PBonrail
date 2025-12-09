# core/serializers.py
from rest_framework import serializers
from .models import DeviceData, Device

class DeviceDataSerializer(serializers.ModelSerializer):
    # accept device_id (string) in incoming JSON
    device_id = serializers.CharField(write_only=True)

    class Meta:
        model = DeviceData
        # include fields you want returned/accepted
        fields = ("id", "device_id", "nitrogen", "phosphorus", "potassium",
                  "temperature", "humidity", "timestamp")
        read_only_fields = ("id", "timestamp")

    def validate_device_id(self, value):
        try:
            Device.objects.get(device_id=value)
        except Device.DoesNotExist:
            raise serializers.ValidationError("Device not found")
        return value

    def create(self, validated_data):
        device_id = validated_data.pop("device_id")
        device = Device.objects.get(device_id=device_id)
        # create DeviceData linked to the device
        return DeviceData.objects.create(device=device, **validated_data)
