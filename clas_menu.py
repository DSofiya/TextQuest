import pygame
import subprocess
import sys
import os
import json
from general_function import select_font, sufix_images, resource_path


class Button:
    def __init__(self, x, y, width, height, image_path, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.text = text

    def draw(self, surface, button_font):
        surface.blit(self.image, self.rect.topleft)
        text_surface = button_font.render(self.text, True, (255, 228, 181))
        text_rect = text_surface.get_rect(center=self.rect.midbottom)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


class CharacterSelector:
    def __init__(self, bg_image, window_size):
        self.bg_image = bg_image
        self.window_size = window_size
        self.button_font, _, self.big_font = select_font()
        self.load_buttons()

    def load_buttons(self):
        buttons_data = [
            {
                "x": self.window_size[0] / 5,
                "y": self.window_size[0] / 8,
                "width": self.window_size[0] / 6,
                "height": self.window_size[0] / 5.8,
                "image_path": resource_path(os.path.join("Character", "Bard.png")),
                "text": "Бард",
            },
            {
                "x": self.window_size[0] / 2.2,
                "y": self.window_size[0] / 8,
                "width": self.window_size[0] / 6,
                "height": self.window_size[0] / 5.8,
                "image_path": resource_path(os.path.join("Character", "Cleric.png")),
                "text": "Клірик",
            },
            {
                "x": self.window_size[0] / 2.2,
                "y": self.window_size[0] / 3.2,
                "width": self.window_size[0] / 6,
                "height": self.window_size[0] / 5.8,
                "image_path": resource_path(os.path.join("Character", "Fighter.png")),
                "text": "Воїн",
            },
            {
                "x": self.window_size[0] / 5,
                "y": self.window_size[0] / 3.2,
                "width": self.window_size[0] / 6,
                "height": self.window_size[0] / 5.8,
                "image_path": resource_path(os.path.join("Character", "Wizard.png")),
                "text": "Чарівник",
            },
            {
                "x": self.window_size[0] / 1.35,
                "y": self.window_size[0] / 10,
                "width": self.window_size[0] / 10,
                "height": self.window_size[0] / 10,
                "image_path": resource_path(os.path.join("Character", "exit.png")),
                "text": "Вихід до головного меню ",
            },
        ]

        self.buttons = [
            Button(
                data["x"],
                data["y"],
                data["width"],
                data["height"],
                data["image_path"],
                data["text"],
            )
            for data in buttons_data
        ]

    def display_menu(self):
        window = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption("Вибір класу героя")

        running = True
        while running:
            window.blit(self.bg_image, (0, 0))
            title_text = self.big_font.render(
                "Обери клас персонажа", True, (255, 228, 181)
            )
            window.blit(
                title_text, (self.window_size[0] / 3.5, self.window_size[0] / 9)
            )

            for button in self.buttons:
                button.draw(window, self.button_font)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    for button in self.buttons:
                        if button.is_clicked(pos):
                            self.handle_button_click(button)

        pygame.quit()
        sys.exit()

    def handle_button_click(self, button):
        if button == self.buttons[-1]:
            pygame.quit()
            subprocess.run(["python", resource_path("main.py")])
        else:
            class_name = button.text
            path_file = resource_path(os.path.join("Text_patern", "character_info.json"))
            with open(path_file, "r", encoding="utf-8") as file:
                data = json.load(file)
                suffix = sufix_images(button.text)
                selected_class = [f"Мій клас - {class_name}", suffix]
                data["class"] = selected_class
            with open(path_file, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            pygame.quit()
            subprocess.run(["python", resource_path("name_character.py")])


if __name__ == "__main__":
    pygame.init()
    bg_image = pygame.image.load(resource_path(os.path.join("Menu_images", "picture_menu.jpg")))
    WINDOW_SIZE = bg_image.get_size()
    character_selector = CharacterSelector(bg_image, WINDOW_SIZE)
    character_selector.display_menu()
