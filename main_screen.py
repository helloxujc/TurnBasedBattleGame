import pygame
from Final_Project_Battle import config
from Final_Project_Battle.gui_elements import GUIElements

class MainScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(config.FONT_NAME, config.FONT_SIZE)
        self.font_color = config.WHITE
        self.title_font = pygame.font.Font(None, 50)
        self.font = pygame.font.Font(None, 36)
        self.background_image = pygame.image.load("images/game_screen_background.png")
        self.background_image = pygame.transform.scale(self.background_image,
                                                       (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
                                                        # Scale the image to fit the screen size
        self.button_color = config.BLUE
        self.button_border_color = config.WHITE
        self.buttons = []

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            for button in self.buttons:
                if button["rect"].collidepoint(mouse_pos):
                    return GUIElements.on_button_click(button["text"], context="main_screen")
        return None


    def render(self):
        """Render the main menu interface"""
        self.screen.blit(self.background_image, (0, 0))  # Set up background image, (0,0) is the top-left corner

        # Draw the main title
        title_text = "Welcome to the Battleground!"
        title_surface = self.title_font.render(title_text, True, self.font_color)  # Corrected rendering
        title_rect = title_surface.get_rect(center=(config.SCREEN_WIDTH // 2, 100))  # Centered at the top
        self.screen.blit(title_surface, title_rect)

        # Button data
        button_data = [
            {"text": "1. Start Game", "pos": (300, 200), "size": (200, 50)},
            {"text": "2. Exit", "pos": (300, 400), "size": (200, 50)},
        ]

        # Create buttons using GUIElements
        self.buttons = GUIElements.create_buttons(button_data)

        for button in self.buttons:
            # Draw buttons using GUIElements
            GUIElements.draw_button(
                screen=self.screen,
                button=button,
                font=self.font,
                button_color=self.button_color,
                border_color=self.button_border_color
            )

        # Update the screen
        pygame.display.flip()

