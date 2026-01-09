from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json

class DeviceLiveConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.device_id = self.scope["url_route"]["kwargs"]["device_id"]
        self.group_name = f"device_{self.device_id}"
        user = self.scope["user"]

        # 🔐 Auth check
        if not user or not user.is_authenticated:
            await self.close()
            return

        # 🔐 Ownership check (ASYNC SAFE)
        has_access = await self.user_has_device(user, self.device_id)
        if not has_access:
            await self.close()
            return

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
        await self.send(text_data=json.dumps(event["data"]))

    # ============================
    # SYNC ORM → ASYNC WRAPPER
    # ============================
    @database_sync_to_async
    def user_has_device(self, user, device_id):
        from core.models import Device
        return Device.objects.filter(
            device_id=device_id,
            user=user
        ).exists()
