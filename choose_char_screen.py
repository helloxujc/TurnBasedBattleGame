import pygame

from Final_Project_Battle import config
from Final_Project_Battle.gui_elements import GUIElements


class ChooseCharScreen:
    def __init__(self, screen):
        self.buttons = []
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 20)
        self.text_color = config.WHITE
        self.button_color = config.BLUE
        self.button_border_color = config.WHITE
        self.background_image = pygame.image.load("images/game_screen_background.png")
        self.background_image = pygame.transform.scale(self.background_image,
                                                       (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
                                                        # Scale the image to fit the screen size
        self.red_warrior = pygame.image.load("images/red_bird_512.png")
        self.yellow_tanker = pygame.image.load("images/yellow_bird_512.png")
        self.black_magician = pygame.image.load("images/black_bird_512.png")

        self.selected_character = None # to store the player's choice

        self.button_rect = pygame.Rect(300, 500, 200, 50)  # Return the button's position and size
        self.buttons = []

        # Define Warrior's abilities
        self.warrior_abilities = [
            "Damage Output: High (Attack range: 10-15)",
            "Damage Resistance: Low (Defense range: 5-10)",
            "Special Skill: Shield Block",
            "(Reduces all incoming damage by 75% for a turn)"
        ]
        # Define Tanker's abilities
        self.tanker_abilities = [
            "Damage Output: Low (Attack range: 5-10)",
            "Damage Resistance: High (Defense range: 10-15)",
            "Special Skill: Fireball",
            "(Increase attack damage by 75% for a turn)"
        ]
        # Define Magician's abilities
        self.magician_abilities = [
            "Damage Output: Moderate (Attack range: 8 - 13)",
            "Damage Resistance: Moderate (Defense range: 8 - 13)",
            "Special Skill: Magic Powder",
            "(Reduces all incoming damage by 25 % and",
            "increases attack damages by 25 % a turn)"
        ]
    def render(self):
        """Render the character selection screen"""
        self.screen.blit(self.background_image, (0, 0))  # Set up background image, (0,0) is the top-left corner

        # Multi-line text wrapping
        instructions = (
            "Choose your character. "
            "Each character will have 3 actions: "
            "Attack, Defend, and Special Skill. "
            "Utilize these actions to take down your enemy "
            "in the Battleground."
        )
        max_width = config.SCREEN_WIDTH - 100  # Allow some margin
        wrapped_text = self.wrap_text(instructions, self.font, max_width)

        # Vertical starting point for text
        start_y = 50
        line_spacing = 10

        for i, line in enumerate(wrapped_text):
            text_surface = self.font.render(line, True, (250, 250, 250))
            text_rect = text_surface.get_rect(
                center=(config.SCREEN_WIDTH // 2, start_y + i * (self.font.get_height() + line_spacing)))
            self.screen.blit(text_surface, text_rect)

        button_data = [
            {"text": "Warrior", "pos": (300, 200), "size": (150, 50)},
            {"text": "Tanker", "pos": (300, 300), "size": (150, 50)},
            {"text": "Magician", "pos": (300, 400), "size": (150, 50)},
        ]

        # Create buttons using GUIElements
        self.buttons = GUIElements.create_buttons(button_data)

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

            # Display the warrior image next to the "Warrior" button
            warrior_button_rect = self.buttons[0]["rect"]  # The "Warrior" button is the first one
            self._display_character_image(self.red_warrior, warrior_button_rect)

            # Display the tanker image next to the "Tanker" button
            tanker_button_rect = self.buttons[1]["rect"]  # The "Tanker" button is the second one
            self._display_character_image(self.yellow_tanker, tanker_button_rect)

            # Display the magician image next to the "Magician" button
            magician_button_rect = self.buttons[2]["rect"]  # The "Magician" button is the third one
            self._display_character_image(self.black_magician, magician_button_rect)

            # Display warrior's abilities to the user to the right of the button
            # Position the abilities text to the right of the "Warrior" button
            abilities_x = warrior_button_rect.right + 13  # 13px space from the button
            abilities_y = warrior_button_rect.top
            for line in self.warrior_abilities:
                abilities_surface = self.small_font.render(line, True, self.text_color)
                self.screen.blit(abilities_surface, (abilities_x, abilities_y))
                abilities_y += self.small_font.get_height() + 5  # Add some spacing between lines

            # Display tanker's abilities to the user to the right of the button
            # Position the abilities text to the right of the "Tanker" button
            abilities_x = tanker_button_rect.right + 13  # 13px space from the button
            abilities_y = tanker_button_rect.top
            for line in self.tanker_abilities:
                abilities_surface = self.small_font.render(line, True, self.text_color)
                self.screen.blit(abilities_surface, (abilities_x, abilities_y))
                abilities_y += self.small_font.get_height() + 5  # Add some spacing between lines

            # Display magician's abilities to the user to the right of the button
            # Position the abilities text to the right of the "Tanker" button
            abilities_x = magician_button_rect.right + 13  # 13px space from the button
            abilities_y = magician_button_rect.top
            for line in self.magician_abilities:
                abilities_surface = self.small_font.render(line, True, self.text_color)
                self.screen.blit(abilities_surface, (abilities_x, abilities_y))
                abilities_y += self.small_font.get_height() + 5  # Add some spacing between lines

        pygame.display.flip()

    def wrap_text(self, text, font, max_width):
        """Text wrapping based on pixel width."""
        words = text.split(' ')
        lines = []
        current_line = []

        for word in words:
            test_line = ' '.join(current_line + [word])  # check the current line with the new word
            if font.size(test_line)[0] <= max_width:
                current_line.append(word)
            else:
                if current_line:  # Add the current line to the list
                    lines.append(' '.join(current_line))
                current_line = [word]  # Start a new line with the current word

        if current_line:  # Add any remaining words as the last line
            lines.append(' '.join(current_line))

        return lines

    def _display_character_image(self, character_image, button_rect):
        """This is a helper function meant to resize and display the character images next to the buttons"""

        # Set a larger target height for the character images (e.g., 1.5 times the button height)
        target_height = button_rect.height * 1.5  # Make character image 1.5 times the button height
        aspect_ratio = character_image.get_width() / character_image.get_height()
        target_width = int(target_height * aspect_ratio)

        # Scale the image to the new size
        resized_character_image = pygame.transform.scale(character_image, (target_width, target_height))

        # Create the rectangle for positioning the image to the left of the button
        # Position the image to the left of the button by adjusting the x-coordinate
        character_image_rect = resized_character_image.get_rect(
            topleft=(button_rect.left - target_width - 10, button_rect.centery - target_height // 2))

        # Blit the resized image onto the screen
        self.screen.blit(resized_character_image, character_image_rect)

    def handle_event(self, event):
        """handle help screen events"""
        if event.type == pygame.MOUSEBUTTONDOWN:  # detect mouse click events
            mouse_pos = event.pos  # get the mouse click position
            for button in self.buttons:
                if button["rect"].collidepoint(mouse_pos): # check which character was selected
                    if button["text"] == "Warrior":
                        self.selected_character = "Warrior"
                        return "Warrior"
                    elif button["text"] == "Tanker":
                        self.selected_character = "Tanker"
                        return "Tanker"
                    elif button["text"] == "Magician":
                        self.selected_character = "Magician"
                        return "Magician"
        return None