import pygame
import sys
import os
import subprocess
import pyperclip
import json
from general_function import load_images, select_font, resource_path

YELLOW = (255, 228, 181)
RED = (139, 0, 0)


class Button:
    def __init__(self, x, y, width, height, image_path, text, callback=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.text = text
        self.callback = callback

    def draw(self, surface, text_position, button_font):
        surface.blit(self.image, self.rect.topleft)
        text_surface = button_font.render(self.text, True, YELLOW)
        if text_position:
            text_rect = text_surface.get_rect(center=self.rect.midbottom)
        else:
            text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

    def handle_click(self):
        if self.callback:
            self.callback()


class Menu:
    def __init__(self):
        pygame.init()
        self.found = True
        self.api_key_text = ""
        self.bg_image = pygame.image.load(resource_path(os.path.join("Menu_images", "picture_menu.jpg")))
        self.WINDOW_SIZE = self.bg_image.get_size()
        self.window = pygame.display.set_mode(self.WINDOW_SIZE)
        pygame.display.set_caption("Вибір пригоди")
        self.initialize_game()

    def initialize_game(self):
        self.image_race, self.image_clas = load_images()
        self.button_font, self.menu_font, self.big_font = select_font()
        self.buttons = self.load_buttons()

    def load_buttons(self):
        config = {
            "exit": {
                "x": self.WINDOW_SIZE[0] / 1.38,
                "y": self.WINDOW_SIZE[0] / 10,
                "width": self.WINDOW_SIZE[0] / 9,
                "height": self.WINDOW_SIZE[0] / 8,
                "image_path": resource_path(os.path.join("Character", "exit.png")),
                "text": "Вихід до головного меню ",
                "callback": self.exit_game,
            },
            "castle": {
                "x": self.WINDOW_SIZE[0] / 3.5,
                "y": self.WINDOW_SIZE[0] / 8.4,
                "width": self.WINDOW_SIZE[0] / 6,
                "height": self.WINDOW_SIZE[0] / 5.6,
                "image_path": resource_path(os.path.join("Adventure", "castel.jpg")),
                "text": "Вбивство та суд у місті Леоніс",
                "callback": self.start_castle_adventure,
            },
            "hotel": {
                "x": self.WINDOW_SIZE[0] / 2,
                "y": self.WINDOW_SIZE[0] / 8.4,
                "width": self.WINDOW_SIZE[0] / 6,
                "height": self.WINDOW_SIZE[0] / 5.6,
                "image_path": resource_path(os.path.join("Adventure", "hotel.jpg")),
                "text": "Готель 'Етельбург'",
                "callback": self.start_hotel_adventure,
            },
            "town": {
                "x": self.WINDOW_SIZE[0] / 3.5,
                "y": self.WINDOW_SIZE[0] / 3.2,
                "width": self.WINDOW_SIZE[0] / 6,
                "height": self.WINDOW_SIZE[0] / 5.6,
                "image_path": resource_path(os.path.join("Adventure", "town.jpg")),
                "text": "Темна загроза над містом Роузфілд",
                "callback": self.start_town_adventure,
            },
            "save": {
                "x": self.WINDOW_SIZE[0] / 2,
                "y": self.WINDOW_SIZE[0] / 2.2,
                "width": self.WINDOW_SIZE[0] / 9,
                "height": self.WINDOW_SIZE[0] / 16,
                "image_path": resource_path(os.path.join("Menu_images", "button.png")),
                "text": "Зберегти ключ",
                "callback": self.save_api_key,
            },
        }

        buttons = [
            Button(
                data["x"],
                data["y"],
                data["width"],
                data["height"],
                data["image_path"],
                data["text"],
                data["callback"],
            )
            for data in config.values()
        ]

        return buttons

    def exit_game(self):
        subprocess.run(["python", resource_path("main.py")])
        pygame.quit()
        sys.exit()

    def start_castle_adventure(self):
        self.setup_adventure_paths(
            resource_path(os.path.join("Murder_in_city", "beginning", "beginning.json")),
            resource_path(os.path.join("Murder_in_city", "items.json")),
        )

    def start_hotel_adventure(self):
        self.setup_adventure_paths(
            resource_path(os.path.join("Hotel_quest", "beginning", "beginning.json")),
            resource_path(os.path.join("Hotel_quest", "items.json")),
        )

    def start_town_adventure(self):
        with open(
            resource_path(os.path.join("Text_patern", "api_key.txt")), "r", encoding="utf-8"
        ) as file:
            content = file.read()
            if "АПІ" in content:
                self.found = True
                subprocess.run(["python", resource_path("play_game_GPT.py")])
                pygame.quit()
                sys.exit()
            else:
                self.found = False

    def setup_adventure_paths(self, first_file_path, file_path_item):
        path_file = resource_path(os.path.join("Text_patern", "character_info.json"))
        with open(path_file, "r", encoding="utf-8") as file:
            data = json.load(file)
            data["first_file_path"] = first_file_path
            data["file_path_item"] = file_path_item
        with open(path_file, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        subprocess.run(["python", resource_path("play_game.py")])
        pygame.quit()
        sys.exit()

    def save_api_key(self):
        with open(
            resource_path(os.path.join("Text_patern", "api_key.txt")), "w", encoding="utf-8"
        ) as file:
            lines = self.api_key_text.strip("")
            file.writelines(f"АПІ - {lines}")

    def render_menu(self):
        self.window.blit(self.bg_image, (0, 0))
        self.window.blit(
            self.image_race, (self.WINDOW_SIZE[0] / 12, self.WINDOW_SIZE[1] / 4)
        )
        self.window.blit(
            self.image_clas, (self.WINDOW_SIZE[0] / 1.4, self.WINDOW_SIZE[1] / 2.2)
        )

        for button in self.buttons:
            button.draw(self.window, True, self.button_font)
        self.buttons[-1].draw(self.window, False, self.button_font)
      
        user_surface = self.menu_font.render(
            "API key: " + self.api_key_text, True, YELLOW
        )
        self.window.blit(
            user_surface, (self.WINDOW_SIZE[0] / 2, self.WINDOW_SIZE[0] / 2 / 1.1)
        )

        title_lines = [
            "Для гри з позначкою ChatGPT необхідно ввести та",
            "зберегти ваш ключ API з https://platform.openai.com",
        ]
        line_height = 0
        for line in title_lines:
            title_text = self.menu_font.render(line, True, YELLOW)
            self.window.blit(
                title_text,
                (self.WINDOW_SIZE[0] / 2, self.WINDOW_SIZE[0] / 2.44 + line_height),
            )
            line_height += 30

        if not self.found:
            title_text = self.big_font.render(f"Ключ не знайдено", True, RED)
            self.window.blit(
                title_text, (self.WINDOW_SIZE[0] / 4, self.WINDOW_SIZE[0] / 2.8)
            )

        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                for button in self.buttons:
                    if button.is_clicked(pos):
                        button.handle_click()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.api_key_text = self.api_key_text[:-1]
                else:
                    self.api_key_text += event.unicode

                if event.key == pygame.K_v and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    clipboard_text = pyperclip.paste().strip("")
                    if clipboard_text:
                        self.api_key_text += clipboard_text

    def run(self):
        running = True
        while running:
            self.render_menu()
            self.handle_events()


if __name__ == "__main__":
    menu = Menu()
    menu.run()
