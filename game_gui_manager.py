import sys
import pygame
from Final_Project_Battle.battle_screen import BattleScreen
from Final_Project_Battle.character import Enemy
from Final_Project_Battle.game_logic import GameLogic
from Final_Project_Battle.choose_char_screen import ChooseCharScreen
from Final_Project_Battle.main_screen import MainScreen
from Final_Project_Battle.result_screen import ResultScreen
from Final_Project_Battle import config


class GameGUIManager:
    def __init__(self, screen, game_data):
        self.screen = screen
        self.in_main_menu = True
        self.in_choose_char = False
        self.in_battle = False
        self.in_result = False

        self.require_full_render = True

        self.main_screen = MainScreen(screen)
        self.choose_char_screen = ChooseCharScreen(screen)
        self.battle_screen = BattleScreen(screen, game_data)
        self.result_screen = ResultScreen(screen, config.SCREEN_WIDTH, config.SCREEN_HEIGHT)

        self.game_data = game_data
        self.game_logic = GameLogic(game_data, self.battle_screen)

    def render(self):
        """Render the interface based on the current state"""
        if self.in_main_menu:
            self.main_screen.render()
        elif self.in_choose_char:
            self.choose_char_screen.render()
        elif self.in_battle:
            if self.require_full_render:
                self.battle_screen.render(True)
                self.require_full_render = False  # reset the Flag
            else:
                self.battle_screen.render(False)
        elif self.in_result:
            self.result_screen.render(self.game_logic.battle_result)

    def handle_event(self, event):
        """Handle events based on the current screen"""
        if self.in_main_menu:
            option = self.main_screen.handle_event(event)
            if option == "start_game":  # Start Game
                self.in_main_menu = False
                self.in_choose_char = True
            elif option == "exit":  # Exit
                pygame.quit()
                sys.exit()

        elif self.in_choose_char:
            # Player selects the character they want to play
            action = self.choose_char_screen.handle_event(event)
            if action in ["Warrior", "Tanker", "Magician"]:
                self.game_data.player.set_character(action)
                print(f"The Player chooses {action} as their character.")
                self.in_choose_char = False
                self.in_battle = True

        elif self.in_battle:
            action = self.battle_screen.handle_event(event)
            if action in ["Attack", "Defend", "Use Skill"]:
                self.game_logic.set_player_action(action) # Set the action chosen by the player
                self.game_logic.play_turn() # Starts a game round

            if self.game_logic.check_status():
                self.in_battle = False
                self.in_result = True  # Ensure the results page is activated

        elif self.in_result:
            action = self.result_screen.handle_event(event)
            if action == "Restart":  # Restart the game
                self.game_logic.reset_game()
                self.in_main_menu = True
                self.in_result = False
                self.require_full_render = True

            elif action == "Exit":  # Exit the game
                pygame.quit()
                sys.exit()




