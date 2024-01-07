import pygame
import sys
import os
import random
# import sqlite3
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

    def ins_draw(self):
        pass

    def button_pressed(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.intersection:
            self.sound.play()
            # time.sleep(0.3)
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, button=self))


class Office:
    def __init__(self):
        pygame.init()
        self.size = self.width, self.height = 1920, 1080
        self.screen = pygame.display.set_mode((1920, 1080), FULLSCREEN)
        pygame.mixer.music.load('data/vent.mp3')
        pygame.mixer.music.set_volume(0.8)
        pygame.mixer.music.play(-1)
        self.clock = pygame.time.Clock()
        self.hours = ['12', '1', '2', '3', '4', '5']

    def fill_camera(self):
        for i in range(3000):
            self.screen.fill(random.choice(((128, 128, 128), (102, 102, 102))),
                             (1250, 695, 205, 163))

    def main_office(self):
        mainloop = True
        print_message = pygame.USEREVENT + 0
        pygame.time.set_timer(print_message, 30000)
        new_game_button = Button((820, 370), (300, 100),
                                 'menu_button.png', 'Светить',
                                 'data/menubtn_sound.mp3', 'menu_button_intersected.png')
        buttons = [new_game_button]
        while mainloop:
            bg = load_image('base_office.jpg').convert()
            bg = pygame.transform.scale(bg, (1920, 1080))
            for event in pygame.event.get():
                self.screen.blit(bg, (0, 0))
                if event.type == print_message:
                    if len(self.hours) > 1:
                        del self.hours[0]
                    else:
                        mainloop = False
                if event.type == pygame.QUIT:
                    mainloop = False
                self.time()
            for button in buttons:
                button.draw(self.screen, pygame.mouse.get_pos())
            self.fill_camera()
            self.clock.tick(20)
            pygame.display.flip()
        pygame.quit()

    def time(self):
        font = pygame.font.Font('data/MorfinSans-Regular.ttf', 55)
        text_rendered = font.render(f'{self.hours[0]} AM', 1, (255, 255, 255))
        text_rect = text_rendered.get_rect(center=(1850, 50))
        self.screen.blit(text_rendered, text_rect)
        font = pygame.font.Font('data/MorfinSans-Regular.ttf', 45)
        text_rendered = font.render(f'Night 1', 1, (255, 0, 0))
        text_rect = text_rendered.get_rect(center=(1850, 100))
        self.screen.blit(text_rendered, text_rect)


if __name__ == '__main__':
    Office()
