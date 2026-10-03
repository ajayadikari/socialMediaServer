from channels.consumer import AsyncConsumer
from channels.exceptions import StopConsumer
from .hooks import (
    add_channel_name_to_user,
    set_channel_name_to_null,
    get_user_channel_name,
)
import json


class PersonalChatConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        try:
            sender_id = self.scope["url_route"]["kwargs"]["sender"]

            await add_channel_name_to_user(
                sender_id,
                self.channel_name
            )

            await self.send({
                "type": "websocket.accept"
            })

        except Exception as err:
            print(err)

            await self.send({
                "type": "websocket.close"
            })

            raise StopConsumer()

    async def websocket_receive(self, event):
        try:
            data = json.loads(event["text"])

            receiver_id = data.get("receiver_id")
            message = data.get("message")

            if not receiver_id:
                await self.send({
                    "type": "websocket.send",
                    "text": json.dumps({
                        "error": "receiver_id is required"
                    })
                })
                return

            if not message:
                await self.send({
                    "type": "websocket.send",
                    "text": json.dumps({
                        "success": True,
                        "message": "message is required"
                    })
                })
                return

            receiver_channel_name = await get_user_channel_name(
                receiver_id
            )

            if not receiver_channel_name:
                await self.send({
                    "type": "websocket.send",
                    "text": json.dumps({
                        "success": False,
                        "message": "receiver not found or not connected"
                    })
                })
                return

            await self.channel_layer.send(
                receiver_channel_name,
                {
                    "type": "chat_message",
                    "message": {
                        "success": True,
                        "message": message
                    },
                }
            )

        except json.JSONDecodeError:
            await self.send({
                "type": "websocket.send",
                "text": json.dumps({
                    "error": "Invalid JSON"
                })
            })

        except Exception as err:
            print(err)

            await self.send({
                "type": "websocket.send",
                "text": json.dumps({
                    "error": "Something went wrong"
                })
            })

    async def chat_message(self, event):
        print("send to receiver:", event)

        await self.send({
            "type": "websocket.send",
            "text": json.dumps({
                "message": event["message"]
            })
        })

    async def websocket_disconnect(self, event):
        await set_channel_name_to_null(self.channel_name)
        raise StopConsumer()
