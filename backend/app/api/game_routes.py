from fastapi import APIRouter
from app.models.character import CharacterType

router = APIRouter(tags=["game"])

@router.get("/characters")
async def get_available_characters():
    # Get list of available character types
    return {
        "characters": [
            {
                "type": CharacterType.WARRIOR,
                "name": "Warrior",
                "description": "High damage, low defense. Special: Shield Block",
                "attack_range": [10, 15],
                "defense_range": [5, 10]
            },
            {
                "type": CharacterType.TANKER,
                "name": "Tanker",
                "description": "Low damage, high defense. Special: Fireball",
                "attack_range": [5, 10],
                "defense_range": [10, 15]
            },
            {
                "type": CharacterType.MAGE,
                "name": "Mage",
                "description": "Balanced stats. Special: Heal",
                "attack_range": [8, 13],
                "defense_range": [8, 13]
            }
        ]
    }

@router.get("/sessions")
async def get_active_sessions():
    #Get list of active game sessions (for debugging/admin)
    from app.websocket.connection_manager import manager

    sessions_data = []
    for session_id, session in manager.game_sessions.items():
        sessions_data.append({
            "session_id": session_id,
            "player_name": session.player.name,
            "state": session.state,
            "turn": session.current_turn,
            "has_ai_opponent": session.ai_opponent is not None
        })

    return {"sessions": sessions_data}

@router.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Game API is running"}