import sys
import os
import pygame
import random
import wx


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
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, button=self))


class MainMenu:
    def __init__(self):
        pygame.init()
        app = wx.App(False)
        self.size = self.width, self.height = wx.GetDisplaySize()
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

        new_game_button = Button((self.width // 2 - 870, 570), (300, 100),
                                 'menu_button.png', 'Новая Игра',
                                 'data/menubtn_sound.mp3', 'menu_button_intersected.png')
        continue_menu_button = Button((self.width // 2 - 857, 650), (300, 100),
                                      'menu_button.png', 'Продолжить',
                                      'data/menubtn_sound.mp3', 'menu_button_intersected.png')
        settings_menu_button = Button((self.width // 2 - 880, 730), (300, 100),
                                      'menu_button.png', 'Настройки',
                                      'data/menubtn_sound.mp3', 'menu_button_intersected.png')
        exit_menu_button = Button((self.width // 2 - 935, 810), (300, 100),
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
                    new_game_menu()

                if event.type == pygame.USEREVENT and event.button == continue_menu_button:
                    pass

                if event.type == pygame.USEREVENT and event.button == settings_menu_button:
                    self.settings_menu()

                if event.type == pygame.USEREVENT and event.button == exit_menu_button:
                    running = False

                for button in buttons:
                    button.button_pressed(event)

            font = pygame.font.Font('data/MorfinSans-Regular.ttf', 160)
            text_rendered = font.render('Source', 1, (255, 0, 0))
            text_rect = text_rendered.get_rect(center=(300, 200))
            self.screen.blit(text_rendered, text_rect)

            text_rendered = font.render('of', 1, (255, 0, 0))
            text_rect = text_rendered.get_rect(center=(160, 300))
            self.screen.blit(text_rendered, text_rect)

            text_rendered = font.render('Fear', 1, (255, 0, 0))
            text_rect = text_rendered.get_rect(center=(210, 400))
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
    Office().default_office()


def continue_game_menu():
    pass


def exit_menu():
    pass


class Office:
    def __init__(self):

        pygame.init()
        app = wx.App(False)
        self.size = self.width, self.height = wx.GetDisplaySize()
        self.screen = pygame.display.set_mode(self.size, pygame.FULLSCREEN)
        pygame.display.set_caption('Source of Fear')

        pygame.mixer.music.load('data/vent.mp3')
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)

        self.clock = pygame.time.Clock()
        self.hours = ['12', '1', '2', '3', '4', '5']
        self.energy = 100
        self.change_energy_point = 0
        self.energy_change_time = 5000
        self.condition = 0

        self.change_hour = pygame.USEREVENT + 0
        pygame.time.set_timer(self.change_hour, 50000)
        self.change_energy = pygame.USEREVENT + 1
        pygame.time.set_timer(self.change_energy, self.energy_change_time)

        self.open_camera_sound = pygame.mixer.Sound('data/change_camera.mp3')
        self.open_camera_sound.set_volume(0.3)
        self.is_door_locked = False

    def fill_tv(self):
        pygame.draw.rect(self.screen, (70, 70, 70),
                         (self.width * 0.6531, self.height * 0.6463, self.width * 0.1026, self.height * 0.1463))
        for i in range(1500):
            pygame.draw.rect(self.screen, random.choice(((34, 34, 34), (102, 102, 102))),
                             (random.randrange(int(self.width * 0.6531), int(self.width * 0.7536)),
                              random.randrange(int(self.height * 0.6481), int(self.height * 0.7917)), 5.5, 3))

    def fill_background(self):
        for i in range(3000):
            self.screen.fill(random.choice(((51, 51, 51), (102, 102, 102))),
                             (random.random() * self.width, random.random() * self.height, 7, 2))

    def camera(self):
        running = True
        self.condition = 4
        pomehi = pygame.mixer.Sound('data/pomehi.mp3')
        pomehi.set_volume(0.3)

        while running:
            bg = load_image('camera.jpg')
            bg = pygame.transform.scale(bg, self.size)
            rect = bg.get_rect(topleft=(0, 0))
            self.screen.blit(bg, rect)
            back = load_image('back_button.png')
            back = pygame.transform.scale(back, (1300, 70))
            rect = back.get_rect(center=(760, 1000))
            self.screen.blit(back, rect)
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pomehi.stop()
                    self.pause()
                if event.type == self.change_hour:
                    if len(self.hours) > 1:
                        del self.hours[0]
                    else:
                        running = False
                if event.type == self.change_energy:
                    if self.energy > 0:
                        self.energy -= 3
                    else:
                        running = False
                if event.type == pygame.MOUSEBUTTONDOWN and \
                        (self.width * 0.05 <= mouse_pos[0] <= self.width * 0.74 and self.height * 0.9 <=
                         mouse_pos[1] <= self.height * 1):
                    pomehi.stop()
                    if self.is_door_locked:
                        self.open_camera_sound.play()
                        self.door_locked()
                    else:
                        self.open_camera_sound.play()
                        self.default_office()
            self.current_time()
            self.current_energy()
            pomehi.play()
            self.clock.tick(60)
            self.fill_background()
            pygame.display.flip()

        pygame.quit()

    def default_office(self):
        running = True
        self.condition = 1

        while running:

            bg = load_image('default_office.jpg')
            bg = pygame.transform.scale(bg, self.size)
            rect = bg.get_rect(topleft=(0, 0))
            self.screen.blit(bg, rect)

            light_on_sound = pygame.mixer.Sound('data/light_on.mp3')
            light_on_sound.set_volume(0.7)
            close_door_sound = pygame.mixer.Sound('data/close_door.mp3')
            close_door_sound.set_volume(0.3)
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN and \
                        (self.width * 0.3594 <= mouse_pos[0] <= self.width * 0.6354 and self.height * 0.1157 <=
                         mouse_pos[1] <= self.height * 0.787):
                    light_on_sound.play()
                    self.light_office()
                if event.type == pygame.MOUSEBUTTONDOWN and \
                        (self.width * 0.6406 <= mouse_pos[0] <= self.width * 0.6849 and self.height * 0.3796 <=
                         mouse_pos[1] <= self.height * 0.4444):
                    close_door_sound.play()
                    self.door_locked()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.pause()
                if event.type == self.change_hour:
                    if len(self.hours) > 1:
                        del self.hours[0]
                    else:
                        running = False
                if event.type == self.change_energy:
                    if self.energy > 0:
                        self.energy -= 1
                    else:
                        running = False
                if event.type == pygame.MOUSEBUTTONDOWN and \
                        (self.width * 0.6531 <= mouse_pos[0] <= self.width * 0.7536 and self.height * 0.6481 <=
                         mouse_pos[1] <= self.height * 0.7917):
                    self.open_camera_sound.play()
                    self.camera()

            self.current_time()
            self.current_energy()
            self.fill_tv()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def light_office(self):
        running = True
        self.condition = 2

        while running:

            bg = load_image('light_office.jpg')
            bg = pygame.transform.scale(bg, self.size)
            rect = bg.get_rect(topleft=(0, 0))
            self.screen.blit(bg, rect)

            light_off_sound = pygame.mixer.Sound('data/light_off.mp3')
            light_off_sound.set_volume(0.3)
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONUP or \
                        not (self.width * 0.3594 <= mouse_pos[0] <= self.width * 0.6354 and self.height * 0.1157 <=
                             mouse_pos[1] <= self.height * 0.787):
                    light_off_sound.play()
                    self.default_office()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.pause()
                if event.type == self.change_hour:
                    if len(self.hours) > 1:
                        del self.hours[0]
                    else:
                        running = False
                if event.type == self.change_energy:
                    if self.energy > 0:
                        self.energy -= 1
                    else:
                        running = False

            self.current_time()
            self.fill_tv()
            self.current_energy()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def door_locked(self):
        running = True
        self.condition = 3
        self.is_door_locked = True

        while running:

            bg = load_image('door_locked.jpg')
            bg = pygame.transform.scale(bg, self.size)
            rect = bg.get_rect(topleft=(0, 0))
            self.energy_change_time = 3000
            self.screen.blit(bg, rect)

            open_door_sound = pygame.mixer.Sound('data/open_door.mp3')
            open_door_sound.set_volume(0.3)
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN and \
                        (self.width * 0.6406 <= mouse_pos[0] <= self.width * 0.6849 and self.height * 0.3796 <=
                         mouse_pos[1] <= self.height * 0.4444):
                    open_door_sound.play()
                    self.is_door_locked = False
                    self.default_office()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.pause()
                if event.type == self.change_hour:
                    if len(self.hours) > 1:
                        del self.hours[0]
                    else:
                        running = False
                if event.type == self.change_energy:
                    if self.energy > 0:
                        self.energy -= 6
                    else:
                        running = False
                if event.type == pygame.MOUSEBUTTONDOWN and \
                        (self.width * 0.6531 <= mouse_pos[0] <= self.width * 0.7536 and self.height * 0.6481 <=
                         mouse_pos[1] <= self.height * 0.7917):
                    self.open_camera_sound.play()
                    self.camera()

            self.current_time()
            self.current_energy()
            self.fill_tv()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def pause(self):
        paused = True

        continue_button = Button((600, 160), (300, 100),
                                 'menu_button.png', 'Продолжить',
                                 'data/menubtn_sound.mp3', 'menu_button_intersected.png')

        settings_button = Button((580, 280), (300, 100),
                                 'menu_button.png', 'Настройки',
                                 'data/menubtn_sound.mp3', 'menu_button_intersected.png')

        exit_button = Button((550, 400), (300, 100),
                             'menu_button.png', 'Выйти в главное меню',
                             'data/menubtn_sound.mp3', 'menu_button_intersected.png')

        buttons = [continue_button, settings_button, exit_button]

        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    paused = False
                if event.type == pygame.USEREVENT and event.button == continue_button:
                    if self.condition == 1:
                        self.default_office()
                    if self.condition == 2:
                        self.light_office()
                    if self.condition == 3:
                        self.door_locked()
                    if self.condition == 4:
                        self.camera()
                if event.type == pygame.USEREVENT and event.button == settings_button:
                    pass
                if event.type == pygame.USEREVENT and event.button == exit_button:
                    MainMenu().main_window()
                for button in buttons:
                    button.button_pressed(event)

            for button in buttons:
                button.draw(self.screen, pygame.mouse.get_pos())

            pygame.time.delay(1)
            self.current_time()
            self.current_energy()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def current_time(self):
        font = pygame.font.Font('data/MorfinSans-Regular.ttf', 55)
        text_rendered = font.render(f'{self.hours[0]} AM', 1, (255, 255, 255))
        text_rect = text_rendered.get_rect(center=(120, 70))
        self.screen.blit(text_rendered, text_rect)

        font = pygame.font.Font('data/MorfinSans-Regular.ttf', 45)
        text_rendered = font.render(f'Night 1', 1, (255, 0, 0))
        text_rect = text_rendered.get_rect(center=(120, 110))
        self.screen.blit(text_rendered, text_rect)

    def current_energy(self):
        font = pygame.font.Font('data/MorfinSans-Regular.ttf', 55)
        text_rendered = font.render(f'{self.energy} left', 1, (255, 255, 255))
        text_rect = text_rendered.get_rect(center=(150, 1000))
        self.screen.blit(text_rendered, text_rect)

    def end_of_night(self):
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
