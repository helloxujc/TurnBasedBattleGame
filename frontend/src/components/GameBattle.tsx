import React from 'react';
import { GameSession, ActionType } from '../types/game';

interface GameBattleProps {
  session: GameSession;
  onAction: (action: ActionType) => void;
  messages: any[];
}

// Helper function to get character image
const getCharacterImage = (characterType: string) => {
  switch (characterType) {
    case 'warrior':
      return '/images/characters/warrior.png';
    case 'tanker':
      return '/images/characters/tanker.png';
    case 'mage':
      return '/images/characters/mage.png';
    default:
      return '/images/characters/warrior.png';
  }
};

export const GameBattle: React.FC<GameBattleProps> = ({
  session,
  onAction,
  messages
}) => {
  const canUseSkill = () => {
    return session.player.character &&
           session.player.character.turns_since_last_skill >= session.player.character.skill_cooldown;
  };

  const getLastTurnResult = () => {
    const lastMessage = messages.slice().reverse().find(m => m.type === 'turn_result');
    return lastMessage?.result?.summary || '';
  };

  if (session.state === 'finished') {
    const isWinner = session.winner === session.player.id;
    return (
      <div className="game-battle finished">
        <h1>{isWinner ? 'Victory!' : 'Defeat!'}</h1>
        <div className="final-stats">
          <div className="player-final">
            <h3>You ({session.player.character?.name})</h3>
            <p>HP: {session.player.character?.current_hp}/{session.player.character?.max_hp}</p>
          </div>
          <div className="opponent-final">
            <h3>AI ({session.ai_opponent?.character.name})</h3>
            <p>HP: {session.ai_opponent?.character.current_hp}/{session.ai_opponent?.character.max_hp}</p>
          </div>
        </div>
        <button onClick={() => window.location.reload()}>
          Play Again
        </button>
      </div>
    );
  }

  const isPlayerTurn = session.state === 'player_turn';

  return (
    <div className="game-battle">
      <h1>Turn {session.current_turn}</h1>

      {/* Battle Info */}
      <div className="room-info">
        <span>Battle vs AI</span>
        <span>{isPlayerTurn ? "Your Turn" : "AI Turn"}</span>
      </div>

      {/* Player Stats */}
      <div className="battle-area">
        <div className="player-stats">
          <div className="character-battle-info">
            <div className="battle-character-image-container">
              <img
                src={getCharacterImage(session.player.character?.character_type || '')}
                alt={session.player.character?.name}
                className="battle-character-image"
              />
            </div>
            <div className="character-info">
              <h3>You - {session.player.character?.name}</h3>
              <div className="hp-bar">
                <div className="hp-fill" style={{
                  width: `${((session.player.character?.current_hp || 0) / (session.player.character?.max_hp || 1)) * 100}%`
                }}></div>
                <span>{session.player.character?.current_hp}/{session.player.character?.max_hp} HP</span>
              </div>
              <p>Skill: {session.player.character?.skill_name}
                {canUseSkill() ? ' (Ready)' : ` (${(session.player.character?.skill_cooldown || 0) - (session.player.character?.turns_since_last_skill || 0)} turns)`}
              </p>
            </div>
          </div>
        </div>

        <div className="vs-divider">VS</div>

        <div className="opponent-stats">
          <div className="character-battle-info">
            <div className="battle-character-image-container">
              <img
                src={getCharacterImage(session.ai_opponent?.character.character_type || '')}
                alt={session.ai_opponent?.character.name}
                className="battle-character-image ai-character"
              />
            </div>
            <div className="character-info">
              <h3>AI - {session.ai_opponent?.character.name}</h3>
              <div className="hp-bar">
                <div className="hp-fill" style={{
                  width: `${((session.ai_opponent?.character.current_hp || 0) / (session.ai_opponent?.character.max_hp || 1)) * 100}%`
                }}></div>
                <span>{session.ai_opponent?.character.current_hp}/{session.ai_opponent?.character.max_hp} HP</span>
              </div>
              <p>Skill: {session.ai_opponent?.character.skill_name}
                {session.ai_opponent?.character && session.ai_opponent.character.turns_since_last_skill >= session.ai_opponent.character.skill_cooldown ? ' (Ready)' :
                 ` (${(session.ai_opponent?.character.skill_cooldown || 0) - (session.ai_opponent?.character.turns_since_last_skill || 0)} turns)`}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Turn Result */}
      {getLastTurnResult() && (
        <div className="turn-result">
          <h4>Last Turn:</h4>
          <p>{getLastTurnResult()}</p>
        </div>
      )}

      {/* Action Buttons */}
      <div className="action-buttons">
        <button
          onClick={() => onAction(ActionType.ATTACK)}
          disabled={!isPlayerTurn}
          className="action-button attack"
        >
          Attack
        </button>
        <button
          onClick={() => onAction(ActionType.DEFEND)}
          disabled={!isPlayerTurn}
          className="action-button defend"
        >
          Defend
        </button>
        <button
          onClick={() => onAction(ActionType.SKILL)}
          disabled={!isPlayerTurn || !canUseSkill()}
          className="action-button skill"
        >
          Use Skill
        </button>
      </div>

      {!isPlayerTurn && session.state === 'ai_turn' && (
        <p className="waiting-message">AI is thinking...</p>
      )}
    </div>
  );
};