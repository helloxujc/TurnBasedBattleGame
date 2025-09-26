from pydantic import BaseModel
from typing import Optional, List
from enum import Enum
from .character import Character, CharacterType

class ActionType(str, Enum):
    ATTACK = "attack"
    DEFEND = "defend"
    SKILL = "skill"

class GameState(str, Enum):
    CHARACTER_SELECT = "character_select"
    PLAYER_TURN = "player_turn"
    AI_TURN = "ai_turn"
    FINISHED = "finished"

class Player(BaseModel):
    id: str
    name: str
    character: Optional[Character] = None

class AIOpponent(BaseModel):
    character: Character
    difficulty: str = "normal"

class GameSession(BaseModel):
    session_id: str
    player: Player
    ai_opponent: Optional[AIOpponent] = None
    state: GameState = GameState.CHARACTER_SELECT
    current_turn: int = 1
    is_player_turn: bool = True
    turn_history: List[str] = []
    winner: Optional[str] = None

    def is_ready(self) -> bool:
        return (self.player.character is not None and
                self.ai_opponent is not None)

class GameAction(BaseModel):
    action_type: ActionType
    damage_dealt: int = 0
    damage_taken: int = 0
    defense_value: int = 0

class SelectCharacterRequest(BaseModel):
    character_type: CharacterType

class GameActionRequest(BaseModel):
    action_type: ActionType

class StartGameRequest(BaseModel):
    player_name: str