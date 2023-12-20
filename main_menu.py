import sys
import os
import pygame
import random


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
            self.extra_im = pygame.transform.scale(load_image(extra_im), (self.width, self.height))
        self.intersection = False

    def draw(self, sc, mouse_pos):
        button_image = self.extra_im if self.intersection else self.image
        sc.blit(button_image, self.rect)

        font = pygame.font.Font(None, 40)
        text_rendered = font.render(self.text, 1, (200, 200, 200))
        text_rect = text_rendered.get_rect(center=self.rect.center)
        sc.blit(text_rendered, text_rect)

        self.intersection = self.rect.collidepoint(mouse_pos)

    def button_pressed(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.intersection:
            self.sound.play()
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, button=self))


pygame.init()
size = width, height = 700, 500
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Source of Fear')

pygame.mixer.music.load('data/menu_music.mp3')
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

clock = pygame.time.Clock()


def fill_background():
    for i in range(3000):
        screen.fill(random.choice(((51, 51, 51), (102, 102, 102))),
                    (random.random() * width, random.random() * height, 7, 2))


def main_menu():
    running = True

    new_game_button = Button(width // 2 - 300, 200, 300, 100,
                             'menu_button.png', 'Новая Игра',
                             'data/menubtn_sound.mp3', 'menu_button_intersected.png')

    continue_menu_button = Button(width // 2, 200, 300, 100,
                                  'menu_button.png', 'Продолжить',
                                  'data/menubtn_sound.mp3', 'menu_button_intersected.png')

    settings_menu_button = Button(width // 2 - 150, 300, 300, 100,
                                  'menu_button.png', 'Настройки',
                                  'data/menubtn_sound.mp3', 'menu_button_intersected.png')

    exit_menu_button = Button(width // 2 - 150, 400, 300, 100,
                              'menu_button.png', 'Выход',
                              'data/menubtn_sound.mp3', 'menu_button_intersected.png')

    buttons = [new_game_button, continue_menu_button, settings_menu_button, exit_menu_button]

    while running:
        screen.fill((0, 0, 0))
        fill_background()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.USEREVENT and event.button == new_game_button:
                pass

            if event.type == pygame.USEREVENT and event.button == continue_menu_button:
                pass

            if event.type == pygame.USEREVENT and event.button == settings_menu_button:
                pass

            if event.type == pygame.USEREVENT and event.button == exit_menu_button:
                running = False

            for button in buttons:
                button.button_pressed(event)

        font = pygame.font.Font('data/plasma-drip-brk.ttf', 85)
        text_rendered = font.render('Source of Fear', 1, (110, 200, 110))
        text_rect = text_rendered.get_rect(center=(350, 100))
        screen.blit(text_rendered, text_rect)

        for button in buttons:
            button.draw(screen, pygame.mouse.get_pos())

        pygame.display.flip()
        clock.tick(60)
    pygame.quit()


def new_game_menu():
    pass


def continue_game_menu():
    pass


def settings_menu():
    pass


def exit_menu():
    pass


if __name__ == '__main__':
    main_menu()
