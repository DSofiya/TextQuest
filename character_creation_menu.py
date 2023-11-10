import pygame
import sys
import os
import subprocess
import json


from general_function import select_font, sufix_images


class Button:
    def __init__(self, x, y, width, height, image_path, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.text = text

    def draw(self, surface, button_font):
        surface.blit(self.image, self.rect.topleft)
        text_surface = button_font.render(self.text, True, YELLOW)
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
                "x": self.window_size[0] / 8,
                "y": self.window_size[0] / 8,
                "width": self.window_size[0] / 7,
                "height": self.window_size[0] / 4.5,
                "image_path": os.path.join("Character", "Human_m.png"),
                "image_path_f": os.path.join("Character", "Human_f.png"),
                "text": "Людина",
            },
            {
                "x": self.window_size[0] / 1.8,
                "y": self.window_size[0] / 8,
                "width": self.window_size[0] / 7,
                "height": self.window_size[0] / 4,
                "image_path": os.path.join("Character", "Tieflings_m.png"),
                "image_path_f": os.path.join("Character", "Tieflings_f.png"),
                "text": "Тифлінг",
            },
            {
                "x": self.window_size[0] / 2.2,
                "y": self.window_size[0] / 4,
                "width": self.window_size[0] / 7,
                "height": self.window_size[0] / 4.5,
                "image_path": os.path.join("Character","Ork_m.png"),
                "image_path_f": os.path.join("Character", "Ork_f.png"),
                "text": "Орк",
            },
            {
                "x": self.window_size[0] / 1.5,
                "y": self.window_size[0] / 3.5,
                "width": self.window_size[0] / 7,
                "height": self.window_size[0] / 5.5,
                "image_path": os.path.join("Character", "Gnomes_m.png"),
                "image_path_f": os.path.join("Character", "Gnomes_f.png"),
                "text": "Гном",
            },
            {
                "x": self.window_size[0] / 2.8,
                "y": self.window_size[0] / 8,
                "width": self.window_size[0] / 8,
                "height": self.window_size[0] / 4.5,
                "image_path": os.path.join("Character", "Elves_m.png"),
                "image_path_f": os.path.join("Character", "Elves_f.png"),
                "text": "Ельф",
            },
            {
                "x": self.window_size[0] / 4.2,
                "y": self.window_size[0] / 4,
                "width": self.window_size[0] / 7,
                "height": self.window_size[0] / 4.5,
                "image_path": os.path.join("Character", "Aasimar_m.png"),
                "image_path_f": os.path.join("Character", "Aasimar_f.png"),
                "text": "Аазімар",
            },
            {
                "x": self.window_size[0] / 1.35,
                "y": self.window_size[0] / 12,
                "width": self.window_size[0] / 11,
                "height": self.window_size[0] / 11,
                "image_path": os.path.join("Character", "exit.png"),
                "image_path_f": os.path.join("Character", "exit.png"),
                "text": "Вихід у головне меню",
            },
        ]

        self.gender_button1 = Button(
            self.window_size[0] / 1.35,
            self.window_size[0] / 5.5,
            self.window_size[0] / 11,
            self.window_size[0] / 11,
            os.path.join("Character", "male", "change.png"),
            "Змінити стать",
        )
        self.gender_button2 = Button(
            self.window_size[0] / 1.35,
            self.window_size[0] / 5.5,
            self.window_size[0] / 11,
            self.window_size[0] / 11,
            os.path.join("Character", "male", "change2.png"),
            "Змінити стать",
        )

        self.buttons_m = [
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
        self.buttons_f = [
            Button(
                data["x"],
                data["y"],
                data["width"],
                data["height"],
                data["image_path_f"],
                data["text"],
            )
            for data in buttons_data
        ]

    def display_menu(self):
        window = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption("Створення Героя")

        change = False
        running = True
        while running:
            window.blit(self.bg_image, (0, 0))
            title_text = self.big_font.render("Обери расу персонажа", True, YELLOW)
            window.blit(title_text, (self.window_size[0] / 4, self.window_size[0] / 11))

            if change:
                gender_button = self.gender_button1
                gender_button.draw(window, self.button_font)
                self.buttons = self.buttons_m
                for button in self.buttons:
                    button.draw(window, self.button_font)
            else:
                gender_button = self.gender_button2
                gender_button.draw(window, self.button_font)
                self.buttons = self.buttons_f
                for button in self.buttons:
                    button.draw(window, self.button_font)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if gender_button.is_clicked(pos):
                        pygame.time.wait(500)
                        if change:
                            change = False
                        else:
                            change = True
                    else:
                        for button in self.buttons:
                            if button.is_clicked(pos):
                                self.handle_button_click(button, change)

        pygame.quit()
        sys.exit()

    def handle_button_click(self, button, change):
        if button == self.buttons[-1]:
            pygame.quit()
            subprocess.run(["python", "main.py"])
        else:
            race_name = button.text
            path_file = os.path.join("Text_patern", "character_info.json")
            with open(path_file, "r", encoding="utf-8") as file:
                data = json.load(file)
                syfix = sufix_images(button.text)
                selected_race = [f"Моя раса - {race_name}", syfix]
                selected_gender = [
                    "Моя стать - " + ("Чоловік" if change else "Жінка"),
                    "_m" if change else "_f",
                ]
                data["race"] = selected_race
                data["gender"] = selected_gender
            with open(path_file, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            pygame.quit()
            subprocess.run(["python", "clas_menu.py"])


if __name__ == "__main__":
    YELLOW = (255, 228, 181)
    pygame.init()
    bg_image = pygame.image.load(os.path.join("Menu_images", "picture_menu.jpg"))
    WINDOW_SIZE = bg_image.get_size()
    character_selector = CharacterSelector(bg_image, WINDOW_SIZE)
    character_selector.display_menu()
