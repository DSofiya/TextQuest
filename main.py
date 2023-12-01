import pygame
import sys
import os
import subprocess
from general_function import load_images, select_font, resource_path

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class GameInitializer:
    @staticmethod
    def initialize_game():
        pygame.init()
        image_path = resource_path(os.path.join("Menu_images", "picture_character.jpg"))
        bg_image = pygame.image.load(image_path)
        WINDOW_SIZE = bg_image.get_size()
        window = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption("DnD Game Menu")
        return window, WINDOW_SIZE, bg_image


class Button:
    def __init__(self, x, y, width, height, image_path, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.text = text

    def draw(self, surface, font):
        surface.blit(self.image, self.rect.topleft)
        text_surface = font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


class ButtonManager:
    @staticmethod
    def load_buttons(WINDOW_SIZE):
        buttons_data = [
            {
                "x": WINDOW_SIZE[0] / 2.5,
                "y": WINDOW_SIZE[0] / 4,
                "width": WINDOW_SIZE[0] / 5,
                "height": WINDOW_SIZE[1] / 8,
                "image_path": resource_path(os.path.join("Menu_images", "button.png")),
                "text": "Створити героя",
            },
            {
                "x": WINDOW_SIZE[0] / 2.5,
                "y": WINDOW_SIZE[0] / 3.2,
                "width": WINDOW_SIZE[0] / 5,
                "height": WINDOW_SIZE[1] / 8,
                "image_path": resource_path(os.path.join("Menu_images", "button.png")),
                "text": "Обрати пригоду",
            },
            {
                "x": WINDOW_SIZE[0] / 2.5,
                "y": WINDOW_SIZE[0] / 2.6,
                "width": WINDOW_SIZE[0] / 5,
                "height": WINDOW_SIZE[1] / 8,
                "image_path": resource_path(os.path.join("Menu_images", "button.png")),
                "text": "Вихід",
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


class MenuRenderer:
    @staticmethod
    def render_menu(window, bg_image, buttons, fon_font, big_font, WINDOW_SIZE):
        window.blit(bg_image, (0, 0))
        for button in buttons:
            button.draw(window, fon_font)
        title_text = big_font.render("Меню гри ", True, BLACK)
        image_race, image_clas = load_images()

        window.blit(title_text, (WINDOW_SIZE[0] / 2.5, WINDOW_SIZE[0] / 5.5))
        window.blit(image_race, (WINDOW_SIZE[0] / 7, WINDOW_SIZE[1] / 4))
        window.blit(image_clas, (WINDOW_SIZE[0] / 1.6, WINDOW_SIZE[1] / 2.5))
        pygame.display.flip()


class MenuEventHandler:
    @staticmethod
    def handle_events(buttons):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                for button in buttons:
                    if button.is_clicked(pos):
                        MenuEventHandler.handle_button_click(button)

    @staticmethod
    def handle_button_click(button):
        if button.text == "Створити героя":
            pygame.quit()
            subprocess.run(["python", resource_path("character_creation_menu.py")])
        elif button.text == "Обрати пригоду":
            pygame.quit()
            subprocess.run(["python", resource_path("adventure_menu.py")])
        elif button.text == "Вихід":
            pygame.quit()
            sys.exit()


def main():
    window, WINDOW_SIZE, bg_image = GameInitializer.initialize_game()
    fon_font, _, big_font = select_font()
    buttons = ButtonManager.load_buttons(WINDOW_SIZE)
    run = True

    while run:
        MenuRenderer.render_menu(
            window, bg_image, buttons, fon_font, big_font, WINDOW_SIZE
        )
        MenuEventHandler.handle_events(buttons)
        if window._pixels_address == None:
            run = False
            break


if __name__ == "__main__":
    main()
