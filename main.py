import uvicorn
import multiprocessing

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from core.api import Api


if __name__ == "__main__":
    multiprocessing.set_start_method("spawn")
    app = FastAPI()
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    app.mount("/static", StaticFiles(directory="static"), name="static")
    api = Api(app=app)
    
    uvicorn.run(app=app, host="127.0.0.1", port=9871)