import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .gemini_chat import ask_ai

class GeminiConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        
        self.chat_session = ask_ai()
    
    
    async def receive(self, text_data):
        data = json.loads(text_data)
        user_message = data['message']       
        
        try:
            if not self.chat_session:
                self.chat_session = ask_ai()
            
            if user_message:
                response = await sync_to_async(self.chat_session.send_message)(user_message)
            
                await self.send(text_data=json.dumps({
                    'message': response.text
                }))
        
        except Exception as e:
            await self.send(text_data=json.dumps({
                'message': f"Error: {str(e)}"
            }))