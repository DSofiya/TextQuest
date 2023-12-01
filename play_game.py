import pygame
import subprocess
import json
import os


from general_function import load_images, select_font, read_character_info, resource_path


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 228, 181)
RED = (139, 0, 0)


class Game:
    def __init__(self, window_size):
        self.window_size = window_size
        self.renderer = GameRenderer(window_size)
        self.logic = GameLogic(window_size)

    def run(self):
        self.renderer.initialize()
        self.logic.initialize()

        running = True
        while running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                self.logic.handle_event(event)
            self.logic.update()
            self.renderer.render(self.logic)

        self.renderer.quit()


class GameRenderer:
    def __init__(self, window_size):
        self.window_size = window_size
        self.window = None
        self.clock = None

    def initialize(self):
        pygame.init()
        self.image_race, self.image_clas = load_images()
        self.bg_image = pygame.image.load(
            resource_path(os.path.join("Menu_images", "picture_menu.jpg"))
        )
        self.image_fon = pygame.transform.scale(
            pygame.image.load(resource_path(os.path.join("Menu_images", "book.png"))),
            (self.window_size[0] / 2.1, self.window_size[0] / 3),
        )

        self.window = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption("Гра")
        self.clock = pygame.time.Clock()

    def render(self, logic):
        self.window.blit(self.bg_image, (0, 0))
        self.window.blit(
            self.image_fon, (self.window_size[0] / 4, self.window_size[1] / 5)
        )
        self.window.blit(
            self.image_race, (self.window_size[0] / 10, self.window_size[1] / 4)
        )
        self.window.blit(
            self.image_clas, (self.window_size[0] / 1.35, self.window_size[1] / 2.5)
        )
        logic.render(self.window)
        pygame.display.flip()

    def quit(self):
        pygame.quit()


