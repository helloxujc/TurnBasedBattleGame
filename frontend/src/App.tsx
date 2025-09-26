import React from 'react';
import './App.css';
import { useWebSocket } from './hooks/useWebSocket';
import { MainMenu } from './components/MainMenu';
import { CharacterSelect } from './components/CharacterSelect';
import { GameBattle } from './components/GameBattle';
import { CharacterType, ActionType, GameState } from './types/game';

const WEBSOCKET_URL = 'ws://localhost:8000/ws';

function App() {
  const {
    connected,
    session,
    sessionId,
    messages,
    sendMessage
  } = useWebSocket(WEBSOCKET_URL);

  const handleStartGame = (playerName: string) => {
    sendMessage({
      type: 'start_game',
      player_name: playerName
    });
  };

  const handleSelectCharacter = (characterType: CharacterType) => {
    sendMessage({
      type: 'select_character',
      character_type: characterType
    });
  };

  const handleGameAction = (action: ActionType) => {
    sendMessage({
      type: 'game_action',
      action_type: action
    });
  };

  // Determine which component to render based on game state
  const renderCurrentView = () => {
    if (!session) {
      return (
        <MainMenu
          onStartGame={handleStartGame}
          connected={connected}
        />
      );
    }

    switch (session.state) {
      case GameState.CHARACTER_SELECT:
        return (
          <div className="character-selection-screen">
            <h2>Welcome, {session.player.name}!</h2>
            <CharacterSelect
              onSelectCharacter={handleSelectCharacter}
              disabled={false}
            />
          </div>
        );

      case GameState.PLAYER_TURN:
      case GameState.AI_TURN:
      case GameState.FINISHED:
        return (
          <GameBattle
            session={session}
            onAction={handleGameAction}
            messages={messages}
          />
        );

      default:
        return <div>Loading game...</div>;
    }
  };

  return (
    <div className="App">
      <div className="game-container">
        {renderCurrentView()}
      </div>

      {/* Debug info in development */}
      {process.env.NODE_ENV === 'development' && (
        <div className="debug-info">
          <p>Connected: {connected ? 'Yes' : 'No'}</p>
          <p>Session ID: {sessionId}</p>
          <p>Game State: {session?.state}</p>
          <p>Messages: {messages.length}</p>
        </div>
      )}
    </div>
  );
}

export default App;
