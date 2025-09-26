import React, { useState } from 'react';

interface MainMenuProps {
  onStartGame: (playerName: string) => void;
  connected: boolean;
}

export const MainMenu: React.FC<MainMenuProps> = ({ onStartGame, connected }) => {
  const [playerName, setPlayerName] = useState('');

  const handleStartGame = (e: React.FormEvent) => {
    e.preventDefault();
    if (playerName.trim()) {
      onStartGame(playerName.trim());
    }
  };

  if (!connected) {
    return (
      <div className="main-menu">
        <h1>Turn-Based Battle Game</h1>
        <p>Connecting to server...</p>
      </div>
    );
  }

  return (
    <div className="main-menu">
      <h1>Turn-Based Battle Game</h1>
      <p className="subtitle">Battle against AI opponents!</p>

      <form onSubmit={handleStartGame} className="start-form">
        <h2>Enter the Arena</h2>
        <input
          type="text"
          placeholder="Enter your name"
          value={playerName}
          onChange={(e) => setPlayerName(e.target.value)}
          maxLength={20}
          required
        />
        <button type="submit" disabled={!playerName.trim()} className="start-button">
          Start Battle
        </button>
      </form>

      <div className="game-info">
        <h3>How to Play</h3>
        <ul>
          <li>Choose your character class</li>
          <li>Battle against AI opponent</li>
          <li>Use Attack, Defend, or Special Skills</li>
          <li>Defeat your opponent to win!</li>
        </ul>
      </div>
    </div>
  );
};