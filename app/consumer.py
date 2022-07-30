import json
from time import sleep

from asgiref.sync import async_to_sync
from channels.consumer import SyncConsumer
from channels.db import database_sync_to_async
from channels.exceptions import StopConsumer
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from channels.layers import get_channel_layer

from app.models import  Chat


class MyConsumer(WebsocketConsumer):
    # This Handler is called when client initially open a connection and is about to finishing handshake

    def connect(self):
        print('Connection Connected')
        user = self.scope['user'].id
        receiver = self.scope['url_route']['kwargs']['pk']
        self.room_name = str(int(user) + int(receiver))
        self.room_group_name = self.room_name
        async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)
        self.accept()
        print(self.channel_layer)
        print(self.channel_name)

    # This Handler is called When data received from client

    def receive(self, text_data=None, bytes_data=None):
        print('Message Received', text_data)
        pk = self.scope['url_route']['kwargs']['pk']
        user = self.scope['user'].id
        data = json.loads(text_data)
        message = data['msg']
        chat = Chat(sender_id=user, receiver_id=pk, message=message,room_name = self.room_group_name)
        chat.save()
        async_to_sync(self.channel_layer.group_send)(
                        self.room_group_name,
                        dict(type='chat.message', message=message)
        )
        print(message)

    def chat_message(self, event):
        print(event)
        self.send(json.dumps({'msg': event['message']}))

    # This Handler is called when client lost the connection closing the connection the server lose the connection

    def disconnect(self, code):
        print('Connection Disconnected', code)
        raise StopConsumer()
