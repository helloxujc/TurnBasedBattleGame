"""
Final_Project_Battle
│
├── main.py                             # Game entry file
├── character.py                        # Include the Character Class, 3 subclasses, and Player and Enemy Classes
├── game_data.py                        # Initialize the Player and Enemy objects
├── game_logic.py                       # Define the Game class to manage game logic
├── game_gui_manager.py                 # Define the GameUI class to manage the graphical interface
├        ├── ── main_screen.py
├        ├── ── battle_screen.py
├        ├── ── choose_char_screen.py
├        ├── ── result_screen.py
├        ├── ── gui_elements.py         # Helper functions for GUI
└── config.py                           # Store constants (e.g., screen size, color schemes)
"""

import pygame
import sys

from Final_Project_Battle import config
from Final_Project_Battle.game_data import GameData
from Final_Project_Battle.game_gui_manager import GameGUIManager

def main():
    # Initialize the pygame library and load all of its modules.
    pygame.init()

    # Initialize the clock
    clock = pygame.time.Clock()

    # Create a window with its size configured in the global 'config' file.
    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))

    #Set the window title configured in the global 'config' file，displayed at the top of the window.
    pygame.display.set_caption(config.WINDOW_TITLE)

    # Create an instance of GameData
    game_data = GameData()

    # Create an instance of GameGUIManager.
    gui_manager = GameGUIManager(screen, game_data)

    # Set a flag variable to control whether the main loop continues running.
    # When running is set to False, the main loop will end, and the program will exit.
    running = True

    #The main loop begins, and the program will repeatedly execute this loop until running is set to False.
    while running:
        for event in pygame.event.get():        # Retrieve all currently occurring events (e.g., key presses, mouse clicks, window close events, etc.)
            if event.type == pygame.QUIT:       # Check if the event type is a user request to exit (e.g., clicking the window's close button)
                running = False                 # If yes, set running to 'False' to end the main loop.
                pygame.quit()                   # Close the Pygame module and release resources.
                sys.exit()                      # Completely exit the program.

            gui_manager.handle_event(event)

        gui_manager.render()

        clock.tick(config.FPS)

# Call the main function
if __name__ == "__main__":
    main()