export enum CharacterType {
  WARRIOR = "warrior",
  TANKER = "tanker",
  MAGE = "mage"
}

export enum ActionType {
  ATTACK = "attack",
  DEFEND = "defend",
  SKILL = "skill"
}

export enum GameState {
  CHARACTER_SELECT = "character_select",
  PLAYER_TURN = "player_turn",
  AI_TURN = "ai_turn",
  FINISHED = "finished"
}

export interface Character {
  name: string;
  character_type: CharacterType;
  max_hp: number;
  current_hp: number;
  attack_range: [number, number];
  defense_range: [number, number];
  skill_name: string;
  turns_since_last_skill: number;
  skill_cooldown: number;
}

export interface Player {
  id: string;
  name: string;
  character?: Character;
}

export interface AIOpponent {
  character: Character;
  difficulty: string;
}

export interface GameSession {
  session_id: string;
  player: Player;
  ai_opponent?: AIOpponent;
  state: GameState;
  current_turn: number;
  is_player_turn: boolean;
  turn_history: string[];
  winner?: string;
}

export interface GameMessage {
  type: string;
  [key: string]: any;
}