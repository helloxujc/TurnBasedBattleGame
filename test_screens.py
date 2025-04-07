import pygame
import unittest
from unittest.mock import patch
from Final_Project_Battle import config
from Final_Project_Battle.game_data import GameData
from Final_Project_Battle.gui_elements import GUIElements
from Final_Project_Battle.main_screen import MainScreen
from Final_Project_Battle.choose_char_screen import ChooseCharScreen
from Final_Project_Battle.battle_screen import BattleScreen
from Final_Project_Battle.result_screen import ResultScreen

class TestScreens(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        self.game_data = GameData()

        # Create main_screen with the same buttons in MainScreen
        self.main_screen = MainScreen(self.screen)
        button_data = [
            {"text": "1. Start Game", "pos": (300, 200), "size": (200, 50)},
            {"text": "2. Exit", "pos": (300, 400), "size": (200, 50)},
        ]
        self.main_screen.buttons = GUIElements.create_buttons(button_data)

        # Create choose_char_screen with the same buttons in ChooseCharScreen
        self.choose_char_screen = ChooseCharScreen(self.screen)
        button_data = [
            {"text": "Warrior", "pos": (300, 200), "size": (200, 50)},
            {"text": "Tanker", "pos": (300, 300), "size": (200, 50)},
            {"text": "Magician", "pos": (300, 400), "size": (200, 50)},
        ]
        self.choose_char_screen.buttons = GUIElements.create_buttons(button_data)

        # Create battle_screen with the same buttons in BattleScreen
        self.battle_screen = BattleScreen(self.screen, self.game_data)
        button_data = [
            {"text": "1. Attack", "pos": (300, 250), "size": (200, 50)},
            {"text": "2. Defend", "pos": (300, 350), "size": (200, 50)},
            {"text": "3. Use Special Skill", "pos": (300, 450), "size": (300, 50)},
        ]
        self.battle_screen.buttons = GUIElements.create_buttons(button_data)

        # Create result_screen with the same buttons in ResultScreen
        width = config.SCREEN_WIDTH
        height = config.SCREEN_HEIGHT
        self.result_screen = ResultScreen(self.screen, width, height)
        self.result_screen.buttons = [
            {"text": "Restart", "pos": (width // 2 - 75, height // 2 + 50), "size": (150, 50)},
            {"text": "Exit", "pos": (width // 2 - 75, height // 2 + 120), "size": (150, 50)}
        ]

    def tearDown(self):
        pygame.quit()

    # ==== MainScreen unit tests ====

    def test_main_screen_start_game(self):
        # Test handling Start Game
        mock_StartGame = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(350, 220))
        action = self.main_screen.handle_event(mock_StartGame)
        self.assertEqual(action, "start_game")

    @patch("pygame.quit")  # Mock pygame.quit
    @patch("builtins.exit")  # Mock exit
    def test_main_screen_exit_game(self, mock_exit, mock_pygame_quit):
        # Test handling Exit Game
        mock_EndGame = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(350, 420))
        action = self.main_screen.handle_event(mock_EndGame)
        mock_pygame_quit.assert_called_once()
        mock_exit.assert_called_once()

    # ==== ChooseCharScreen unit tests ====

    def test_choose_char_screen_warrior(self):
        # Test handling user choose Warrior
        mock_Warrior = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(350, 220))
        action = self.choose_char_screen.handle_event(mock_Warrior)
        self.assertEqual(action, "Warrior")

    def test_choose_char_screen_tanker(self):
        # Test handling user choose Tanker
        mock_Tanker = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(350, 320))
        action = self.choose_char_screen.handle_event(mock_Tanker)
        self.assertEqual(action, "Tanker")

    def test_choose_char_screen_magician(self):
        # Test handling user choose Magician
        mock_Magician = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(350, 420))
        action = self.choose_char_screen.handle_event(mock_Magician)
        self.assertEqual(action, "Magician")

    # ==== BattleScreen unit tests ====

    def test_battle_screen_attack(self):
        # Test handling attach move
        mock_Attack = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(350, 275))
        action = self.battle_screen.handle_event(mock_Attack)
        self.assertEqual(action, "Attack")

    def test_battle_screen_defend(self):
        # Test handling defend move
        mock_Defend = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(350, 375))
        action = self.battle_screen.handle_event(mock_Defend)
        self.assertEqual(action, "Defend")

    def test_battle_screen_use_skill(self):
        # Test handling use special skill move
        mock_UseSkill = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(350, 475))
        action = self.battle_screen.handle_event(mock_UseSkill)
        self.assertEqual(action, "Use Skill")

    # ==== ResultScreen unit tests ====

    def test_result_screen_restart(self):
        # Test handling restart game
        mock_Restart = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(350, 375))
        action = self.result_screen.handle_event(mock_Restart)
        self.assertEqual(action, "Restart")

    def test_result_screen_exit(self):
        # Test handling exit game
        mock_Exit = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(350, 450))
        action = self.result_screen.handle_event(mock_Exit)
        self.assertEqual(action, "Exit")

if __name__ == "__main__":
    unittest.main()
