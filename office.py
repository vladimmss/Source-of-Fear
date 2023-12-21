import pygame
import sys
import os
import datetime
from pygame.locals import *


class Office:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1920, 1080), FULLSCREEN)
        pygame.mixer.music.load('data/vent.mp3')
        pygame.mixer.music.set_volume(0.8)
        pygame.mixer.music.play(-1)
        mainLoop = True
        while mainLoop:
            bg = self.load_image('office.png').convert()
            bg = pygame.transform.scale(bg, (1920, 1080))
            for event in pygame.event.get():
                self.screen.blit(bg, (0, 0))
                if event.type == pygame.QUIT:
                    mainLoop = False
                self.time()
            pygame.display.update()

    def load_image(self, name, colorkey=None):
        fullname = os.path.join('data', name)
        if not os.path.isfile(fullname):
            print(f"Файл с изображением '{fullname}' не найден")
            sys.exit()
        image = pygame.image.load(fullname)
        if colorkey is not None:
            image = image.convert()
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
        else:
            image = image.convert_alpha()
        return image

    def time(self):
        font = pygame.font.Font('data/plasma-drip-brk.ttf', 85)
        text_rendered = font.render('Source of Fear', 1, (110, 200, 110))
        text_rect = text_rendered.get_rect(center=(350, 100))
        self.screen.blit(text_rendered, text_rect)

    pygame.quit()


if __name__ == '__main__':
    Office()
