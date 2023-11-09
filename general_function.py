import pygame
import json

MAX_WIDTH_RASE = 700
MAX_HEIGHT_RASE = 600
MAX_WIDTH_CLAS = 400
MAX_HEIGHT_CLAS = 300


def resize_image(image, max_width, max_height):
    width, height = image.get_width(), image.get_height()
    aspect_ratio = width / height
    
    if width > max_width or height > max_height:
        new_width = min(width, max_width)
        new_height = int(new_width / aspect_ratio)
        if new_height > max_height:
            new_height = max_height
            new_width = int(new_height * aspect_ratio)
        return pygame.transform.scale(image, (new_width, new_height))
    else:
        return image


def read_character_info():
    file_path = "Text_patern\\character_info.json"
    race_name = ""
    clas_name = ""
    with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

    name = data.get('name', '')
    race_name = data.get('race', '')
    clas_name = data.get('class', '')
    addition = data.get('gender', '')
    first_file_path = data.get('first_file_path', '')
    file_path_item = data.get('file_path_item', '')
    return race_name, clas_name, addition, name, first_file_path, file_path_item


def load_images():
    
    race_name, clas_name, addition, _, _, _ = read_character_info()

    race = race_name[0].replace("Моя раса - ", "").strip()
    race_images = {
        "Ельф": f"Character\\Elves{addition[1]}.png",
        "Людина": f"Character\\Human{addition[1]}.png",
        "Тифлінг": f"Character\\Tieflings{addition[1]}.png",
        "Орк": f"Character\\Ork{addition[1]}.png",
        "Гном": f"Character\\Gnomes{addition[1]}.png",
        "Аазімар": f"Character\\Aasimar{addition[1]}.png"
    }
    
    clas = clas_name[0].replace("Мій клас - ", "").strip()
    clas_images = {
        "Бард": "Character\\Bard.png",
        "Чарівник": "Character\\Wizard.png",
        "Воїн": "Character\\Fighter.png",
        "Клірик": "Character\\Cleric.png"
    }
    
    image_race = pygame.image.load(race_images.get(race, "Character\\Human_f.png"))
    image_clas = pygame.image.load(clas_images.get(clas, "Character\\Fighter.png"))
    image_cooming_soon =pygame.image.load("Menu_images\\coming_soon.png")
    
    image_race = resize_image(image_race, MAX_WIDTH_RASE, MAX_HEIGHT_RASE)
    image_clas = resize_image(image_clas, MAX_WIDTH_CLAS, MAX_HEIGHT_CLAS)
    image_cooming_soon =resize_image(image_cooming_soon, MAX_WIDTH_CLAS, MAX_HEIGHT_CLAS)

    return image_race, image_clas, image_cooming_soon


def select_font():
    button_font_path = "Font\\quest.ttf"
    button_font_size = 30
    button_font = pygame.font.Font(button_font_path, button_font_size)

    menu_font_path = "Font\\old.ttf"
    menu_font_size = 25
    menu_font = pygame.font.Font(menu_font_path, menu_font_size)

    big_font_path = "Font\\western.ttf"
    big_font_size = 80
    big_font = pygame.font.Font(big_font_path, big_font_size)

    return button_font, menu_font, big_font 

def sufix_images(name):
    suffixes = {
        "Людина": "_h",
        "Тифлінг": "_t",
        "Орк": "_o",
        "Гном": "_g",
        "Ельф": "_e",
        "Аазімар": "_a",
        "Бард": "_b",
        "Клірик": "_k",
        "Воїн": "_f",
        "Чарівник": "_w"
    }

    return suffixes.get(name, "")