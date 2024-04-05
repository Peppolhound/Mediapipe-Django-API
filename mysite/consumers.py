# from channels.generic.websocket import AsyncWebsocketConsumer
# import cv2
# import base64
# import asyncio
# from .camera import VideoCamera

# class VideoStreamConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()
        
#         # Crea un'istanza di VideoCamera
#         self.camera = VideoCamera()
        
#         # Inizia a trasmettere i frame video al client
#         while True:
#             frame = self.camera.get_frame()
#             # Codifica il frame in base64 per trasmetterlo come stringa
#             encoded_frame = base64.b64encode(frame).decode('utf-8')
#             await self.send(text_data=encoded_frame)
#             # await asyncio.sleep(0.1)  # Regola questo valore in base alla frequenza dei frame desiderata

#     async def disconnect(self, close_code):
#         print('Disconneted')

# consumers.py
import base64
import cv2
from channels.generic.websocket import AsyncWebsocketConsumer
from .camera import VideoCamera


class VideoStreamConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.camera = VideoCamera()
        # Assumendo che hai una funzione che ti dà i frame della webcam...
        while True:
            frame = self.camera.get_frame() # Ottieni il frame come array NumPy
            _, buffer = cv2.imencode('.jpg', frame)
            frame_base64 = base64.b64encode(buffer).decode('utf-8')
            await self.send(text_data=frame_base64)
            