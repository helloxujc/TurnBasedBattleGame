from unittest.mock import MagicMock, patch
from Final_Project_Battle.game_logic import GameLogic
import pygame

def test_play_turn_skill_in_cooldown(mocker):
    mock_game_data = MagicMock()
    mock_battle_screen = MagicMock()
    test_game_logic = GameLogic(mock_game_data,mock_battle_screen)

    mocker.patch.object(test_game_logic, 'handle_player_turn', return_value = (None,0,0,""))
    mocker.patch.object(test_game_logic, 'update_move_log')
    mocker.patch.object(test_game_logic, 'handle_enemy_turn')
    mocker.patch.object(test_game_logic, 'check_status', return_value = False)

    mocker.patch.object(pygame.display,'update')

    test_game_logic.play_turn()
    test_game_logic.update_move_log.assert_called_once_with(False,"Skill is still in cooldown. Please choose another action.")
    pygame.display.update.assert_called_once()

def test_play_turn_skill_both_defend(mocker):
    mock_game_data = MagicMock()
    mock_battle_screen = MagicMock()
    test_game_logic = GameLogic(mock_game_data, mock_battle_screen)

    mocker.patch.object(test_game_logic, 'handle_player_turn', return_value=("Defend", 0, 10, "Player defends"))
    mocker.patch.object(test_game_logic, 'handle_enemy_turn', return_value=("Defend", 0, 10, "Enemy defends"))
    mocker.patch.object(test_game_logic, 'update_move_log')
    mocker.patch.object(test_game_logic, 'check_status', return_value=False)
    mocker.patch.object(pygame.display, 'update')

    test_game_logic.play_turn()

    test_game_logic.update_move_log.assert_called_once_with(True,"Both sides are defending. No damage dealt this round.")
    pygame.display.update.assert_called_once()

def test_play_turn_skill_both_attack(mocker):
    mock_game_data = MagicMock()
    mock_battle_screen = MagicMock()
    test_game_logic = GameLogic(mock_game_data, mock_battle_screen)

    mocker.patch.object(test_game_logic, 'handle_player_turn', return_value=("Attack", 10, 0, "Player attacks"))
    mocker.patch.object(test_game_logic, 'handle_enemy_turn', return_value=("Attack", 5, 0, "Enemy attacks"))
    mocker.patch.object(test_game_logic, 'update_move_log')
    mocker.patch.object(test_game_logic, 'check_status', return_value=False)
    mocker.patch.object(pygame.display, 'update')

    mock_game_data.player.character.current_hp = 100
    mock_game_data.enemy.character.current_hp = 100
    test_game_logic.play_turn()

    assert mock_game_data.player.character.current_hp == 100 - 5
    assert mock_game_data.enemy.character.current_hp == 100 - 10

    test_game_logic.update_move_log.assert_any_call(True,"Player attacks")
    test_game_logic.update_move_log.assert_any_call(True, "Enemy attacks")
    pygame.display.update.assert_called_once()

def test_handle_player_turn_normal_case():
    mock_game_data = MagicMock()
    mock_battle_screen = MagicMock()
    test_game_logic = GameLogic(mock_game_data, mock_battle_screen)

    mock_character = mock_game_data.player.character
    mock_character.attack.return_value = 10
    test_game_logic.player_action = "Attack"

    action, damage, defense, move_info = test_game_logic.handle_player_turn()

    assert action == "Attack"
    assert damage == 10
    assert defense == 0
    assert move_info == "Player attacks and inflicts 10 damage points."
    mock_character.attack.assert_called_once()

def test_handle_player_turn_skill_in_cooldown():
    mock_game_data = MagicMock()
    mock_battle_screen = MagicMock()
    test_game_logic = GameLogic(mock_game_data, mock_battle_screen)

    mock_character = mock_game_data.player.character
    mock_character.skill_requirement.return_value = False
    test_game_logic.player_action = "Use Skill"

    action, damage, defense, move_info = test_game_logic.handle_player_turn()

    assert action is None
    assert damage == 0
    assert defense == 0
    assert move_info == ""

def test_handle_enemy_turn_normal_case():
    mock_game_data = MagicMock()
    mock_battle_screen = MagicMock()
    test_game_logic = GameLogic(mock_game_data, mock_battle_screen)
    mock_character = mock_game_data.enemy.character
    mock_character.skill_requirement.return_value = True
    mock_character.attack.return_value = 10
    mock_character.defend.return_value = 0
    mock_character.current_hp = 80
    mock_character.max_hp = 100

    with patch("random.choice", return_value = "Attack"):
        action, damage, defense, move_info = test_game_logic.handle_enemy_turn()

    assert action == "Attack"
    assert damage == 10
    assert defense == 0
    assert move_info == "Enemy attacks and inflicts 10 damage points."
    mock_character.attack.assert_called_once()

def test_handle_enemy_turn_skill_is_in_cooldown():
    mock_game_data = MagicMock()
    mock_battle_screen = MagicMock()
    test_game_logic = GameLogic(mock_game_data, mock_battle_screen)
    mock_character = mock_game_data.enemy.character
    mock_character.skill_requirement.return_value = False
    mock_character.current_hp = 80
    mock_character.max_hp = 100

    with patch("random.choice", return_value = "Defend"):
        action, damage, defense, move_info = test_game_logic.handle_enemy_turn()

    assert action == "Defend"
    mock_character.defend.assert_called_once()

def test_check_status_player_loses():
    mock_game_data = MagicMock()
    mock_battle_screen = MagicMock()
    test_game_logic = GameLogic(mock_game_data, mock_battle_screen)
    mock_character = mock_game_data.player.character
    mock_character.current_hp = 0
    mock_game_data.enemy.character.current_hp = 30

    result = test_game_logic.check_status()
    assert result is True
    assert test_game_logic.battle_result == "Enemy"

def test_check_status_enemy_loses():
    mock_game_data = MagicMock()
    mock_battle_screen = MagicMock()
    test_game_logic = GameLogic(mock_game_data, mock_battle_screen)
    mock_character = mock_game_data.enemy.character
    mock_character.current_hp = 0
    mock_game_data.player.character.current_hp = 30

    result = test_game_logic.check_status()
    assert result is True
    assert test_game_logic.battle_result == "Player"

def test_check_status_game_continues():
    mock_game_data = MagicMock()
    mock_battle_screen = MagicMock()
    test_game_logic = GameLogic(mock_game_data, mock_battle_screen)
    mock_game_data.player.character.current_hp = 30
    mock_game_data.enemy.character.current_hp = 30

    result = test_game_logic.check_status()
    assert result is False
    assert test_game_logic.battle_result is None