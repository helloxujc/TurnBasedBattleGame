import pygame

from Final_Project_Battle import config
from Final_Project_Battle.gui_elements import GUIElements
from Final_Project_Battle.gui_elements import ProgressBar

class BattleScreen:
    def __init__(self, screen, game_data):
        self.screen = screen
        self.game_data = game_data
        self.text_color = config.WHITE
        self.button_color = config.BLUE
        self.button_border_color = config.WHITE
        self.font = pygame.font.Font(None, 36)
        self.background_color = config.GREEN
        self.background_image = pygame.image.load("images/game_screen_background.png")
        self.background_image = pygame.transform.scale(self.background_image,
                                                       (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
                                                        # Scale the image to fit the screen size
        self.character_images = {
            "Warrior": "red_bird_512.png",
            "Tanker": "yellow_bird_512.png",
            "Magician": "black_bird_512.png",
        }

        self.buttons = []
        self.move_log = []  # Initialize the move log

        # Progress bars
        self.player_bar = ProgressBar(
            screen,pos=(50, 50), size=(300, 20),
            max_hp=self.game_data.player.character.max_hp,
            current_hp=self.game_data.player.character.current_hp,
            color=(0, 255, 0),
            label = "Player")  # Green bar

        self.enemy_bar = ProgressBar(
            screen, pos=(50, 100),
            size=(300, 20),
            max_hp=self.game_data.enemy.character.max_hp,
            current_hp=self.game_data.enemy.character.current_hp,
            color=(255, 0, 0),
            label = "Enemy")  # Red bar

    def update_move_log(self, move_log): # Update the displayed move log on the battle screen
        self.move_log = move_log

    def render(self, full_render):
        """Render the battle screen"""

        # Fully render the entire battle screen
        if full_render:
            # Display the background image
            self.screen.blit(self.background_image, (0, 0))  # Set up background image, (0,0) is the top-left corner

            # Draw title
            GUIElements.draw_title(
                screen=self.screen,
                text="Welcome to Battle",
                font=pygame.font.Font(None, 48),
                color=(255, 255, 255),
                y_position=20
            )

            # Draw the separator line
            GUIElements.draw_separator_line(
                screen=self.screen,
                color=(255, 255, 255),
                y_position=78,  # title_y (20) + title_height (48) + 10
                width=2
            )

            # Adjust the position of the progress bars and labels
            progress_bar_offset = 40
            gap_between_bars = 70
            player_bar_y, enemy_bar_y = GUIElements.calculate_progress_bar_positions(
                line_y=78,  # y-coordinate of the line dividing two bars
                progress_bar_offset=progress_bar_offset,
                gap_between_bars=gap_between_bars
            )

            self.player_bar.set_position((50, player_bar_y))  # The position of the player's progress bar
            self.enemy_bar.set_position((50, enemy_bar_y))  # The position of the enemy's progress bar

            self.player_bar.render(self.game_data.player.character.current_hp)
            self.enemy_bar.render(self.game_data.enemy.character.current_hp)

            # Define the button layout
            button_data = [
                {"text": "1. Attack", "pos": (300, 250), "size": (180, 40)},
                {"text": "2. Defend", "pos": (300, 350), "size": (180, 40)},
                {"text": "3. Use Special Skill", "pos": (300, 450), "size": (270, 40)},
            ]
            self.buttons = GUIElements.create_buttons(button_data)  # Create button data

            # Draw each button
            for button in self.buttons:
                GUIElements.draw_button(
                    screen=self.screen,
                    button=button,
                    font=self.font,
                    button_color=self.button_color,
                    border_color=self.button_border_color,
                    text_color=self.text_color,
                )

            # Refresh the screen
            pygame.display.flip()

        else:
            # Render only the progress bar
            self.player_bar.render(self.game_data.player.character.current_hp)
            self.enemy_bar.render(self.game_data.enemy.character.current_hp)

            # Get the rendering area of the progress bar (assuming get_rect() returns the area)
            player_bar_rect = self.player_bar.get_rect()
            enemy_bar_rect = self.enemy_bar.get_rect()

            # Refresh only the area of the progress bar
            pygame.display.update([player_bar_rect, enemy_bar_rect])

        # Clear the move log area before rendering the move log
        log_area_rect = pygame.Rect(50, 550, self.screen.get_width() - 300, 90)
        self.screen.fill(self.background_color, log_area_rect)

        # Display the move log on the screen
        y_offset = 550
        for move in self.move_log:
            move_text = pygame.font.SysFont("Arial", 10).render(move, True, (0, 0, 0))
            self.screen.blit(move_text, (50, y_offset))
            y_offset += 15

    # Handle events for the battle screen
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            print(f"Mouse clicked at: {mouse_pos}")  # Print the mouse click position
            for button in self.buttons:
                print(f"Checking button rect: {button['rect']}")  # Print the button's area
                if button["rect"].collidepoint(mouse_pos):
                    action = GUIElements.on_button_click(button["text"], context="battle_screen")
                    print(f"Button clicked: {action}")  # Debug information
                    return action
        return None