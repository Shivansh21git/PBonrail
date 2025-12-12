from channels.generic.websocket import AsyncWebsocketConsumer
import json

class DeviceLiveConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.device_id = self.scope["url_route"]["kwargs"]["device_id"]

        # Join group named after device ID
        await self.channel_layer.group_add(
            self.device_id,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.device_id,
            self.channel_name
        )

    async def send_update(self, event):
        # "event" contains {"type": "...", "data": {...}}
        await self.send(text_data=json.dumps(event["data"]))
