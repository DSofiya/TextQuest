import pygame
import sys
import subprocess
import random
import json

from general_function import select_font, read_character_info


YELLOW = (255, 228, 181)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class Button:
    def __init__(self, x, y, width, height, image_path, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.button_font, self.menu_font, self.big_font = select_font()
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.text = text

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

class CharacterSelector:
    def __init__(self, bg_image, window_size):
        self.bg_image = bg_image
        self.window_size = window_size
        self.button_font, _, self.big_font = select_font()
        self.load_buttons()
        self.user_name = ""


    def load_buttons(self):
        buttons_data = [
            {"x": self.window_size[0] / 1.4, "y":self.window_size[0] / 9.8, "width": self.window_size[0]/ 7, "height": self.window_size[0] / 8,
            "image_path": "Character\\exit.png", "text": "Вихід у головне меню"},

            {"x": self.window_size[0] / 2.5, "y": self.window_size[0] / 3.5, "width": self.window_size[0]/ 5.5, "height": self.window_size[0] / 8,
            "image_path": "Menu_images\\button.png", "text": "Записати" },
            
            {"x": self.window_size[0] / 6, "y": self.window_size[0] / 4.2, "width": self.window_size[0]/ 5, "height": self.window_size[0] / 5,
            "image_path": "Character\\random\\random1.png", "text": "Рандомний вибір імені"}]


        self.buttons = [Button(data["x"], data["y"], data["width"], data["height"], data["image_path"], data["text"]) for data in buttons_data]

        self.button_random_images = [
            pygame.image.load("Character\\random\\random1.png"),
            pygame.image.load("Character\\random\\random2.png"),
            pygame.image.load("Character\\random\\random3.png")]

        current_image_index = 0 
        self.button_random_rect = self.button_random_images[current_image_index].get_rect()
        self.button_random_rect.x , self.button_random_rect.y= self.window_size[0] / 6.5 , self.window_size[0] / 4.2 


    def display_menu(self):
        input_rect = pygame.Rect(self.window_size[0] / 2.5, self.window_size[0] / 4.2, self.window_size[0] / 5, self.window_size[0] / 20)
        window = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption("Створення імені героя")
        _, _, addition, _, _, _ = read_character_info()
        character_created_message = "Персонаж створений успішно"
        current_image_index = 0
        last_image_change_time = pygame.time.get_ticks()
        n = 0
        choose_name_random = False
        running = True

        while running:
            window.blit(bg_image, (0, 0))
            pygame.draw.rect(window, BLACK, input_rect)
            pygame.draw.rect(window, YELLOW, input_rect, 2)

            title_text = self.big_font.render("Введіть ім'я персонажа", True, YELLOW)
            window.blit(title_text, (WINDOW_SIZE[0] / 3.2, WINDOW_SIZE[0] / 6))

            text_surface = self.button_font.render(self.user_name, True, YELLOW)
            text_rect = text_surface.get_rect(center=input_rect.center)
            window.blit(text_surface, text_rect.topleft)

            self.buttons[0].draw(window, True, self.button_font)
            self.buttons[1].draw(window, False, self.button_font)

            current_time = pygame.time.get_ticks()
            if current_time - last_image_change_time > 400:
                current_image_index = (current_image_index + 1) % len(self.button_random_images)
                last_image_change_time = current_time
                n += 1
                if n == 4:
                    choose_name_random = False
                    n = 0

            if choose_name_random:
                window.blit(self.button_random_images[current_image_index], self.button_random_rect)
            else:
                self.buttons[2].draw(window, True, self.button_font)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.user_name = self.user_name[:-1]
                    elif event.unicode.isprintable():
                        self.user_name += event.unicode
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    for button in self.buttons:
                        if button.is_clicked(pos):
                            if button == self.buttons[0]:
                                pygame.quit()
                                subprocess.run(["python", "main.py"])
                            elif button == self.buttons[2]:
                                choose_name_random = True
                                random_name_file = f"Text_patern\\random_name{addition[1]}.txt"
                                self.user_name = self.get_random_name(random_name_file)

                            elif button == self.buttons[1]:
                                self.handle_character_creation_success(window, character_created_message)

        pygame.quit()
        sys.exit()


    def get_random_name(self, file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
            random_line = random.choice(lines)
            return random_line.strip()


    def handle_character_creation_success(self, window, character_created_message):
        path_file = "Text_patern\\character_info.json"
        with open(path_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
            selected_name = f"Моє ім'я - {self.user_name}"
            data["name"] = selected_name

        with open(path_file, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        text_surface = self.button_font.render(character_created_message, True, YELLOW)
        text_rect = text_surface.get_rect(center=(WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2))
        window.blit(text_surface, text_rect.topleft)
        pygame.display.flip()
        pygame.time.wait(1000)
        pygame.quit()
        subprocess.run(["python", "main.py"])


if __name__ == "__main__":
    pygame.init()
    bg_image = pygame.image.load("Menu_images\\picture_menu.jpg")
    WINDOW_SIZE = bg_image.get_size()
    character_selector = CharacterSelector(bg_image, WINDOW_SIZE)
    character_selector.display_menu()