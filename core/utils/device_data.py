# core/utils/device_data.py

from core.models import DeviceData


def get_latest_device_data(device):
    """
    Returns latest sensor data for a device as a Python dict.
    Returns None if no data exists.
    """

    latest = (
        DeviceData.objects
        .filter(device=device)
        .order_by("-timestamp")
        .first()
    )

    if not latest:
        return None

    return {
        "nitrogen": latest.nitrogen,
        "phosphorus": latest.phosphorus,
        "potassium": latest.potassium,
        "temperature": latest.temperature,
        "humidity": latest.humidity,
        "timestamp": latest.timestamp,
    }
