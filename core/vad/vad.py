import json
from fastapi import WebSocket
import webrtcvad

from typing import Callable


class VADProcessor(object):

    def __init__(
        self,
        mode: int,
        sample_rate: int = 16000,
        frame_duration: int = 30,
        padding_duration: float = 1500,
        callback: Callable = None,
    ):
        self.vad = webrtcvad.Vad(mode)
        self.sample_rate = sample_rate
        self.frame_duration_ms = frame_duration
        self.padding_duration_ms = padding_duration
        self.frame_size_bytes = int(
            self.sample_rate * 2 * (self.frame_duration_ms / 1000)
        )
        self.max_silence_frames = int(self.padding_duration_ms / self.frame_duration_ms)
        self.buffer = b""
        self.audio_frames = []
        self.silence_counter = 0
        self.is_speaking = False
        self.callback = callback

    async def _reset(self):
        self.is_speaking = False
        self.silence_counter = 0
        self.audio_frames = []

    async def process_chunk(self, chunk: bytes, websocket: WebSocket):
        self.websocket = websocket
        self.buffer += chunk

        while len(self.buffer) >= self.frame_size_bytes:
            frame = self.buffer[: self.frame_size_bytes]
            self.buffer = self.buffer[self.frame_size_bytes :]
            await self._analyze_frame(frame)

    async def _analyze_frame(self, frame):
        is_speech = self.vad.is_speech(frame, self.sample_rate)
        if is_speech:
            if not self.is_speaking:
                self.is_speaking = True
            self.silence_counter = 0
            self.audio_frames.append(frame)
        else:
            if self.is_speaking:
                self.silence_counter += 1
                self.audio_frames.append(frame)

                if self.silence_counter >= self.max_silence_frames:
                    audio_bytes = b"".join(self.audio_frames)
                    transcription = await self.callback(audio_bytes)
                    await self.websocket.send_text(json.dumps({
                        'type': 'transcription',
                        'text': transcription
                    }))
                    await self._reset()
