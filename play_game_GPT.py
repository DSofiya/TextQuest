import pygame
import openai
import os
import subprocess
import json

from general_function import (
    load_images,
    select_font,
    read_character_info,
    resource_path,
)


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 228, 181)
RED = (139, 0, 0)


def initialize_game():
    pygame.init()
    bg_image = pygame.image.load(resource_path(os.path.join("Menu_images", "picture_menu.jpg")))
    WINDOW_SIZE = bg_image.get_size()
    window = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Гра")
    clock = pygame.time.Clock()
    user_input = ""
    chat_response = ""
    return chat_response, user_input, bg_image, WINDOW_SIZE, window, clock


def key_verification():
    api_key = ""
    with open(
        resource_path(os.path.join("Text_patern", "api_key.txt")), "r", encoding="utf-8"
    ) as file:
        lines = file.readlines()
        found = False
        for i, line in enumerate(lines):
            if "АПІ" in line:
                found = True
                api_key = line.strip("АПІ - ")

    openai.api_key = api_key

    if not found:
        print_exept_openai = True
    else:
        print_exept_openai = False

    return openai.api_key, print_exept_openai


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


def load_buttons(WINDOW_SIZE):
    buttons_data = [
        {
            "x": WINDOW_SIZE[0] / 1.43,
            "y": WINDOW_SIZE[1] / 6.6,
            "width": WINDOW_SIZE[0] / 20,
            "height": WINDOW_SIZE[0] / 20,
            "image_path": resource_path(os.path.join("Menu_images", "arroy2_up.png")),
            "text": "",
        },
        {
            "x": WINDOW_SIZE[0] / 1.43,
            "y": WINDOW_SIZE[1] / 3,
            "width": WINDOW_SIZE[0] / 20,
            "height": WINDOW_SIZE[0] / 20,
            "image_path": resource_path(os.path.join("Menu_images", "arroy2_down.png")),
            "text": "",
        },
        {
            "x": WINDOW_SIZE[0] / 1.30,
            "y": WINDOW_SIZE[1] / 8,
            "width": WINDOW_SIZE[0] / 11,
            "height": WINDOW_SIZE[1] / 5.5,
            "image_path": resource_path(os.path.join("Character", "exit.png")),
            "text": "Вихід до головного меню ",
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


def image(path_image, size):
    image = pygame.image.load(path_image)
    image = pygame.transform.scale(image, size)

    return image


def grate_into_rows(scrolling_text, menu_font, WINDOW_SIZE):
    lines = []
    words = scrolling_text.split(" ")
    current_line = ""
    for word in words:
        word.replace("\n", " ")
        test_line = current_line + word + " "
        test_size = menu_font.size(test_line)
        if test_size[0] < WINDOW_SIZE[0] / 2 - 200:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + " "
    lines.append(current_line)

    return lines


def find_text(prompt_key):
    with open(
        resource_path(os.path.join("Text_patern", "Rosefild.json"), "r", encoding="utf-8")
    ) as file:
        text_list = json.load(file)
        text = text_list.get(prompt_key)
        return text


def get_prompt_text(user_input, prompt_text):
    race_name, _, _, name, _, _ = read_character_info()

    if prompt_text == "":
        list = [
            "хазяїн",
            "лікар",
            "доктор",
            "розкажи",
            "поговори",
            "підійти",
            "настоят",
            "храм",
            "магаз",
            "алхімік",
            "власник",
            "зіл",
            "заклин",
            "невидимост",
            "світіння",
            "катакомб",
            "ввійти",
            "війти",
            "зайти",
            "повернутись",
            "далі",
            "так",
            "є",
            "карт",
            "закляття",
            "стати",
            "напаст",
            "підійти",
            "убити",
            "наступного",
            "втікти",
            "подарувати",
            "продати",
            "вкрасти",
            "розбити",
            "битись",
            "прислужн",
            "else",
        ]
        for else_line in list:
            if else_line in user_input:
                text = find_text(else_line)
                break
            else:
                text = find_text("else")
    else:
        text = find_text(prompt_text)
    text = f"({name},{race_name[0]}) {text} "
    return text


def get_ansver_GPT(user_input, prompt_text):
    print_exept_openai = False
    response = None
    prompt_text = get_prompt_text(user_input, prompt_text)

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"User: {user_input}+{prompt_text}\nChatGPT:",
            max_tokens=618,
        )
    except openai.error.AuthenticationError:
        print_exept_openai = True
    return print_exept_openai, response


def refresh_window(buttons, button_font, WINDOW_SIZE, window, bg_image):
    image_fon = image(
        resource_path(os.path.join("Menu_images", "book.png")),
        (WINDOW_SIZE[0] / 2, WINDOW_SIZE[0] / 2.5),
    )
    image_ansver = image(
        resource_path(os.path.join("Menu_images", "ansver.png")),
        (WINDOW_SIZE[0] / 1.6, WINDOW_SIZE[0] / 12),
    )
    image_race, image_class = load_images()

    window.blit(bg_image, (0, 0))
    window.blit(image_fon, (WINDOW_SIZE[0] / 4, WINDOW_SIZE[1] / 7))
    window.blit(image_race, (WINDOW_SIZE[0] / 10, WINDOW_SIZE[1] / 4))
    window.blit(image_class, (WINDOW_SIZE[0] / 1.35, WINDOW_SIZE[1] / 2.5))
    window.blit(image_ansver, (WINDOW_SIZE[0] / 4.52, WINDOW_SIZE[1] / 1.5))
    for button in buttons:
        button.draw(window, button_font)


def render_chat_response(chat_response, menu_font, scroll_y, window, WINDOW_SIZE):
    y_position = WINDOW_SIZE[1] // 5
    displayed_lines = chat_response
    for line in displayed_lines:
        chatgpt_surface = menu_font.render(line, True, (0, 0, 0))
        if (
            y_position + scroll_y >= WINDOW_SIZE[1] // 5
            and y_position + scroll_y <= WINDOW_SIZE[1] // 1.6
        ):
            window.blit(chatgpt_surface, (WINDOW_SIZE[1] // 2, y_position + scroll_y))
        y_position += menu_font.get_linesize()


def main():
    chat_response, user_input, bg_image, WINDOW_SIZE, window, clock = initialize_game()
    scroll_y, char_index, time_passed = 0, 0, 0
    button_font, menu_font, big_font = select_font()
    openai.api_key, print_exept_openai = key_verification()

    buttons = load_buttons(WINDOW_SIZE)
    refresh_window(buttons, button_font, WINDOW_SIZE, window, bg_image)
    text = "Ви потрапляєте в місто Роузфілд. На центральній площі міста\
    ви бачите величезний храм 'Пророчих Світів', зліва сховався \
    магазин місцевого алхіміка де можна знайти зілля, магічні \
    склянки та загадкові рецепти. Праворуч від храму, ви помічаєте таверну і прямуєте до неї."
    chat_response = grate_into_rows(text, menu_font, WINDOW_SIZE)
    render_chat_response(chat_response, menu_font, scroll_y, window, WINDOW_SIZE)
    pygame.display.flip()

    print_exept_openai, response = get_ansver_GPT(user_input, "first_prompt")
    if response is not None:
        chat_response = grate_into_rows(
            response.choices[0].text.strip(), menu_font, WINDOW_SIZE
        )

    running = True
    while running:
        refresh_window(buttons, button_font, WINDOW_SIZE, window, bg_image)
        user_surface = menu_font.render("Пригодник: " + user_input, True, WHITE)
        window.blit(user_surface, (WINDOW_SIZE[0] / 3.8, WINDOW_SIZE[1] / 1.4))

        if print_exept_openai:
            title_text = big_font.render(
                f"Ключ не активований, або записаний неправильно!", True, RED
            )
            window.blit(title_text, (WINDOW_SIZE[0] / 8, WINDOW_SIZE[0] / 4))

        time_delta = clock.tick(30)
        time_passed += time_delta
        if time_passed > 1000 and char_index < len(chat_response):
            char_index += 1
            time_passed = 0

        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] and scroll_y < 0:
            scroll_y += 3
        if keys[pygame.K_DOWN] and scroll_y > -(
            len(chat_response) * menu_font.get_linesize() - WINDOW_SIZE[1] // 5
        ):
            scroll_y -= 3

        render_chat_response(chat_response, menu_font, scroll_y, window, WINDOW_SIZE)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    print_exept_openai, response = get_ansver_GPT(user_input, "")
                    chat_response = grate_into_rows(
                        response.choices[0].text.strip(), menu_font, WINDOW_SIZE
                    )
                    user_input = ""
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                else:
                    user_input += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                for button in buttons:
                    if button.is_clicked(pos):
                        if button == buttons[-1]:
                            pygame.quit()
                            subprocess.run(["python", resource_path("main.py")])
                        elif button == buttons[0] and scroll_y < 0:
                            scroll_y += 20
                        elif button == buttons[1] and scroll_y > -(
                            len(chat_response) * menu_font.get_linesize()
                            - WINDOW_SIZE[1] // 5
                        ):
                            scroll_y -= 20

    pygame.quit()


if __name__ == "__main__":
    main()
