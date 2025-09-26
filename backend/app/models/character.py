from pydantic import BaseModel
from typing import Tuple
from enum import Enum
import random

class CharacterType(str, Enum):
    WARRIOR = "warrior"
    TANKER = "tanker"
    MAGE = "mage"

class Character(BaseModel):
    name: str
    character_type: CharacterType
    max_hp: int = 100
    current_hp: int = 100
    attack_range: Tuple[int, int]
    defense_range: Tuple[int, int]
    skill_name: str
    turns_since_last_skill: int = 0
    skill_cooldown: int = 3

    def attack(self) -> int:
        attack_value = random.randint(*self.attack_range)
        damage = max(attack_value + random.randint(-5, 5), 1)
        return damage

    def defend(self) -> int:
        defense_value = random.randint(*self.defense_range)
        defense = max(defense_value + random.randint(-5, 5), 1)
        return defense

    def can_use_skill(self) -> bool:
        return self.turns_since_last_skill >= self.skill_cooldown

    def use_skill(self) -> Tuple[int, int]:  # Returns (damage, defense)
        if not self.can_use_skill():
            return 0, 0

        self.turns_since_last_skill = 0

        if self.character_type == CharacterType.WARRIOR:
            # Shield Block - enhanced defense
            defense_value = random.randint(*self.defense_range)
            defense = max(int(defense_value * 1.75) + random.randint(-5, 5), 1)
            return 0, defense
        elif self.character_type == CharacterType.TANKER:
            # Fireball - enhanced attack
            attack_value = random.randint(*self.attack_range)
            damage = max(int(attack_value * 1.75) + random.randint(-5, 5), 1)
            return damage, 0
        elif self.character_type == CharacterType.MAGE:
            # Heal - restore HP and moderate damage
            heal_amount = max(int(25 * 1.25), 1)
            self.current_hp = min(self.current_hp + heal_amount, self.max_hp)
            attack_value = random.randint(*self.attack_range)
            damage = max(int(attack_value * 1.25) + random.randint(-5, 5), 1)
            return damage, 0

        return 0, 0

    def take_damage(self, damage: int):
        self.current_hp = max(0, self.current_hp - damage)

    def is_alive(self) -> bool:
        return self.current_hp > 0

    def reset(self):
        self.current_hp = self.max_hp
        self.turns_since_last_skill = 0

    @classmethod
    def create_character(cls, character_type: CharacterType) -> "Character":
        character_configs = {
            CharacterType.WARRIOR: {
                "name": "Warrior",
                "attack_range": (10, 15),
                "defense_range": (5, 10),
                "skill_name": "Shield Block"
            },
            CharacterType.TANKER: {
                "name": "Tanker",
                "attack_range": (5, 10),
                "defense_range": (10, 15),
                "skill_name": "Fireball"
            },
            CharacterType.MAGE: {
                "name": "Mage",
                "attack_range": (8, 13),
                "defense_range": (8, 13),
                "skill_name": "Heal"
            }
        }

        config = character_configs[character_type]
        return cls(
            character_type=character_type,
            **config
        )