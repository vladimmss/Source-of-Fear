import sys
import os
import pygame
import random
import time
from pygame.locals import *


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


class Main:
    def __init__(self):
        pygame.init()
        self.size = self.width, self.height = 1920, 1080
        self.screen = pygame.display.set_mode((1920, 1080), FULLSCREEN)
        pygame.display.set_caption('Source of Fear')

        pygame.mixer.music.load('data/menu_music.mp3')
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)
        self.stop_thread = False

        self.clock = pygame.time.Clock()

    class Button:
        def __init__(self, x, y, wd, ht, image, text=None, sound=None, extra_im=None):
            self.x, self.y = x, y
            self.width, self.height = wd, ht

            self.image = pygame.transform.scale(load_image(image), (self.width, self.height))
            self.rect = self.image.get_rect(topleft=(x, y))

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
                time.sleep(0.3)
                pygame.event.post(pygame.event.Event(pygame.USEREVENT, button=self))

    def fill_background(self):
        for i in range(3000):
            self.screen.fill(random.choice(((51, 51, 51), (102, 102, 102))),
                             (random.random() * self.width, random.random() * self.height, 7, 2))

    def main_menu(self):
        running = True

        new_game_button = self.Button(self.width // 2 - 900, 500, 300, 100,
                                      'menu_button.png', 'Новая Игра',
                                      'data/menubtn_sound.mp3', 'menu_button_intersected.png')

        continue_menu_button = self.Button(self.width // 2 - 890, 600, 300, 100,
                                           'menu_button.png', 'Продолжить',
                                           'data/menubtn_sound.mp3', 'menu_button_intersected.png')

        settings_menu_button = self.Button(self.width // 2 - 910, 700, 300, 100,
                                           'menu_button.png', 'Настройки',
                                           'data/menubtn_sound.mp3', 'menu_button_intersected.png')

        exit_menu_button = self.Button(self.width // 2 - 965, 800, 300, 100,
                                       'menu_button.png', 'Выход',
                                       'data/menubtn_sound.mp3', 'menu_button_intersected.png')

        buttons = [new_game_button, continue_menu_button, settings_menu_button, exit_menu_button]

        while running:
            if not running:
                break
            self.screen.fill((0, 0, 0))
            image = pygame.transform.scale(load_image('manekens.png'), (1100, 1100))
            rect = image.get_rect(topleft=(700, 0))
            self.screen.blit(image, rect)
            self.fill_background()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.USEREVENT and event.button == new_game_button:
                    self.new_game_menu()

                if event.type == pygame.USEREVENT and event.button == continue_menu_button:
                    pass

                if event.type == pygame.USEREVENT and event.button == settings_menu_button:
                    pass

                if event.type == pygame.USEREVENT and event.button == exit_menu_button:
                    running = False

                for button in buttons:
                    button.button_pressed(event)

            font = pygame.font.Font('data/MorfinSans-Regular.ttf', 150)
            text_rendered = font.render(f'Source', 1, (255, 255, 255))
            text_rect = text_rendered.get_rect(center=(300, 100))
            self.screen.blit(text_rendered, text_rect)

            text_rendered = font.render(f'of', 1, (255, 255, 255))
            text_rect = text_rendered.get_rect(center=(160, 200))
            self.screen.blit(text_rendered, text_rect)

            text_rendered = font.render(f'Fear', 1, (255, 255, 255))
            text_rect = text_rendered.get_rect(center=(210, 300))
            self.screen.blit(text_rendered, text_rect)

            for button in buttons:
                button.draw(self.screen, pygame.mouse.get_pos())

            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()

    def new_game_menu(self):
        import office
        office.Office()

    def continue_game_menu(self):
        pass

    def settings_menu(self):
        pass

    def exit_menu(self):
        pass


if __name__ == '__main__':
    Main().main_menu()
