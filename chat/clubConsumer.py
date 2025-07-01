from channels.consumer import AsyncConsumer
from channels.exceptions import StopConsumer


class ClubConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        clubname = self.scope['url_route']['kwargs']['club']
        self.clubname = clubname
        await self.channel_layer.group_add(self.clubname, self.channel_name)
        await self.send({
            "type": "websocket.accept", 
            "message": "connected"
        })

    async def websocket_receive(self, event):
        await self.channel_layer.group_send(self.clubname, {
            "type": "chat.message", 
            "text": event['text']
        })

    async def chat_message(self, event):
        print(event)
        await self.send({
            "type": "websocket.send", 
            "text": event['text']
        })


    async def websocket_disconnect(self, event):
        
        self.channel_layer.group_discard(self.clubname, self.channel_name)
        raise StopConsumer