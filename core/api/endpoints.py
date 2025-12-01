import json
import traceback

from fastapi import WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from starlette.types import Message

from core.vad import VADProcessor
from core.asr.asr import ASR

class Endpoints(object):
    
    def __init__(self):
        self.asr_model = ASR()
        self.vad = VADProcessor(
            mode=3,
            sample_rate=16000,
            frame_duration=30,
            padding_duration=1500,
            callback=self.asr_model.on_audio_frame
        )
    
    async def root(self):
        return FileResponse('static/index.html')
    
    async def asr(self, websocket: WebSocket):
        await websocket.accept()
        try:
            while True:
                message = await websocket.receive()
                if 'text' in message:
                    await self._handle_text_message(message)
                if 'bytes' in message:
                    await self._handle_binary_message(message, websocket)
        
        except WebSocketDisconnect:
            print('WebSocketDisconnect')
        except Exception as e:
            traceback.print_exc()
    
    async def _handle_text_message(self, message: Message):
        msg = json.loads(message['text'])
        print(msg)
    
    async def _handle_binary_message(self, message: Message, websocket: WebSocket):
        await self.vad.process_chunk(message['bytes'], websocket)
        