import pygame

class GUIElements:
    @staticmethod
    def draw_title(screen, text, font, color, y_position):
        """
        Draw the title on the screen.

        :param screen: The pygame screen to draw on.
        :param text: The text content of the title.
        :param font: The pygame font object.
        :param color: The color of the text (tuple, e.g., (255, 255, 255)).
        :param y_position: The vertical position of the title.
        """
        # Render the title text
        title_surface = font.render(text, True, color)
        screen_width = screen.get_width()
        title_width = title_surface.get_width()
        title_x = (screen_width - title_width) // 2  # Center the title horizontally
        screen.blit(title_surface, (title_x, y_position))

    @staticmethod
    def draw_separator_line(screen, color, y_position, width=2):
        """
        Draw a horizontal separator line on the screen.

        :param screen: The pygame screen to draw on.
        :param color: The color of the line (tuple, e.g., (255, 255, 255)).
        :param y_position: The vertical position of the line.
        :param width: The thickness of the line (default is 2).
        """
        screen_width = screen.get_width()  # Get the width of the screen
        pygame.draw.line(screen, color, (0, y_position), (screen_width, y_position), width)

    @staticmethod
    def calculate_progress_bar_positions(line_y, progress_bar_offset, gap_between_bars):
        """
        Calculate the y-coordinates for the player and enemy progress bars.

        :param line_y: The y-coordinate of the separator line.
        :param progress_bar_offset: The vertical offset from the separator line to the player's progress bar.
        :param gap_between_bars: The vertical gap between the player's and enemy's progress bars.
        :return: A tuple containing the y-coordinates of the player's and enemy's progress bars.
        """
        player_bar_y = line_y + progress_bar_offset
        enemy_bar_y = player_bar_y + gap_between_bars
        return player_bar_y, enemy_bar_y

    @staticmethod
    def create_buttons(button_data):
        """
        Create a generic method for button creation
        """
        return [
            {"rect": pygame.Rect(data["pos"][0], data["pos"][1], data["size"][0], data["size"][1]),
             "text": data["text"]}
            for data in button_data
        ]

    @staticmethod
    def draw_button(screen, button, font, button_color, border_color, text_color=(255, 255, 255)):
        """
        Draw a single button, including the background, border, and text
        """
        pygame.draw.rect(screen, button_color, button["rect"])
        pygame.draw.rect(screen, border_color, button["rect"], width=2)
        text = font.render(button["text"], True, text_color)
        text_rect = text.get_rect(center=button["rect"].center)
        screen.blit(text, text_rect)

    @staticmethod
    def on_button_click(button_text, context=None):
        """Perform actions based on the button's text and context"""
        if context == "main_screen":
            if button_text == "1. Start Game":
                print("Start Game clicked!")
                return "start_game"  # Return a flag for state switching
            elif button_text == "2. Exit":
                print("Exit clicked!")
                pygame.quit()
                exit()

        elif context == "help_screen":
            if button_text == "Back":
                print("Returning to main menu")
                return "back"

        elif context == "battle_screen":
            if button_text == "1. Attack":
                print("Attack action triggered!")
                return "Attack"
            elif button_text == "2. Defend":
                print("Defend action triggered!")
                return "Defend"
            elif button_text == "3. Use Special Skill":
                print("Use Special Skill action triggered!")
                return "Use Skill"

        return None  # Default to no action



class ProgressBar:
    def __init__(self, screen, pos, size, max_hp, current_hp, color, label):
        self.screen = screen
        self.pos = pos  # Coordinates of the progress bar (x, y)
        self.size = size  # Dimensions of the progress bar (width, height)
        self.max_hp = max_hp  # Maximum value (e.g., initial HP)
        self.current_hp = current_hp  # Current value
        self.color = color  # Progress bar color
        self.label = label  # Progress bar label text
        self.font = pygame.font.Font(None, 24)  #  Initialize font

    def set_position(self, pos):
        """
        Update the position of the progress bar
        """
        self.pos = pos

    def render(self, current_hp):
        """
        Render the progress bar and label
        """
        # Calculate the current width of the progress bar
        bar_width = (self.current_hp / self.max_hp) * self.size[0]

        # Draw the background box
        pygame.draw.rect(self.screen, (100, 100, 100), (*self.pos, *self.size))

        # Draw the progress bar
        pygame.draw.rect(self.screen, self.color, (*self.pos, bar_width, self.size[1]))

        # Draw the label text
        if self.label:
            # Clear the text area to ensure no overlapping shadows
            label_clear_rect = pygame.Rect(self.pos[0], self.pos[1] - 25, self.size[0], 25)

            # Create a surface
            label_surface = pygame.Surface((label_clear_rect.width, label_clear_rect.height), pygame.SRCALPHA)

            # Fill with the blue color
            label_surface.fill((50, 50, 200))

            # Blit the surface
            self.screen.blit(label_surface, (label_clear_rect.x, label_clear_rect.y))

            # Construct the display content, such as 'Player: 80/100'
            self.current_hp = current_hp
            label_text = f"{self.label}: {self.current_hp}/{self.max_hp}"
            label_surface_text = self.font.render(label_text, True, (255, 255, 255))  # White text

            # The label is displayed above the progress bar
            label_pos = (self.pos[0], self.pos[1] - 25)
            self.screen.blit(label_surface_text, label_pos)

    def get_rect(self):
        return pygame.Rect(self.pos[0], self.pos[1]-25, self.size[0], self.size[1]+25)