class JSONReader:
    def read_json_file(self, filename_for_read):
        with open(filename_for_read, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data

    def write_json_file(self, existing_data, filename):
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(existing_data, file, ensure_ascii=False, indent=4)


class TextBot:
    def __init__(self):
        (
            self.race_name,
            self.clas_name,
            self.addition,
            self.name,
            self.first_file_path,
            self.file_path_item,
        ) = read_character_info()
        self.reader = JSONReader()
        self.chat_response = ""
        self.ansver2 = ""
        self.ansver1 = ""
        self.gold = 0

    def generate_response(self, current_filename):
        json_data = self.reader.read_json_file(current_filename)
        description = json_data.get("description", "")
        ansvers = json_data.get("ansvers", {})
        self.ansver1 = ansvers.get("ansver1", [])
        self.ansver2 = ansvers.get("ansver2", [])
        items = json_data.get("items", {})
        items = {key: value for key, value in items.items() if value.lower() == "true"}
        existing_data = self.reader.read_json_file(self.file_path_item)
        for key, value in items.items():
            existing_data[key] = "True" if value.lower() == "true" else "False"
        self.reader.write_json_file(existing_data, self.file_path_item)
        self.chat_response = description.strip()

    def process_answer(self, choice_filename):
        choice_filename = resource_path(os.path.join(choice_filename[1], choice_filename[2], choice_filename[3]))
        json_data_choice = self.reader.read_json_file(choice_filename)
        existing_data = self.reader.read_json_file(self.file_path_item)
        true_values = [
            value.lower() == "true"
            for key, value in existing_data.items()
            if "folse" not in key.lower()
        ]
        all_key = [key for key, value in existing_data.items() if "folse" not in key.lower()]
        if true_values == len(all_key):
            next_filename = (json_data_choice.get("next_end", []) if json_data_choice.get("next_end") else None)
        else:
            next_filename = ( json_data_choice.get("next", []) if json_data_choice.get("next") else None)

        gold = int(json_data_choice.get("currency", {}).get("gold", 0))
        self.gold += gold
        selection = json_data_choice.get("selection", {})
        selection = {key: value for key, value in selection.items() if value == "True"}

        suffixes = {
            "class_selection": self.clas_name[1],
            "race_selection": self.race_name[1],
            "gender_selection": self.addition[1]
        }
        if len(selection):
            selection_key = next(iter(selection.keys()))
            selection_as_string = str(selection_key)
            suffix = suffixes[selection_as_string]
        else:
            suffix = ""
        next_filename = resource_path(os.path.join(next_filename[0], next_filename[1], f"{next_filename[2]}{suffix}.json"))

        return next_filename

    def clear_files(self):
        existing_data = self.reader.read_json_file(self.file_path_item)
        for key, value in existing_data.items():
            existing_data[key] = "False"
        self.reader.write_json_file(existing_data, self.file_path_item)


class Button:
    def __init__(self, x, y, width, height, image_path, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.text = text

    def draw_midbottom(self, surface, button_font):
        surface.blit(self.image, self.rect.topleft)
        text_surface = button_font.render(self.text, True, YELLOW)
        text_rect = text_surface.get_rect(center=self.rect.midbottom)
        surface.blit(text_surface, text_rect)

    def draw_center(self, surface, button_font):
        surface.blit(self.image, self.rect.topleft)
        lines = str(self.text).splitlines()
        y_offset = 0
        for line in lines:
            text_surface = button_font.render(line, True, YELLOW)
            text_rect = text_surface.get_rect(
                centerx=self.rect.centerx, centery=self.rect.centery + y_offset
            )
            surface.blit(text_surface, text_rect)
            y_offset += text_rect.height

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


class GameLogic:
    def __init__(self, window_size):
        self.window_size = window_size
        self.textbot = TextBot()
        self.scroll_y = 0
        self.char_index = 0
        self.time_passed = 0
        self.textbot.generate_response(self.textbot.first_file_path)
        self.buttons = self.load_buttons(
            self.textbot.ansver1[0], self.textbot.ansver2[0], self.textbot.gold
        )

    def initialize(self):
        self.button_font, self.menu_font, self.big_font = select_font()

    def handle_event(self, event):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] and self.scroll_y < 0:
            self.scroll_y += 20
        if keys[pygame.K_DOWN] and self.scroll_y > -(
            len(self.textbot.chat_response) * self.menu_font.get_linesize()
            - self.window_size[1] // 5
        ):
            self.scroll_y -= 20
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
            for button in self.buttons:
                if button.is_clicked(pos):
                    self.handle_button_click(button)

    def handle_button_click(self, button):
        if button == self.buttons[2]:
            self.textbot.clear_files()
            pygame.quit()
            subprocess.run(["python", resource_path("main.py")])
        elif button == self.buttons[0] and self.scroll_y < 0:
            self.scroll_y += 20
        elif button == self.buttons[1] and self.scroll_y > -(
            len(self.textbot.chat_response) * self.menu_font.get_linesize()
            - self.window_size[1] // 5
        ):
            self.scroll_y -= 20
        elif button == self.buttons[3]:
            if self.textbot.ansver1[1] == "":
                self.textbot.clear_files()
                pygame.quit()
                subprocess.run(["python", resource_path("main.py")])
            else:
                current_filename = self.textbot.process_answer(self.textbot.ansver1)
                self.textbot.generate_response(current_filename)
                self.char_index = 0
        elif button == self.buttons[4]:
            if self.textbot.ansver1[1] == "":
                self.textbot.clear_files()
                pygame.quit()
                subprocess.run(["python", resource_path("main.py")])
            else:
                current_filename = self.textbot.process_answer(self.textbot.ansver2)
                self.textbot.generate_response(current_filename)
                self.char_index = 0

    def update(self):
        time_delta = pygame.time.get_ticks() - self.time_passed
        self.time_passed += time_delta
        if self.time_passed > 100 and self.char_index < len(self.textbot.chat_response):
            self.char_index += 1
            self.time_passed = 0

    def render(self, surface):
        y_position = self.window_size[1] // 4
        x_position = self.window_size[0] // 3.5
        displayed_text = self.textbot.chat_response[: self.char_index]
        current_line = ""

        for char in displayed_text:
            current_line += char
            text_width, _ = self.menu_font.size(current_line)
            char_width, _ = self.menu_font.size(char)
            if text_width > self.window_size[0] / 3 and char == " " or char == ":":
                chat_surface = self.menu_font.render(char, True, BLACK)
                surface.blit(chat_surface, (x_position, y_position + self.scroll_y))
                y_position += self.menu_font.get_linesize()
                current_line = char
                x_position = self.window_size[0] / 3.5
            else:
                chat_surface = self.menu_font.render(char, True, BLACK)
                surface.blit(chat_surface, (x_position, y_position + self.scroll_y))
                x_position += char_width

        y_position += self.menu_font.get_linesize()
        self.buttons = self.load_buttons(
            self.textbot.ansver1[0], self.textbot.ansver2[0], self.textbot.gold
        )
        for button in self.buttons[:3]:
            button.draw_midbottom(surface, self.button_font)
        for button in self.buttons[3:]:
            button.draw_center(surface, self.menu_font)

    def load_buttons(self, ansver1, ansver2, count_gold):
        buttons_data = [
            {
                "x": self.window_size[0] / 1.43,
                "y": self.window_size[1] / 4.5,
                "width": self.window_size[0] / 22,
                "height": self.window_size[0] / 22,
                "image_path": resource_path(os.path.join("Menu_images", "arroy2_up.png")),
                "text": "",
            },
            {
                "x": self.window_size[0] / 1.43,
                "y": self.window_size[1] / 2.5,
                "width": self.window_size[0] / 22,
                "height": self.window_size[0] / 22,
                "image_path": resource_path(os.path.join("Menu_images", "arroy2_down.png")),
                "text": "",
            },
            {
                "x": self.window_size[0] / 1.33,
                "y": self.window_size[1] / 7,
                "width": self.window_size[0] / 10,
                "height": self.window_size[1] / 5,
                "image_path": resource_path(os.path.join("Character", "exit.png")),
                "text": "Вихід до головного меню ",
            },
            {
                "x": self.window_size[0] / 8,
                "y": self.window_size[1] / 1.7,
                "width": self.window_size[0] / 3,
                "height": self.window_size[0] / 5,
                "image_path": resource_path(os.path.join("Menu_images", "button.png")),
                "text": ansver1,
            },
            {
                "x": self.window_size[0] / 2,
                "y": self.window_size[1] / 1.7,
                "width": self.window_size[0] / 3,
                "height": self.window_size[0] / 5,
                "image_path": resource_path(os.path.join("Menu_images", "button.png")),
                "text": ansver2,
            },
            {
                "x": self.window_size[0] / 4.2,
                "y": self.window_size[1] / 5.8,
                "width": self.window_size[0] / 25,
                "height": self.window_size[0] / 15,
                "image_path": resource_path(os.path.join("Menu_images", "gold.png")),
                "text": count_gold,
            },
        ]

        buttons = [
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

        return buttons


def main():
    bg_image = pygame.image.load(resource_path(os.path.join("Menu_images", "picture_menu.jpg")))
    window_size = bg_image.get_size()
    game = Game(window_size)
    game.run()


if __name__ == "__main__":
    main()
