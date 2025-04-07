"""
Game Loop:
The entire battle is a loop process until either the player or the enemy's health points drop to 0.
Each round consists of a Player turn and an Enemy turn.
Player Turn:
The system prompts the player to choose an action (attack, defend, or use skill).
Based on the player's choice, the corresponding action is executed:
    Attack: The player inflicts damage to the enemy.
    Defend: The player reduces the damage inflicted by the enemy in this round.
    Use Skill: The player uses a special skill to inflict damage or reduce incoming damage.
Enemy Turn:
The enemy is randomly assigned an action (attack, defend, or use skill).
At the end of each turn, the system checks whether both sides still have health remaining
to decide if the battle should continue.
"""
import random
import pygame
from Final_Project_Battle import config
from Final_Project_Battle.character import Enemy

class GameLogic:
    def __init__(self, game_data, battle_screen):
        self.game_data = game_data # Initialize game_data
        self.battle_screen = battle_screen # Initialize battle_screen
        self.move_log = []  # Initialize move log
        self.round_number = 1  # Set round number to 1
        self.turn = "Player" # Player acts first by default
        self.player_action = None
        self.battle_result = None

    # Function to set player's action
    def set_player_action(self, action):
        self.player_action = action

    def play_turn(self):
        #Every round starts with the Player's turn, activated by the Player's choice of action in the battle_screen page
        player_action, player_damage, player_defense, player_move_info = self.handle_player_turn()  # Handles player's action

        # If the player_action is None, meaning the Player tries to use skill when the skill is still in cooldown.
        # This round is deemed ineffective and the player need to choose another action to restart the round
        if player_action is None:
            move_info = f"Skill is still in cooldown. Please choose another action."
            self.update_move_log(False,move_info) # Update the move log
            self.battle_screen.render(full_render=False)
            print(move_info)
            pygame.display.update()
            return

        # If the player_action is valid, enemy action will be handled
        enemy_action, enemy_damage, enemy_defense, enemy_move_info = self.handle_enemy_turn()  # Handles the enemy's action

        # If the damage output by both the Player and the Enemy are 0 in this round, meaning they only
        # have defense points, no damage is dealt in this round. This means that their health points will
        # not be changed in this round
        if player_damage == 0 and enemy_damage == 0:
            move_info = f"Both sides are defending. No damage dealt this round."
            self.update_move_log(True,move_info)
            print(move_info)
            # Their skill cooldown period will be logged
            self.game_data.player.character.turns_since_last_skill += 1
            self.game_data.enemy.character.turns_since_last_skill += 1
            self.round_number += 1  # Updates round number

        # If there is damage output in this round, changes in their health points will be calculated
        else:
            # The current Player's HP is equal to the Player's HP minus the damage points inflicted by the enemy and plus its
            # defense points. And the Play HP cannot go below 0.
            self.game_data.player.character.current_hp = max(0, self.game_data.player.character.current_hp - enemy_damage + player_defense)
            # The current health points of the Player cannot exceed 100
            self.game_data.player.character.cap_health()
            self.update_move_log(True,player_move_info)
            print(player_move_info)
            # Check if the Player's HP is reduced to zero
            if not self.check_status():
                # If the Player doesn't lose, calculate the Enemy's HP (same logic as calculating the Player HP)
                self.game_data.enemy.character.current_hp = max(0, self.game_data.enemy.character.current_hp - player_damage + enemy_defense)
                # The current health points of the Enemy cannot exceed 100
                self.game_data.enemy.character.cap_health()
                # Their skill cooldown period will be logged
                self.game_data.player.character.turns_since_last_skill += 1
                self.game_data.enemy.character.turns_since_last_skill += 1
                self.update_move_log(True,enemy_move_info)
                print(enemy_move_info)
                # Check if the Enemy's HP is reduced to zero
                if not self.check_status():
                    self.round_number += 1 # Updates round number if the game is not ended
        print(f"Player current hp: {self.game_data.player.character.current_hp}")
        print(f"Enemy current hp: {self.game_data.enemy.character.current_hp}")
        self.battle_screen.render(full_render=False)
        pygame.display.update()

    def update_move_log(self, valid_action, move_info):
        """
        Function to update move log, takes a Boolean parameter: valid_action, and a string parameter: move_info
        If it's not a valid_action, the round number remains unchanged.
        """
        if valid_action:
            move_with_round = f"Round {self.round_number}: {move_info}"
            self.move_log.append(move_with_round)
        else:
            self.move_log.append(move_info)

        # Only leaves the latest 2 logs on the screen
        if len(self.move_log) > 2:
            self.move_log.pop(0)

        self.battle_screen.update_move_log(self.move_log)

    # Function to handle the Player's turn in one round
    def handle_player_turn(self):
        turn = "Player"
        curr_character = self.game_data.player.character
        damage_points = 0
        defense_points = 0
        move_info = ""

        action = self.player_action
        if action == "Attack":
            damage_points = curr_character.attack()
            move_info = f"{turn} attacks and inflicts {damage_points} damage points."

        elif action == "Defend":
            defense_points = curr_character.defend()
            move_info = f"{turn} defends and gains {defense_points} points in defense."

        elif action == "Use Skill":
            # The Player can only use the special skill every 3 rounds
            if curr_character.skill_requirement():
                damage_points, defense_points = curr_character.use_skill()
                # Reset the skill to cooldown period after it's used
                curr_character.turns_since_last_skill = 0
                move_info = f"{turn} uses skill and inflicts {damage_points} damage points, gains {defense_points} points in defense."
            # The action = None when user tries to use the special skill while it's still in cooldown
            else:
                action = None
        # Return the Player's action type, damage output, defense output and move log
        return action, damage_points, defense_points, move_info

    # Function to handle the Player's turn in one round
    def handle_enemy_turn(self):
        turn = "Enemy"
        curr_character = self.game_data.enemy.character
        damage_points = 0
        defense_points = 0
        move_info = ""

        # The enemy is randomly assigned an action
        action_options1 = ["Attack", "Defend", "Use Skill"]
        action_options2 = ["Attack", "Defend"]
        action_weights1 = [1.5, 7, 1.5]
        action_weights2 = [3, 7]
        # If the skill is not in cool down, the enemy will be randomly assigned one of the 3 actions
        if curr_character.skill_requirement():
            # If the enemy HP is below 50% of its maximum HP, it is more likely to be assigned the defense action
            if self.game_data.enemy.character.current_hp >= config.DEFAULT_HP / 2:
                action = random.choice(action_options1)
            else:
                action = random.choices(action_options1, weights=action_weights1, k=1)[0]
        # If the skill is in cool down, the enemy will be randomly assigned one of the 2 actions
        else:
            if self.game_data.enemy.character.current_hp >= config.DEFAULT_HP / 2:
                action = random.choice(action_options2)
            else:
                action = random.choices(action_options2, weights=action_weights2, k=1)[0]

        if action == "Attack":
            damage_points = curr_character.attack()
            move_info = f"{turn} attacks and inflicts {damage_points} damage points."

        elif action == "Defend":
            defense_points = curr_character.defend()
            move_info = f"{turn} defends and gains {defense_points} points in defense."

        elif action == "Use Skill":
            damage_points, defense_points = curr_character.use_skill()
            # Reset the skill to cooldown period after it's used
            curr_character.turns_since_last_skill = 0
            move_info = f"{turn} uses skill and inflicts {damage_points} damage points, gains {defense_points} points in defense."

        # Return the Enemy's action type, damage output, defense output and move log
        return action, damage_points, defense_points, move_info

    # Function to check if either the Player or the Enemy's HP has reached 0
    def check_status(self):
        if self.game_data.player.character.current_hp <= 0:
            self.battle_result = "Enemy"
            return True  # Battle ends
        elif self.game_data.enemy.character.current_hp <= 0:
            self.battle_result = "Player"
            return True  # Battle ends
        return False  # Battle continues

    def reset_game(self):
        """Reset the game logic state"""
        self.game_data.player.reset()  # Reset player's stats
        self.game_data.enemy.reset()  # Reset enemy's stats

        # Enemy's new character.
        new_enemy = Enemy()
        print(new_enemy)

        self.turn = "Player"  # Reset the turn to the player
        self.battle_result = None  # Clear the battle results
        self.player_action = None  # Clear any stored player actions
        self.round_number = 1 # Reset the round number
        print("Game has been reset. Player starts.")
