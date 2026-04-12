import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .gemini_chat import ask_ai

class GeminiConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send(json.dumps({
            'message': 'Connected to Gemini WebSocket!'
        }))
    
    async def disconnect(self, close_code):
        pass
    
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']       
        
        try:
            response = await sync_to_async(ask_ai)(message)
            
            await self.send(text_data=json.dumps({
                'message': response
            }))
        
        except Exception as e:
            await self.send(text_data=json.dumps({
                'message': f"Error: {str(e)}"
            }))