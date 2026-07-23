from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

import json
from .models import Conversation, Message
from auth_network.models import User


class ChatConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		self.conversation_id = self.scope["url_route"]["kwargs"]["conversation_id"]
		print(self.scope['user'].id)

		self.room_group_name = f"chat_{self.conversation_id}"

		await self.channel_layer.group_add(
			self.room_group_name,
			self.channel_name
		)

		await self.accept()

	async def disconnect(self, close_code):
		await self.channel_layer.group_discard(
			self.room_group_name,
			self.channel_name
		)

	async def receive(self, text_data):
		data = json.loads(text_data)

		body = data["message"]

		message = await self.save_message(body)

		await self.channel_layer.group_send(
			self.room_group_name,
			{
				"type": "chat_message",
				"id": message.id,
				"sender": message.sender.username,
				"message": message.body,
				"created_at": message.created_at.strftime("%H:%M"),
			}
		)

	async def chat_message(self, event):
		await self.send(text_data=json.dumps(
		{
			"id": event["id"],
			"sender": event["sender"],
			"message": event["message"],
			"created_at": event["created_at"],
		})
	)

	@database_sync_to_async
	def save_message(self, body):
		conversation = Conversation.objects.get(
			id=self.conversation_id
		)

		message = Message.objects.create(
			conversation=conversation,
			sender=self.scope['user'],
			body=body
		)

		return message