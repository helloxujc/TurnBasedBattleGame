import React from 'react';
import { CharacterType } from '../types/game';

interface CharacterSelectProps {
  onSelectCharacter: (characterType: CharacterType) => void;
  disabled?: boolean;
}

const characterData = {
  [CharacterType.WARRIOR]: {
    name: "Warrior",
    description: "High damage, low defense",
    skill: "Shield Block - Enhanced defense",
    stats: "Attack: 10-15, Defense: 5-10",
    image: "/images/characters/warrior.png"
  },
  [CharacterType.TANKER]: {
    name: "Tanker",
    description: "Low damage, high defense",
    skill: "Fireball - Enhanced attack",
    stats: "Attack: 5-10, Defense: 10-15",
    image: "/images/characters/tanker.png"
  },
  [CharacterType.MAGE]: {
    name: "Mage",
    description: "Balanced stats with healing",
    skill: "Heal - Restore HP and attack",
    stats: "Attack: 8-13, Defense: 8-13",
    image: "/images/characters/mage.png"
  }
};

export const CharacterSelect: React.FC<CharacterSelectProps> = ({ onSelectCharacter, disabled }) => {
  return (
    <div className="character-select">
      <h2>Choose Your Character</h2>
      <div className="character-grid">
        {Object.entries(characterData).map(([type, data]) => (
          <div key={type} className="character-card">
            <div className="character-image-container">
              <img
                src={data.image}
                alt={data.name}
                className="character-image"
                onError={(e) => {
                  e.currentTarget.style.display = 'none';
                }}
              />
            </div>
            <h3>{data.name}</h3>
            <p className="character-description">{data.description}</p>
            <p className="character-stats">{data.stats}</p>
            <p className="character-skill"><strong>Special:</strong> {data.skill}</p>
            <button
              onClick={() => onSelectCharacter(type as CharacterType)}
              disabled={disabled}
              className="select-character-button"
            >
              Select {data.name}
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};