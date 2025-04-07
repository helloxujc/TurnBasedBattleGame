
from unittest.mock import patch
import pytest
from Final_Project_Battle.character import Character, Warrior, Tanker, Magician

@pytest.fixture
def test_character():
    return Character("test_char",100,(5,10),(5,10),"test_skill")

@patch('random.randint', return_value=8)
@patch('Final_Project_Battle.config.RANDOM_MODIFIER',2)
def test_attack_normal_case(mock_randint, test_character):
    damage = test_character.attack()
    assert damage == 10

@patch('random.randint', return_value=5)
@patch('Final_Project_Battle.config.RANDOM_MODIFIER',-5)
def test_attack_minimum_damage(mock_randint, test_character):
    damage = test_character.attack()
    assert damage == 1

@patch('random.randint', return_value=10)
@patch('Final_Project_Battle.config.RANDOM_MODIFIER',5)
def test_attack_maximum_damage(mock_randint, test_character):
    damage = test_character.attack()
    assert damage == 15

@patch('random.randint', return_value=8)
@patch('Final_Project_Battle.config.RANDOM_MODIFIER',2)
def test_defense_normal_case(mock_randint, test_character):
    defense = test_character.defend()
    assert defense == 10

@patch('random.randint', return_value=5)
@patch('Final_Project_Battle.config.RANDOM_MODIFIER',-5)
def test_defense_minimum_damage(mock_randint, test_character):
    defense = test_character.defend()
    assert defense == 1

@patch('random.randint', return_value=10)
@patch('Final_Project_Battle.config.RANDOM_MODIFIER',5)
def test_defense_maximum_damage(mock_randint, test_character):
    defense = test_character.defend()
    assert defense == 15

def test_cap_health(test_character):
    test_character.current_hp = 110
    test_character.cap_health()
    assert test_character.current_hp == test_character.max_hp

def test_use_skill_warrior():
    test_warrior = Warrior()
    mock_defense_value = 10
    mock_random_modifier = 2
    expected_defense = max(mock_defense_value * 1.75 + mock_random_modifier,1)
    with patch('random.randint', return_value = mock_defense_value),\
         patch('Final_Project_Battle.config.RANDOM_MODIFIER', mock_random_modifier):
        damage, defense = test_warrior.use_skill()
    assert damage == 0
    assert defense == expected_defense

def test_use_skill_tanker():
    test_tanker = Tanker()
    mock_attack_value = 10
    mock_random_modifier = 2
    expected_damage = max(mock_attack_value * 1.75 + mock_random_modifier,1)
    with patch('random.randint', return_value = mock_attack_value),\
         patch('Final_Project_Battle.config.RANDOM_MODIFIER', mock_random_modifier):
        damage, defense = test_tanker.use_skill()
    assert damage == expected_damage
    assert defense == 0

def test_use_skill_magician():
    test_tanker = Magician()
    mock_attack_value = 10
    mock_defense_value = 10
    mock_random_modifier = 2
    expected_damage = max(mock_attack_value * 1.25 + mock_random_modifier,1)
    expected_defense = max(mock_defense_value * 1.25 + mock_random_modifier, 1)
    with patch('random.randint', return_value = mock_attack_value),\
         patch('Final_Project_Battle.config.RANDOM_MODIFIER', mock_random_modifier):
        damage, defense = test_tanker.use_skill()
    assert damage == expected_damage
    assert defense == expected_defense
