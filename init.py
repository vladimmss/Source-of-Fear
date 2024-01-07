import sys
import os
import pygame
import random
import office
import time
# from pygame.locals import *


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f'Файл с изображением {fullname} не найден')
        sys.exit()
    img = pygame.image.load(fullname)
    if colorkey is not None:
        img = img.convert()
        if colorkey == -1:
            colorkey = img.get_at((0, 0))
        img.set_colorkey(colorkey)
    else:
        img = img.convert_alpha()
    return img


class Button:
    def __init__(self, pos: tuple, size: tuple, image=None, text=None, sound=None, extra_im=None):
        self.x, self.y = pos
        self.width, self.height = size

        if image:
            self.image = pygame.transform.scale(load_image(image), (self.width, self.height))
            self.rect = self.image.get_rect(topleft=pos)

        if text:
            self.text = text
        if sound:
            self.sound = pygame.mixer.Sound(sound)
            self.sound.set_volume(0.3)
        if extra_im:
            self.extra_im = pygame.transform.scale(load_image(image), (self.width, self.height))

        self.intersection = False

    def draw(self, sc, mouse_pos):
        font = pygame.font.Font('data/MorfinSans-Regular.ttf', 70)
        text_rendered = font.render(self.text, 1, (255, 255, 255))
        text_rect = text_rendered.get_rect(center=self.rect.center)
        sc.blit(text_rendered, text_rect)

        self.intersection = self.rect.collidepoint(mouse_pos)

    def button_pressed(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.intersection:
            self.sound.play()
            # time.sleep(0.3)
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, button=self))


