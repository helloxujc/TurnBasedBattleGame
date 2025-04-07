from Final_Project_Battle.character import Player
from Final_Project_Battle.character import Enemy

class GameData:
    def __init__(self):
        # Initialize the player and enemy
        self.player = Player()
        self.player.set_character("Warrior")
        self.enemy = Enemy()

    def reset(self):
        self.player.reset()
        self.enemy.reset()