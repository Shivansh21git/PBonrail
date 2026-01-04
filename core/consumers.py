from channels.generic.websocket import AsyncWebsocketConsumer
import json
from django.contrib.auth.models import AnonymousUser
from core.models import Device


class DeviceLiveConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]
        self.device_id = self.scope["url_route"]["kwargs"]["device_id"]
        self.group_name = f"device_{self.device_id}"

        # 🔐 Auth + ownership check
        if isinstance(user, AnonymousUser):
            await self.close()
            return

        if not Device.objects.filter(device_id=self.device_id, user=user).exists():
            await self.close()
            return
        
        # Join group named after device ID
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def send_update(self, event):
        # "event" contains {"type": "...", "data": {...}}
        await self.send(text_data=json.dumps(event["data"]))
