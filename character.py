
from Final_Project_Battle import config
import random

class Character:
    def __init__(self, name, max_hp, attack_range, defense_range, skill):
        """
        :param name: name of the character
        :param max_hp: maximum health points
        :param attack_range: attack range
        :param defense_range: defense range
        :param skill: special skill
        set the turns_since_last_skill to 0 for calculating when skill can be used
        set the skill cooldown to 3, meaning that either side could only use the skill once every three turns
        """
        self.name = name
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.attack_range = attack_range
        self.defense_range = defense_range
        self.skill = skill
        self.turns_since_last_skill = 0
        self.skill_cooldown = 3

    def attack(self):
        """
        Attack value is a random integer generated within the character's attack range.
        Damage output equals to the attack value plus a random modifier (-5 to 5),
        but it will guarantee 1 damage output at minimum.
        :return: the amount of damage the character exerts on the opposite character
        """
        attack_value = random.randint(*self.attack_range)
        damage = max(attack_value + config.RANDOM_MODIFIER, 1)
        return damage

    def defend(self):
        """
        Defense value is a random integer generated within the character's defense range.
        Defense output equals to the defense value plus a random modifier (-5 to 5),
        but it will guarantee 1 defense output at minimum.
        :return: how much the character reduces the opposite character's incoming attacks
        """
        defense_value = random.randint(*self.defense_range)
        defense = max(defense_value + config.RANDOM_MODIFIER, 1)
        return defense

    def cap_health(self):
        # Function to ensure the health points do not go beyond 100 during the game
        if self.current_hp > self.max_hp:
            self.current_hp = self.max_hp

    def skill_requirement(self):
        # Function to manage skill cooldown period
        if self.turns_since_last_skill >= self.skill_cooldown:
            return True
        else:
            return False

    def use_skill(self):
        if not self.skill_requirement():
            print(f"Skill is in cooldown.")
        self.turns_since_last_skill = 0 # reset cooldown
        return 0,0

    def reset(self):
        # Function to reset the character's health points
        self.current_hp = config.DEFAULT_HP

# Subclass of the Character
class Warrior(Character):
    """
    Warrior: Damage Output: High (Attack range: 10-15)
             Damage Resistance: Low (Defense range: 5-10)
             Special Skill: Shield Block – Reduces all incoming damage by 75% for a turn
    """
    def __init__(self):
        super().__init__(name="Warrior", max_hp=config.DEFAULT_HP, attack_range=config.WA_ATK_RANGE,
                         defense_range=config.WA_DEF_RANGE, skill = "Shield Block")

    def use_skill(self):
        """
        Skill that boosts defense output with a skill modifier (*1.75)
        :return: damage output = 0, defense output
        """
        defense_value = random.randint(*self.defense_range)
        defense = max(defense_value * config.WA_SK_MODIFIER + config.RANDOM_MODIFIER, 1)  # At least 1 point of defense
        return 0, defense

# Subclass of the Character
class Tanker(Character):
    """
    Tanker: Damage Output: Low (Attack range: 5-10)
            Damage Resistance: High (Defense range: 10-15)
            Special Skill: Fireball - Increase attack damage by 75% for a turn
    """
    def __init__(self):
        super().__init__(name="Tanker", max_hp=config.DEFAULT_HP, attack_range=config.TK_ATK_RANGE,
                         defense_range= config.TK_DEF_RANGE, skill="Fireball")

    def use_skill(self):
        """
        Skill that boosts damage output with a skill modifier (*1.75)
        :return: damage output, defense output = 0
        """
        attack_value = random.randint(*self.attack_range)
        damage = max(attack_value * config.TK_SK_MODIFIER + config.RANDOM_MODIFIER, 1)
        return damage, 0

# Subclass of the Character
class Magician(Character):
    """
    Magician: Damage Output: Moderate (Attack range: 8-13)
              Damage Resistance: Moderate (Defense range: 8-13)
              Special Skill: Magic Powder - Reduces all incoming damage by 25% and increases attack damages by 25% a turn
    """
    def __init__(self):
        super().__init__(name="Magician", max_hp=config.DEFAULT_HP, attack_range=config.MAG_ATK_RANGE,
                         defense_range=config.MAG_DEF_RANGE, skill="Magic Powder")

    def use_skill(self):
        """
        Skill that boosts damage output and defense output with a skill modifier (*1.25)
        :return: damage output, defense output
        """
        attack_value = random.randint(*self.attack_range)
        damage = max(attack_value * config.MAG_SK_MODIFIER + config.RANDOM_MODIFIER, 1)
        defense_value = random.randint(*self.defense_range)
        defense = max(defense_value * config.MAG_SK_MODIFIER + config.RANDOM_MODIFIER, 1)
        return damage, defense

class Player:
    def __init__(self):
        self.character = None
        self.name = "Player"

    # Function for the player to choose the character they want to play
    def set_character(self, character_type):
        if character_type == "Warrior":
            self.character = Warrior()
        elif character_type == "Tanker":
            self.character = Tanker()
        elif character_type == "Magician":
            self.character = Magician()

    # Function to reset the character
    def reset(self):
        if self.character:
            self.character.reset()
            print(f"{self.name} has been reset.")

    # Function to get the maximum health points
    @property
    def max_hp(self):
        if self.character:
            return self.character.max_hp
        else:
            return  0

    # Function to get the current health points
    @property
    def current_hp(self):
        if self.character:
            return self.character.current_hp
        else:
            return 0

class Enemy:
    def __init__(self):
        # The AI enemy will be randomly assigned a character from the 3 choices
        self.character = random.choice([Warrior(),Tanker(),Magician()])
        self.name = "Enemy"
        print(f'The Enemy chooses {self.character.name} as their character.')

    # Function to reset the character
    def reset(self):
        if self.character:
            self.character.reset()
            print(f"{self.name} has been reset.")

    # Function to get the maximum health points
    @property
    def max_hp(self):
        if self.character:
            return self.character.max_hp
        else:
            return 0

    # Function to get the current health points
    @property
    def current_hp(self):
        if self.character:
            return self.character.current_hp
        else:
            return 0

    def __str__(self):
        return "The enemy awaits for the rematch in the Battleground..."

