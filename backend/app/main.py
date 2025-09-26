from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import game_routes
from app.websocket import connection_manager

app = FastAPI(title="Turn-Based Battle Game API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(game_routes.router, prefix="/api")

app.include_router(connection_manager.router)

@app.get("/")
async def root():
    return {"message": "Turn-Based Battle Game API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}