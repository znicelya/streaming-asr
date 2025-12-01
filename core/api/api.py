from fastapi import FastAPI

from core.api import Endpoints


class Api:
    def __init__(self, app: FastAPI):
        self.app = app
        self.endpoints = Endpoints()
        self.add_api_routers()
        self.add_ws_routers()
        
    def add_api_routers(self):
        self.app.add_api_route('/', self.endpoints.root, methods=['GET'], summary="index主页")
        
    def add_ws_routers(self):
        self.app.add_api_websocket_route('/asr', self.endpoints.asr, name='asr')
        