class MainMenu:
    def __init__(self):
        pygame.init()
        self.size = self.width, self.height = 1920, 1080
        self.screen = pygame.display.set_mode(self.size, pygame.FULLSCREEN)
        pygame.display.set_caption('Source of Fear')

        pygame.mixer.music.load('data/menu_music.mp3')
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)

        self.clock = pygame.time.Clock()

    def fill_background(self):
        for i in range(3000):
            self.screen.fill(random.choice(((51, 51, 51), (102, 102, 102))),
                             (random.random() * self.width, random.random() * self.height, 7, 2))

    def main_window(self):
        running = True

        new_game_button = Button((self.width // 2 - 830, 370), (300, 100),
                                 'menu_button.png', 'Новая Игра',
                                 'data/menubtn_sound.mp3', 'menu_button_intersected.png')
        continue_menu_button = Button((self.width // 2 - 820, 450), (300, 100),
                                      'menu_button.png', 'Продолжить',
                                      'data/menubtn_sound.mp3', 'menu_button_intersected.png')
        settings_menu_button = Button((self.width // 2 - 840, 530), (300, 100),
                                      'menu_button.png', 'Настройки',
                                      'data/menubtn_sound.mp3', 'menu_button_intersected.png')
        exit_menu_button = Button((self.width // 2 - 895, 610), (300, 100),
                                  'menu_button.png', 'Выход',
                                  'data/menubtn_sound.mp3', 'menu_button_intersected.png')

        buttons = [new_game_button, continue_menu_button, settings_menu_button, exit_menu_button]

        while running:
            self.screen.fill((0, 0, 0))
            image = pygame.transform.scale(load_image('manekens.png'), (1000, 1000))
            rect = image.get_rect(topleft=(470, 0))
            self.screen.blit(image, rect)
            self.fill_background()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.USEREVENT and event.button == new_game_button:
                    self.size = self.width, self.height = 1920, 1080
                    self.screen = pygame.display.set_mode(self.size, pygame.FULLSCREEN)
                    pygame.mixer.music.load('data/start.mp3')
                    pygame.mixer.music.set_volume(0.3)
                    pygame.mixer.music.play(-1)
                    time.sleep(1)

                    # тут надо доделать
                    new_game_menu()

                if event.type == pygame.USEREVENT and event.button == continue_menu_button:
                    pass

                if event.type == pygame.USEREVENT and event.button == settings_menu_button:
                    self.settings_menu()

                if event.type == pygame.USEREVENT and event.button == exit_menu_button:
                    running = False

                for button in buttons:
                    button.button_pressed(event)

            font = pygame.font.Font('data/MorfinSans-Regular.ttf', 150)
            text_rendered = font.render('Source', 1, (255, 0, 0))
            text_rect = text_rendered.get_rect(center=(300, 100))
            self.screen.blit(text_rendered, text_rect)

            text_rendered = font.render('of', 1, (255, 0, 0))
            text_rect = text_rendered.get_rect(center=(160, 200))
            self.screen.blit(text_rendered, text_rect)

            text_rendered = font.render('Fear', 1, (255, 0, 0))
            text_rect = text_rendered.get_rect(center=(210, 300))
            self.screen.blit(text_rendered, text_rect)

            for button in buttons:
                button.draw(self.screen, pygame.mouse.get_pos())

            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()

    def settings_menu(self):
        running = True

        back_button = Button((self.width // 2 - 150, 600), (300, 100),
                             'menu_button.png', 'Назад',
                             'data/menubtn_sound.mp3', 'menu_button_intersected.png')

        buttons = [back_button]

        while running:
            self.screen.fill((0, 0, 0))
            self.fill_background()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if ((event.type == pygame.USEREVENT and event.button == back_button) or
                        (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)):
                    self.main_window()

                for button in buttons:
                    button.button_pressed(event)

            font1 = pygame.font.Font('data/MorfinSans-Regular.ttf', 150)
            text_rendered = font1.render('Настройки', 1, (255, 0, 0))
            text_rect = text_rendered.get_rect(center=((self.width // 2 - text_rendered.get_width() // 2), 90))
            self.screen.blit(text_rendered, text_rect)

            font2 = pygame.font.Font('data/MorfinSans-Regular.ttf', 60)
            text_rendered = font2.render('Громкость', 1, (255, 255, 255))
            text_rect = text_rendered.get_rect(center=((self.width // 6), 270))
            self.screen.blit(text_rendered, text_rect)

            text_rendered = font2.render('Яркость', 1, (255, 255, 255))
            text_rect = text_rendered.get_rect(center=((self.width // 6), 390))
            self.screen.blit(text_rendered, text_rect)

            text_rendered = font2.render('Музыка', 1, (255, 255, 255))
            text_rect = text_rendered.get_rect(center=((self.width // 6), 510))
            self.screen.blit(text_rendered, text_rect)

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()[0]

            for button in buttons:
                button.draw(self.screen, mouse_pos)

            sliders = [Slider((720, 265), (450, 35), 0.3, 0, 100),
                       Slider((720, 385), (450, 35), 0.7, 0, 10)]

            for slider in sliders:
                if slider.slider_rect.collidepoint(mouse_pos) and mouse_pressed:
                    slider.move(mouse_pos)
                slider.render(self.screen)

            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()


def new_game_menu():
    office.Office().main_office()


def continue_game_menu():
    pass


def exit_menu():
    pass


class Slider:
    def __init__(self, pos: tuple, size: tuple, start_value: float, min_value: int, max_value: int):
        self.pos = pos
        self.size = size

        self.slider_left = self.pos[0] - size[0] // 2
        self.slider_right = self.pos[0] + size[0] // 2
        self.slider_top = self.pos[1] - size[1] // 2

        self.min = min_value
        self.max = max_value

        self.start_value = (self.slider_right - self.slider_left) * start_value

        self.slider_rect = pygame.Rect(self.slider_left, self.slider_top, self.size[0], self.size[1])
        self.button_rect = pygame.Rect(self.slider_left + self.start_value, self.slider_top + 5, 10, self.size[1] - 10)

    def render(self, sc):
        pygame.draw.rect(sc, pygame.Color('white'), self.slider_rect, width=5)
        pygame.draw.rect(sc, pygame.Color('red'), self.button_rect)

    def move(self, mouse_pos):
        self.button_rect.centerx = mouse_pos[0]

    def get_value(self):
        value_range = self.slider_right - self.slider_left - 1
        button_value = self.button_rect.centerx - self.slider_left

        return (button_value / value_range) * (self.max - self.min) + self.min


if __name__ == '__main__':
    MainMenu().main_window()
