import sys
import os
import pygame
import random
# import screen_brightness_control as sbc


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
                    pygame.mixer.music.stop()
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
                pygame.mixer.music.set_volume(round(slider.get_value()) // 100)
                # sbc.set_brightness(round(slider.get_value()))

            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()


def new_game_menu():
    Office().default_office()


def continue_game_menu():
    pass


class Office:
    def __init__(self):

        pygame.init()
        self.size = self.width, self.height = 1920, 1080
        self.screen = pygame.display.set_mode(self.size, pygame.FULLSCREEN)
        pygame.display.set_caption('Source of Fear')

        pygame.mixer.music.load('data/vent.mp3')
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)

        self.clock = pygame.time.Clock()
        self.hours = ['12', '1', '2', '3', '4', '5']

        self.energy_counter = 100
        self.energy_left = 100
        self.change_energy_point = 0
        self.energy_change_time = 1000

        self.condition = 0
        self.cam_position = 1

        self.change_hour = pygame.USEREVENT + 0
        pygame.time.set_timer(self.change_hour, 50000)
        self.change_energy = pygame.USEREVENT + 1
        pygame.time.set_timer(self.change_energy, self.energy_change_time)

    def fill_background(self):
        for i in range(3000):
            self.screen.fill(random.choice(((51, 51, 51), (102, 102, 102))),
                             (random.random() * self.width, random.random() * self.height, 7, 2))

    def fill_tv(self):
        pygame.draw.rect(self.screen, (70, 70, 70), (850, 472, 133, 108))
        for i in range(500):
            pygame.draw.rect(self.screen, random.choice(((34, 34, 34), (102, 102, 102))),
                             (random.randrange(850, 976),
                              random.randrange(472, 578), 7, 2))

    def default_office(self):
        running = True

        while running:

            bg = load_image('default_office.jpg')
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
                        (480 <= mouse_pos[0] <= 820 and 105 <= mouse_pos[1] <= 550):
                    light_on_sound.play()
                    self.light_office()
                if event.type == pygame.MOUSEBUTTONDOWN and \
                        (838 <= mouse_pos[0] <= 884 and 282 <= mouse_pos[1] <= 326):
                    close_door_sound.play()
                    self.door_locked()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.condition = 1
                    bg = load_image('default_office_paused.jpg')
                    rect = bg.get_rect(topleft=(0, 0))
                    self.screen.blit(bg, rect)
                    self.pause()
                if event.type == pygame.MOUSEBUTTONDOWN and \
                        (850 <= mouse_pos[0] <= 976 and 472 <= mouse_pos[1] <= 578):
                    self.condition = 1
                    pygame.mixer.music.stop()
                    self.camera()
                if event.type == self.change_hour:
                    if len(self.hours) > 1:
                        del self.hours[0]
                    else:
                        running = False
                if event.type == self.change_energy:
                    if self.energy_counter > 0:
                        self.energy_counter -= 0.1
                    else:
                        running = False

            self.current_time()
            self.current_energy()
            self.fill_tv()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def light_office(self):
        running = True

        while running:

            bg = load_image('light_office.jpg')
            rect = bg.get_rect(topleft=(0, 0))
            self.screen.blit(bg, rect)

            light_off_sound = pygame.mixer.Sound('data/light_off.mp3')
            light_off_sound.set_volume(0.3)
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONUP or \
                        not (480 <= mouse_pos[0] <= 820 and 105 <= mouse_pos[1] <= 550):
                    light_off_sound.play()
                    self.default_office()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.condition = 2
                    bg = load_image('light_office_paused.jpg')
                    rect = bg.get_rect(topleft=(0, 0))
                    self.screen.blit(bg, rect)
                    self.pause()
                if event.type == self.change_hour:
                    if len(self.hours) > 1:
                        del self.hours[0]
                    else:
                        running = False
                if event.type == self.change_energy:
                    if self.energy_counter > 0:
                        self.energy_counter -= 0.3
                    else:
                        running = False

            self.current_time()
            self.current_energy()
            self.fill_tv()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def door_locked(self):
        running = True

        while running:

            bg = load_image('door_locked.jpg')
            rect = bg.get_rect(topleft=(0, 0))
            self.screen.blit(bg, rect)

            open_door_sound = pygame.mixer.Sound('data/open_door.mp3')
            open_door_sound.set_volume(0.3)
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN and \
                        (838 <= mouse_pos[0] <= 884 and 282 <= mouse_pos[1] <= 326):
                    open_door_sound.play()
                    self.default_office()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.condition = 3
                    bg = load_image('door_locked_paused.jpg')
                    rect = bg.get_rect(topleft=(0, 0))
                    self.screen.blit(bg, rect)
                    self.pause()
                if event.type == pygame.MOUSEBUTTONDOWN and \
                        (850 <= mouse_pos[0] <= 976 and 472 <= mouse_pos[1] <= 578):
                    self.condition = 3
                    pygame.mixer.music.stop()
                    self.camera()
                if event.type == self.change_hour:
                    if len(self.hours) > 1:
                        del self.hours[0]
                    else:
                        running = False
                if event.type == self.change_energy:
                    if self.energy_counter > 0:
                        self.energy_counter -= 0.4
                    else:
                        running = False

            self.current_time()
            self.current_energy()
            self.fill_tv()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def camera(self):

        running = True

        pygame.mixer.music.load('data/pomehi.mp3')
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)

        camera_sound = pygame.mixer.Sound('data/change_camera.mp3')
        camera_sound.set_volume(0.3)

        while running:

            if self.cam_position == 1:
                bg = load_image('cam1.jpg')
                rect = bg.get_rect(topleft=(0, 0))
                self.screen.blit(bg, rect)
            if self.cam_position == 2:
                bg = load_image('cam2.jpg')
                rect = bg.get_rect(topleft=(0, 0))
                self.screen.blit(bg, rect)

            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                # if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    # self.condition = 4
                    # pygame.mixer.music.stop()
                    # self.pause()
                if event.type == self.change_hour:
                    if len(self.hours) > 1:
                        del self.hours[0]
                    else:
                        running = False
                if event.type == self.change_energy:
                    if self.energy_counter > 0:
                        if self.condition == 3:
                            self.energy_counter -= 0.8
                        else:
                            self.energy_counter -= 0.3
                    else:
                        running = False
                if event.type == pygame.MOUSEBUTTONDOWN and \
                        (72 <= mouse_pos[0] <= 937 and 644 <= mouse_pos[1] <= 687):
                    pygame.mixer.music.stop()
                    camera_sound.play()
                    pygame.mixer.music.load('data/vent.mp3')
                    pygame.mixer.music.set_volume(0.2)
                    pygame.mixer.music.play(-1)
                    if self.condition == 1:
                        self.default_office()
                    if self.condition == 3:
                        self.door_locked()
                if event.type == pygame.MOUSEBUTTONDOWN and \
                        (1040 <= mouse_pos[0] <= 1150 and 482 <= mouse_pos[1] <= 550):
                    camera_sound.play()
                    self.cam_position = 1
                if event.type == pygame.MOUSEBUTTONDOWN and \
                        (1161 <= mouse_pos[0] <= 1209 and 489 <= mouse_pos[1] <= 544):
                    camera_sound.play()
                    self.cam_position = 2

            button_image = load_image('back_button.png')
            button_image = pygame.transform.scale(button_image, (865, 45))
            rect = button_image.get_rect(center=(505, 665))
            self.screen.blit(button_image, rect)
            self.current_time()
            self.current_energy()
            self.fill_background()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def pause(self):
        paused = True

        continue_button = Button((500, 250), (300, 100),
                                 'menu_button.png', 'Продолжить',
                                 'data/menubtn_sound.mp3', 'menu_button_intersected.png')

        exit_button = Button((495, 380), (300, 100),
                             'menu_button.png', 'Выйти в меню',
                             'data/menubtn_sound.mp3', 'menu_button_intersected.png')

        buttons = [continue_button, exit_button]

        pygame.mixer.music.pause()

        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    paused = False
                if event.type == pygame.USEREVENT and event.button == continue_button:
                    pygame.mixer.music.unpause()
                    if self.condition == 1 or self.condition == 2:
                        self.default_office()
                    if self.condition == 3:
                        self.door_locked()
                if event.type == pygame.USEREVENT and event.button == exit_button:
                    pygame.time.set_timer(self.change_hour, 0)
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
        text_rect = text_rendered.get_rect(center=(100, 50))
        self.screen.blit(text_rendered, text_rect)

        font = pygame.font.Font('data/MorfinSans-Regular.ttf', 45)
        text_rendered = font.render(f'Night 1', 1, (255, 0, 0))
        text_rect = text_rendered.get_rect(center=(100, 100))
        self.screen.blit(text_rendered, text_rect)

    def current_energy(self):
        if self.energy_counter <= (self.energy_left - 1):
            self.energy_left -= 1
        font = pygame.font.Font('data/MorfinSans-Regular.ttf', 55)
        text_rendered = font.render(f'{self.energy_left}%', 1, (255, 255, 255))
        text_rect = text_rendered.get_rect(center=(1200, 50))
        self.screen.blit(text_rendered, text_rect)


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
