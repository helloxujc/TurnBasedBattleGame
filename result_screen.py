import pygame
from Final_Project_Battle import config

class ResultScreen:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.button_border_color = config.WHITE
        self.background_image = pygame.image.load("images/game_screen_background.png")
        self.background_image = pygame.transform.scale(self.background_image,
                                                       (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        # Scale the image to fit the screen size
        self.buttons = [
            {"text": "Restart", "pos": (width // 2 - 75, height // 2 + 50), "size": (150, 50)},
            {"text": "Exit", "pos": (width // 2 - 75, height // 2 + 120), "size": (150, 50)}
        ]

    def render(self, winner):
        # Display the background image
        self.screen.blit(self.background_image, (0, 0))  # Set up background image, (0,0) is the top-left corner

        # Draw the victory message
        font = pygame.font.Font(None, 60)
        result_text = f"{winner} Wins!"
        text_surface = font.render(result_text,
                                   True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.width // 2,
                                                  self.height // 2 - 50))
        self.screen.blit(text_surface, text_rect)

        # Draw the buttons
        for button in self.buttons:
            pygame.draw.rect(self.screen, (0, 0, 255),
                             (*button["pos"], *button["size"]))

            # Draw the white border around the button
            border_rect = pygame.Rect(button["pos"][0] - 2,
                                      button["pos"][1] - 2,
                                      button["size"][0] + 4,
                                      button["size"][1] + 4)

            pygame.draw.rect(self.screen, self.button_border_color,
                             border_rect, 2)  # 2 is the border thickness

            button_font = pygame.font.Font(None, 40)
            button_text = button_font.render(button["text"],
                                             True, (255, 255, 255))
            text_rect = button_text.get_rect(center=(button["pos"][0] + button["size"][0] // 2,
                                                     button["pos"][1] + button["size"][1] // 2))
            self.screen.blit(button_text, text_rect)

        pygame.display.flip()

    def handle_event(self, event):
        """Handle button clicks and return the appropriate state."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            for button in self.buttons:
                rect = pygame.Rect(button["pos"], button["size"])
                if rect.collidepoint(mouse_pos):
                    return button["text"]
        return None