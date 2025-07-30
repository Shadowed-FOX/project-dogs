# app/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import MessageChannel, Message
from django.contrib.auth.models import User
import logging

logger = logging.getLogger(__name__)


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.channel_id = self.scope["url_route"]["kwargs"]["channel_id"]
        self.room_group_name = f"chat_{self.channel_id}"
        logger.info(
            f"Connecting to channel {self.channel_id} for user {self.scope['user']}"
        )

        if await self.is_participant(self.scope["user"], self.channel_id):
            logger.info(f"User {self.scope['user']} is a participant")
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()
        else:
            logger.warning(f"User {self.scope['user']} not a participant")
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()
            # await self.close()

    async def disconnect(self, close_code):
        logger.info(f"Disconnecting from channel {self.channel_id}, code: {close_code}")
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        logger.info(f"Received message: {text_data}")
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        user = self.scope["user"]

        if user.is_authenticated:
            saved_message = await self.save_message(user, self.channel_id, message)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": message,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "created_at": saved_message.created_at.strftime("%Y-%m-%d %H:%M"),
                },
            )

    async def chat_message(self, event):
        logger.info(f"Broadcasting message: {event['message']}")
        await self.send(
            text_data=json.dumps(
                {
                    "message": event["message"],
                    "first_name": event["first_name"],
                    "last_name": event["last_name"],
                    "created_at": event["created_at"],
                }
            )
        )

    @database_sync_to_async
    def save_message(self, user, channel_id, content):
        channel = MessageChannel.objects.get(id=channel_id)
        message = Message.objects.create(channel=channel, user=user, content=content)
        logger.info(f"Saved message: {content} by {user}")
        return message

    @database_sync_to_async
    def is_participant(self, user, channel_id):
        return MessageChannel.objects.filter(id=channel_id, participants=user).exists()
