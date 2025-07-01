from channels.consumer import AsyncConsumer
from channels.exceptions import StopConsumer
from .hooks import add_channel_name_to_user
import json


class PersonalChatConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        try: 
            senderId = self.scope['url_route']['kwargs']['sender']

            await add_channel_name_to_user(senderId, self.channel_name)
            await self.send({
                "type": "websocket.accept"
            })
        except Exception as err:
            print(err)
            await self.send({
                "type": "websocket.disconnect"
            })
            raise StopConsumer

    async def websocket_receive(self, event):
        data = json.loads(event['text'])
        receiver_channel_name = data.get('cn')
        message = data.get('message')
        try:
            if not receiver_channel_name:
                await self.send({
                    "type": "websocket.disconnect", 
                    "text": "receiver_channel_name not found"
                })
                return 
            await self.channel_layer.send(receiver_channel_name, {
                "type": "chat.message", 
                "message": message
            })
        except:
            raise StopConsumer
        

    async def chat_message(self, event):
        await self.send({
            "type": "websocket.send", 
            "text": json.dumps(event["message"])
        })
        

    async def websocket_disconnect(self, event):
        await self.close()
        raise StopConsumer

            
        

    