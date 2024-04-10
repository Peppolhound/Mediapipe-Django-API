import cv2
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.template.loader import render_to_string
import asyncio



# class Home(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()
#         html_content = await self.get_home_page_content()
#         await self.send(html_content)

#     @database_sync_to_async
#     def get_home_page_content(self):
#         return render_to_string('home.html')


class VideoStreamConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        # Avvia un loop che invia i frame della videocamera al client
        asyncio.get_event_loop().create_task(self.stream_video())

    async def disconnect(self, close_code):
        # Gestione per la fine della cattura da
        pass

    async def connect(self):
        await self.accept()
        self.connected = True
        asyncio.get_event_loop().create_task(self.stream_video())

    async def disconnect(self, close_code):
        self.connected = False

    async def stream_video(self):
        # Inizializza la cattura video
        cap = cv2.VideoCapture(0)
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    print("Impossibile leggere il frame")
                # Converte il frame in JPEG
                ret, jpeg = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 70]) #riduce la qualità del frame per migliorare la trasmissione dei dati
                # Invia i dati convertiti in byte
                await self.send(bytes_data=jpeg.tobytes())
                # Check connessione websocket
                # if self.connected: 
                #     print('connected')
                # Aspetta prima di inviare il prossimo frame (regolare in base al frame rate)
                await asyncio.sleep(0.1) 
        except Exception as e: 
            print(f"Errore durante la trasmissione del video: {e}")
        # Rilascia la cattura alla fine del loop
        cap.release()