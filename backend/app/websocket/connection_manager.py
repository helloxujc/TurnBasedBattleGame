from fastapi import WebSocket, WebSocketDisconnect, APIRouter
from typing import Dict
import json
import uuid
from app.models.game import GameSession, Player, GameState, AIOpponent
from app.services.game_service import GameService

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.game_sessions: Dict[str, GameSession] = {}
        self.game_service = GameService()

    async def connect(self, websocket: WebSocket) -> str:
        await websocket.accept()
        session_id = str(uuid.uuid4())
        self.active_connections[session_id] = websocket
        return session_id

    def disconnect(self, session_id: str):
        if session_id in self.active_connections:
            del self.active_connections[session_id]
        if session_id in self.game_sessions:
            del self.game_sessions[session_id]

    async def send_message(self, session_id: str, message: dict):
        if session_id in self.active_connections:
            try:
                await self.active_connections[session_id].send_text(json.dumps(message))
            except:
                self.disconnect(session_id)

    def start_game(self, session_id: str, player_name: str) -> GameSession:
        player = Player(id=session_id, name=player_name)
        session = GameSession(session_id=session_id, player=player)
        self.game_sessions[session_id] = session
        return session

    async def handle_message(self, session_id: str, message: dict):
        message_type = message.get("type")

        if message_type == "start_game":
            player_name = message.get("player_name", "Player")
            session = self.start_game(session_id, player_name)
            await self.send_message(session_id, {
                "type": "game_started",
                "session": session.dict(),
                "message": "Choose your character to begin!"
            })

        elif message_type == "select_character":
            await self.handle_character_selection(session_id, message)

        elif message_type == "game_action":
            await self.handle_game_action(session_id, message)

    async def handle_character_selection(self, session_id: str, message: dict):
        session = self.game_sessions.get(session_id)
        if not session:
            return

        character_type = message.get("character_type")

        # Create player character
        player_character = self.game_service.create_character(character_type)
        session.player.character = player_character

        # Create AI opponent with random character
        ai_character_type = self.game_service.get_random_character_type()
        ai_character = self.game_service.create_character(ai_character_type)
        session.ai_opponent = AIOpponent(character=ai_character)

        # Battle begins
        session.state = GameState.PLAYER_TURN
        session.is_player_turn = True

        await self.send_message(session_id, {
            "type": "battle_started",
            "session": session.dict(),
            "message": f"Battle begins! You chose {player_character.name}, AI chose {ai_character.name}"
        })

    async def handle_game_action(self, session_id: str, message: dict):
        session = self.game_sessions.get(session_id)
        if not session or not session.is_ready():
            return

        if session.state != GameState.PLAYER_TURN:
            await self.send_message(session_id, {
                "type": "error",
                "message": "Not your turn"
            })
            return

        action_type = message.get("action_type")

        # Process player turn
        result = await self.game_service.process_player_vs_ai_turn(session, action_type)

        await self.send_message(session_id, {
            "type": "turn_result",
            "result": result,
            "session": session.dict()
        })

        # Check for game over
        if session.state == GameState.FINISHED:
            await self.send_message(session_id, {
                "type": "game_over",
                "winner": session.winner,
                "session": session.dict()
            })

# Global connection manager instance
manager = ConnectionManager()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    session_id = await manager.connect(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            await manager.handle_message(session_id, message)

    except WebSocketDisconnect:
        manager.disconnect(session_id)