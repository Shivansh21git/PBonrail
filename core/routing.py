from django.urls import re_path
from .consumers import DeviceLiveConsumer

websocket_urlpatterns = [
    re_path(r"ws/device/(?P<device_id>[\w-]+)/$", DeviceLiveConsumer.as_asgi()),
]
