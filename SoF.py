import sys
import os
import pygame
import random
# import screen_brightness_control as sbc


CURRENT_NIGHT = 1


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


class Fading:
    def __init__(self):
        pygame.init()
        self.size = self.width, self.height = 1920, 1080
        self.screen = pygame.display.set_mode(self.size, pygame.FULLSCREEN)
        pygame.display.set_caption('Source of Fear')

        self.clock = pygame.time.Clock()

    def fade_in(self, filename):
        fade_in = pygame.Surface((self.width, self.height))
        bg = load_image(filename)
        bg = pygame.transform.scale(bg, (1280, 720))
        rect = bg.get_rect(topleft=(0, 0))
        fade_in.blit(bg, rect)
        fade_in.set_alpha(255)
        alpha = 255
        while alpha > 0:
            self.screen.fill((0, 0, 0))
            alpha -= 3
            fade_in.set_alpha(alpha)
            self.screen.blit(fade_in, (0, 0))
            self.clock.tick(60)
            pygame.display.flip()

    def fadeout(self, filename):
        fadeout = pygame.Surface((self.width, self.height))
        bg = load_image(filename)
        bg = pygame.transform.scale(bg, (1280, 720))
        rect = bg.get_rect(topleft=(0, 0))
        fadeout.blit(bg, rect)
        fadeout.set_alpha(0)
        alpha = 0
        while alpha < 255:
            self.screen.fill((0, 0, 0))
            alpha += 3
            fadeout.set_alpha(alpha)
            self.screen.blit(fadeout, (0, 0))
            self.clock.tick(60)
            pygame.display.flip()


class MainMenu:
    def __init__(self):
        pygame.init()
        self.size = self.width, self.height = 1920, 1080
        self.screen = pygame.display.set_mode(self.size, pygame.FULLSCREEN)
        pygame.display.set_caption('Source of Fear')

        self.clock = pygame.time.Clock()

        self.music_flag = True
        pygame.mixer.music.load('data/menu_music.mp3')
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)

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

            if not self.music_flag:
                pygame.mixer.music.stop()

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

        music_on_button = Button((self.width // 4, 465), (200, 90),
                                 'menu_button.png', 'Вкл',
                                 'data/menubtn_sound.mp3', 'menu_button_intersected.png')

        music_off_button = Button((self.width // 2.7, 465), (200, 90),
                                  'menu_button.png', 'Выкл',
                                  'data/menubtn_sound.mp3', 'menu_button_intersected.png')

        back_button = Button((self.width // 2 - 150, 600), (300, 100),
                             'menu_button.png', 'Назад',
                             'data/menubtn_sound.mp3', 'menu_button_intersected.png')

        buttons = [music_on_button, music_off_button, back_button]

        while running:
            self.screen.fill((0, 0, 0))
            self.fill_background()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if ((event.type == pygame.USEREVENT and event.button == back_button) or
                        (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)):
                    self.main_window()

                if event.type == pygame.USEREVENT and event.button == music_on_button and not self.music_flag:
                    self.music_flag = True
                    pygame.mixer.music.play(-1)

                if event.type == pygame.USEREVENT and event.button == music_off_button:
                    self.music_flag = False
                    pygame.mixer.music.stop()

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
                # pygame.mixer.music.set_volume(round(slider.get_value()) // 100)
                # sbc.set_brightness(round(slider.get_value()))

            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()


def new_game_menu():
    Fading().fade_in('fade_in_menu.jpg')
    FirstNight().introduction()


def fade_i_out(bg):
    Fading().fade_in(bg)


def continue_game_menu():
    if CURRENT_NIGHT == 1:
        Fading().fade_in('fade_in_menu.jpg')
        FirstNight().introduction()


class Office:
    def __init__(self, time_move, number_of_night):

        pygame.init()
        self.size = self.width, self.height = 1920, 1080
        self.screen = pygame.display.set_mode(self.size, pygame.FULLSCREEN)
        pygame.display.set_caption('Source of Fear')

        pygame.mixer.music.load('data/vent.mp3')
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)

        self.laugh_1 = pygame.mixer.Sound('data/laugh1.mp3')
        self.laugh_1.set_volume(0.2)
        self.laugh_2 = pygame.mixer.Sound('data/laugh2.mp3')
        self.laugh_2.set_volume(0.1)
        self.laughs = [self.laugh_1, self.laugh_2]

        self.clock = pygame.time.Clock()
        self.hours = ['12', '1', '2', '3', '4', '5']

        self.energy_counter = 100
        self.energy_left = 100
        self.change_energy_point = 0
        self.energy_change_time = 1000
        self.puppet_change_time = 2000
        self.puppet_time = 100
        self.puppet_left = 99

        self.condition = 0
        self.cam_position = 1
        self.time_move = time_move
        self.is_charge = False

        self.change_hour = pygame.USEREVENT + 0
        pygame.time.set_timer(self.change_hour, 2000)
        self.change_energy = pygame.USEREVENT + 1
        pygame.time.set_timer(self.change_energy, self.energy_change_time)

        self.mannequin = Mannequin(self.screen)
        self.change_position = pygame.USEREVENT + 2
        pygame.time.set_timer(self.change_position, self.time_move)
        self.current_position = 1
        self.number_of_night = number_of_night
        self.changing_position_flag = False
        self.hall_move_flag = 0

        self.screamer = pygame.USEREVENT + 3
        pygame.time.set_timer(self.screamer, 1500)

        self.puppet_change = pygame.USEREVENT + 4
        pygame.time.set_timer(self.puppet_change, self.puppet_change_time)

        self.puppet_plus = pygame.USEREVENT + 5
        pygame.time.set_timer(self.puppet_plus, 1000)

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
        run_sound = pygame.mixer.Sound('data/run_to_puppet.mp3')
        run_sound.set_volume(0.3)
        raw_array = run_sound.get_raw()
        raw_array = raw_array[100000:270000]
        run_sound = pygame.mixer.Sound(buffer=raw_array)

        while running:

            bg = load_image('default_office.jpg')
            rect = bg.get_rect(topleft=(0, 0))
            self.screen.blit(bg, rect)

            if self.hall_move_flag:
                self.mannequin_moving()
                self.hall_move_flag = 0

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
                    if len(self.hours) != 1:
                        del self.hours[0]
                    else:
                        fade_i_out('default_office.jpg')
                        winning(self.number_of_night)
                if event.type == self.change_energy:
                    if self.energy_counter > 0:
                        self.energy_counter -= 0.1
                    else:
                        self.current_position = 7
                if event.type == self.puppet_change:
                    if self.puppet_time > 0:
                        self.puppet_time -= 2
                    else:
                        self.current_position = 7
                if event.type == self.change_position:
                    self.time_move = random.randrange(7000, 20000)
                    self.mannequin_moving()
                    print(self.time_move)
                if event.type == pygame.MOUSEBUTTONDOWN and \
                        (1150 <= mouse_pos[0] <= 1400 and 150 <= mouse_pos[1] <= 678):
                    self.condition = 1
                    run_sound.play()
                    fade_i_out('default_office.jpg')
                    self.puppet()

            self.current_time()
            self.current_energy()
            self.fill_tv()
            if self.current_position == 7:
                pygame.mixer.music.stop()
                screamer_sound = pygame.mixer.Sound('data/screamer_sound.mp3')
                screamer_sound.set_volume(0.3)
                self.mannequin.mannequin_pos_office()
                screamer_sound.play()
                for event in pygame.event.get():
                    if event.type == self.screamer:
                        screamer_sound.stop()
                        losing()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def light_office(self):
        running = True

        while running:

            bg = load_image('light_office.jpg')
            rect = bg.get_rect(topleft=(0, 0))
            self.screen.blit(bg, rect)
            if self.current_position == 3:
                self.mannequin.pos1_hall()
            if self.current_position == 4:
                self.mannequin.pos2_hall()
            if self.current_position == 7:
                self.default_office()

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
                    if len(self.hours) != 1:
                        del self.hours[0]
                    else:
                        winning(self.number_of_night)
                if event.type == self.change_energy:
                    if self.energy_counter > 0:
                        self.energy_counter -= 0.3
                    else:
                        self.current_position = 7
                if event.type == self.puppet_change:
                    if self.puppet_time > 0:
                        self.puppet_time -= 2
                    else:
                        self.current_position = 7
                if event.type == self.change_position:
                    self.time_move = random.randrange(7000, 20000)
                    if self.current_position == 2 or self.current_position == 3:
                        self.hall_move_flag = 1
                        self.default_office()

            self.current_time()
            self.current_energy()
            self.fill_tv()
            if self.current_position == 7:
                pygame.mixer.music.stop()
                screamer_sound = pygame.mixer.Sound('data/screamer_sound.mp3')
                screamer_sound.set_volume(0.3)
                self.mannequin.mannequin_pos_office()
                screamer_sound.play()
                for event in pygame.event.get():
                    if event.type == self.screamer:
                        screamer_sound.stop()
                        losing()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def door_locked(self):
        running = True
        run_sound = pygame.mixer.Sound('data/run_to_puppet.mp3')
        run_sound.set_volume(0.3)
        raw_array = run_sound.get_raw()
        raw_array = raw_array[100000:270000]
        run_sound = pygame.mixer.Sound(buffer=raw_array)

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
                    if len(self.hours) != 1:
                        del self.hours[0]
                    else:
                        fade_i_out('door_locked.jpg')
                        winning(self.number_of_night)
                if event.type == self.puppet_change:
                    if self.puppet_time > 0:
                        self.puppet_time -= 2
                    else:
                        self.current_position = 7
                if event.type == self.change_energy:
                    if self.energy_counter > 0:
                        self.energy_counter -= 0.4
                    else:
                        self.current_position = 7
                if event.type == self.change_position:
                    self.time_move = random.randrange(7000, 20000)
                    self.mannequin_moving()
                if event.type == pygame.MOUSEBUTTONDOWN and \
                        (1150 <= mouse_pos[0] <= 1400 and 150 <= mouse_pos[1] <= 678):
                    self.condition = 3
                    run_sound.play()
                    fade_i_out('door_locked.jpg')
                    self.puppet()

            self.current_time()
            self.current_energy()
            self.fill_tv()
            if self.current_position == 7:
                pygame.mixer.music.stop()
                screamer_sound = pygame.mixer.Sound('data/screamer_sound.mp3')
                screamer_sound.set_volume(0.3)
                self.mannequin.mannequin_pos_office()
                screamer_sound.play()
                for event in pygame.event.get():
                    if event.type == self.screamer:
                        screamer_sound.stop()
                        losing()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def camera(self):

        running = True

        pygame.mixer.music.load('data/pomehi.mp3')
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)

        x = random.randrange(1, 10)

        camera_sound = pygame.mixer.Sound('data/change_camera.mp3')
        camera_sound.set_volume(0.3)

        while running:
            if self.hall_move_flag:
                self.mannequin_moving()
                self.hall_move_flag = 0

            if self.cam_position == 1:
                bg = load_image('cam1.jpg')
                rect = bg.get_rect(topleft=(0, 0))
                self.screen.blit(bg, rect)
                if self.current_position == 1:
                    self.mannequin.pos1_cam1()
                if self.current_position == 2:
                    self.mannequin.pos2_cam1()
            if self.cam_position == 2:
                bg = load_image('cam2.jpg')
                rect = bg.get_rect(topleft=(0, 0))
                self.screen.blit(bg, rect)
                if self.current_position == 5:
                    self.mannequin.pos1_cam2()
                if self.current_position == 6:
                    self.mannequin.pos2_cam2()
            if self.current_position == 7:
                self.default_office()

            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == self.change_hour:
                    if len(self.hours) != 1:
                        del self.hours[0]
                    else:
                        fade_i_out('default_office.jpg')
                        winning(self.number_of_night)
                if event.type == self.change_energy:
                    if self.energy_counter > 0:
                        if self.condition == 3:
                            self.energy_counter -= 0.5
                        else:
                            self.energy_counter -= 0.3
                    else:
                        self.current_position = 7
                    if event.type == self.puppet_change:
                        if self.puppet_time > 0:
                            self.puppet_time -= 2
                        else:
                            self.current_position = 7
                if (event.type == pygame.MOUSEBUTTONDOWN and
                    (72 <= mouse_pos[0] <= 937 and 644 <= mouse_pos[1] <= 687)) or \
                        (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
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
                if event.type == self.change_position:
                    self.time_move = random.randrange(7000, 20000)
                    self.mannequin_moving()

            if x == 9:
                random.choice(self.laughs).play()
                x = 0

            button_image = load_image('back_button.png')
            button_image = pygame.transform.scale(button_image, (865, 45))
            rect = button_image.get_rect(center=(505, 665))
            self.screen.blit(button_image, rect)
            self.current_time()
            self.current_energy()
            self.fill_background()
            if self.current_position == 7:
                pygame.mixer.music.stop()
                screamer_sound = pygame.mixer.Sound('data/screamer_sound.mp3')
                screamer_sound.set_volume(0.3)
                self.mannequin.mannequin_pos_office()
                screamer_sound.play()
                for event in pygame.event.get():
                    if event.type == self.screamer:
                        screamer_sound.stop()
                        losing()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def puppet(self):
        running = True
        run_sound = pygame.mixer.Sound('data/run_to_puppet.mp3')
        run_sound.set_volume(0.3)
        raw_array = run_sound.get_raw()
        raw_array = raw_array[100000:270000]
        run_sound = pygame.mixer.Sound(buffer=raw_array)

        pygame.mixer.music.load('data/puppet_theme.mp3')
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)

        while running:
            mouse_pos = pygame.mouse.get_pos()
            bg = load_image('cam3.jpg')
            rect = bg.get_rect(topleft=(0, 0))
            self.screen.blit(bg, rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == self.change_hour:
                    if len(self.hours) != 1:
                        del self.hours[0]
                    else:
                        fade_i_out('cam3.jpg')
                        winning(self.number_of_night)
                if event.type == self.change_energy:
                    if self.energy_counter > 0:
                        self.energy_counter -= 0.2
                    else:
                        self.current_position = 7
                if event.type == self.puppet_plus:
                    if self.is_charge and self.puppet_time < 100:
                        self.puppet_time += 5
                        self.puppet_left += 5
                        print(self.puppet_time)
                        print(self.puppet_left)
                if event.type == self.puppet_change and not self.is_charge:
                    if self.puppet_time > 0:
                        self.puppet_time -= 5
                        print(self.puppet_left)
                    else:
                        self.current_position = 7
                if (event.type == pygame.MOUSEBUTTONDOWN and
                    (72 <= mouse_pos[0] <= 937 and 644 <= mouse_pos[1] <= 687)) or \
                        (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    run_sound.play()
                    fade_i_out('cam3.jpg')
                    pygame.mixer.music.load('data/vent.mp3')
                    pygame.mixer.music.set_volume(0.2)
                    pygame.mixer.music.play(-1)
                    if self.condition == 1:
                        self.default_office()
                    if self.condition == 3:
                        self.door_locked()
                if event.type == self.change_position:
                    self.time_move = random.randrange(7000, 20000)
                    self.mannequin_moving()
                if event.type == pygame.MOUSEBUTTONDOWN and \
                        (970 <= mouse_pos[0] <= 1300 and 390 <= mouse_pos[1] <= 835):
                    self.is_charge = True
                if event.type == pygame.MOUSEBUTTONUP or \
                        not (970 <= mouse_pos[0] <= 1300 and 390 <= mouse_pos[1] <= 835):
                    self.is_charge = False

            button_image = load_image('back_button.png')
            button_image = pygame.transform.scale(button_image, (865, 45))
            rect = button_image.get_rect(center=(505, 665))
            self.screen.blit(button_image, rect)

            button_image = load_image('puppet_button.png')
            button_image = pygame.transform.scale(button_image, (255, 255))
            rect = button_image.get_rect(center=(1115, 548))
            self.screen.blit(button_image, rect)

            font = pygame.font.Font('data/MorfinSans-Regular.ttf', 50)
            text_rendered = font.render(f'Завести', 1, (255, 255, 255))
            text_rect = text_rendered.get_rect(center=(1115, 520))
            self.screen.blit(text_rendered, text_rect)

            font = pygame.font.Font('data/MorfinSans-Regular.ttf', 50)
            text_rendered = font.render(f'шкатулку', 1, (255, 255, 255))
            text_rect = text_rendered.get_rect(center=(1115, 580))
            self.screen.blit(text_rendered, text_rect)

            self.current_time()
            self.current_energy()
            self.current_puppet()
            if self.current_position == 7:
                pygame.mixer.music.stop()
                screamer_sound = pygame.mixer.Sound('data/screamer_sound.mp3')
                screamer_sound.set_volume(0.3)
                self.mannequin.mannequin_pos_office()
                screamer_sound.play()
                for event in pygame.event.get():
                    if event.type == self.screamer:
                        screamer_sound.stop()
                        losing()
            self.clock.tick(60)
            pygame.display.flip()

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
            self.clock.tick(60)
            pygame.display.flip()

        pygame.quit()

    def current_time(self):
        font = pygame.font.Font('data/MorfinSans-Regular.ttf', 55)
        text_rendered = font.render(f'{self.hours[0]} AM', 1, (255, 255, 255))
        text_rect = text_rendered.get_rect(center=(100, 50))
        self.screen.blit(text_rendered, text_rect)

        font = pygame.font.Font('data/MorfinSans-Regular.ttf', 45)
        text_rendered = font.render(f'Ночь {str(self.number_of_night)}', 1, (255, 0, 0))
        text_rect = text_rendered.get_rect(center=(100, 100))
        self.screen.blit(text_rendered, text_rect)

    def current_energy(self):
        if self.energy_counter <= (self.energy_left - 1):
            self.energy_left -= 1
        font = pygame.font.Font('data/MorfinSans-Regular.ttf', 55)
        text_rendered = font.render(f'{self.energy_left}%', 1, (255, 255, 255))
        text_rect = text_rendered.get_rect(center=(1200, 50))
        self.screen.blit(text_rendered, text_rect)

    def current_puppet(self):
        if self.puppet_time <= (self.puppet_left - 1):
            self.puppet_left -= 1
        font = pygame.font.Font('data/MorfinSans-Regular.ttf', 60)
        text_rendered = font.render(f'{self.puppet_left} to die', 1, (255, 0, 0))
        text_rect = text_rendered.get_rect(center=(1120, 400))
        self.screen.blit(text_rendered, text_rect)

    def mannequin_moving(self):
        if self.number_of_night == 1:
            self.changing_position_flag = True
            if self.current_position == 1 and self.changing_position_flag:
                self.current_position = 2
                self.changing_position_flag = False
            if self.current_position == 2 and self.changing_position_flag:
                self.current_position = 3
                self.changing_position_flag = False
            if self.current_position == 3 and self.changing_position_flag:
                self.current_position = 4
                self.changing_position_flag = False
            if self.current_position == 4 and self.changing_position_flag:
                if self.condition == 3:
                    self.current_position = 5
                    self.changing_position_flag = False
                if self.condition == 1 or self.condition == 2:
                    self.current_position = 7
                    self.changing_position_flag = False
            if self.current_position == 5 and self.changing_position_flag:
                self.current_position = 6
                self.changing_position_flag = False
            if self.current_position == 6 and self.changing_position_flag:
                self.current_position = 2
                self.changing_position_flag = False



class Mannequin(pygame.sprite.Sprite):
    def __init__(self, sc):
        pygame.sprite.Sprite.__init__(self)
        self.screen = sc
        self.pos1, self.size1 = (600, 380), (100, 250)
        self.pos2, self.size2 = (300, 380), (230, 320)
        self.pos3, self.size3 = (500, 350), (150, 250)
        self.pos4, self.size4 = (570, 320), (750, 700)
        self.pos5, self.size5 = (570, 250), (80, 110)
        self.pos6, self.size6 = (650, 330), (250, 380)
        self.pos7, self.size7 = (630, 400), (900, 950)

    def pos1_cam1(self):
        image = load_image('mannequin_pos1.png')
        image = pygame.transform.scale(image, self.size1)
        rect = image.get_rect(center=self.pos1)
        self.screen.blit(image, rect)

    def pos2_cam1(self):
        image = load_image('mannequin_pos2.png')
        image = pygame.transform.scale(image, self.size2)
        rect = image.get_rect(center=self.pos2)
        self.screen.blit(image, rect)

    def pos1_cam2(self):
        image = load_image('mannequin_pos3.png')
        image = pygame.transform.scale(image, self.size3)
        rect = image.get_rect(center=self.pos3)
        self.screen.blit(image, rect)

    def pos2_cam2(self):
        image = load_image('mannequin_pos4.png')
        image = pygame.transform.scale(image, self.size4)
        rect = image.get_rect(center=self.pos4)
        self.screen.blit(image, rect)

    def pos1_hall(self):
        image = load_image('mannequin_pos5.png')
        image = pygame.transform.scale(image, self.size5)
        rect = image.get_rect(center=self.pos5)
        self.screen.blit(image, rect)

    def pos2_hall(self):
        image = load_image('mannequin_pos6.png')
        image = pygame.transform.scale(image, self.size6)
        rect = image.get_rect(center=self.pos6)
        self.screen.blit(image, rect)

    def mannequin_pos_office(self):
        image = load_image('mannequin_pos_office.png')
        image = pygame.transform.scale(image, self.size7)
        rect = image.get_rect(center=self.pos7)
        self.screen.blit(image, rect)


class FirstNight:
    def __init__(self):

        pygame.init()
        self.size = self.width, self.height = 1920, 1080
        self.screen = pygame.display.set_mode(self.size, pygame.FULLSCREEN)
        pygame.display.set_caption('Source of Fear')

        self.clock = pygame.time.Clock()

    def introduction(self):
        running = True

        while running:
            self.screen.fill((0, 0, 0))
            click_sound = pygame.mixer.Sound('data/menubtn_sound.mp3')
            click_sound.set_volume(0.3)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    click_sound.play()
                    Fading().fade_in('first_night_fade.jpg')
                    self.playing_process()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    click_sound.play()
                    Fading().fade_in('first_night_fade.jpg')
                    MainMenu().main_window()

            font1 = pygame.font.Font('data/MorfinSans-Regular.ttf', 150)
            text_rendered = font1.render(f'Первая ночь', 1, pygame.Color('red'))
            text_rect = text_rendered.get_rect(center=((self.width // 2 - text_rendered.get_width() // 2 + 20), 300))
            self.screen.blit(text_rendered, text_rect)

            font2 = pygame.font.Font('data/MorfinSans-Regular.ttf', 70)
            text_rendered = font2.render(f'Нажмите Enter, чтобы начать', 1, pygame.Color('white'))
            text_rect = text_rendered.get_rect(center=((self.width // 2 - text_rendered.get_width() // 2 + 70), 450))
            self.screen.blit(text_rendered, text_rect)

            self.clock.tick(60)
            pygame.display.flip()
        pygame.quit()

    def playing_process(self):
        running = True

        while running:
            Office(random.randrange(10000, 20000), 1).default_office()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.clock.tick(60)
            pygame.display.flip()
        pygame.quit()


def winning(night_completed):
    global CURRENT_NIGHT
    CURRENT_NIGHT = night_completed + 1
    pygame.init()
    size = width, height = 1920, 1080
    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
    pygame.display.set_caption('Source of Fear')

    pygame.mixer.music.load('data/winning.mp3')
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)

    game_over_screen = pygame.USEREVENT + 6
    pygame.time.set_timer(game_over_screen, 7500)
    clock = pygame.time.Clock()

    running = True
    while running:
        screen.fill((0, 0, 0))
        for i in range(3000):
            screen.fill(random.choice(((51, 51, 51), (102, 102, 102))),
                        (random.random() * width, random.random() * height, 7, 2))

        font = pygame.font.Font('data/MorfinSans-Regular.ttf', 200)
        text_rendered = font.render('6 AM', 1, (255, 0, 0))
        text_rect = text_rendered.get_rect(center=((width // 2 - text_rendered.get_width() + 50),
                                                   (height // 2 - text_rendered.get_height() // 2 - 70)))
        screen.blit(text_rendered, text_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == game_over_screen:
                pygame.mixer.music.stop()
                MainMenu().main_window()

        clock.tick(60)
        pygame.display.flip()
    pygame.quit()


def losing():
    pygame.init()
    size = width, height = 1920, 1080
    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
    pygame.display.set_caption('Source of Fear')

    pygame.mixer.music.load('data/game_over_sound.mp3')
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)

    game_over_screen = pygame.USEREVENT + 6
    pygame.time.set_timer(game_over_screen, 7000)
    clock = pygame.time.Clock()

    running = True
    while running:
        screen.fill((0, 0, 0))
        for i in range(3000):
            screen.fill(random.choice(((51, 51, 51), (102, 102, 102))),
                        (random.random() * width, random.random() * height, 7, 2))

        font = pygame.font.Font('data/MorfinSans-Regular.ttf', 200)
        text_rendered = font.render('GAME OVER', 1, (255, 0, 0))
        text_rect = text_rendered.get_rect(center=((width // 2 - text_rendered.get_width() // 2 + 90),
                                                   (height // 2 - text_rendered.get_height() // 2 - 70)))
        screen.blit(text_rendered, text_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == game_over_screen:
                pygame.mixer.music.stop()
                MainMenu().main_window()

        clock.tick(60)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    MainMenu().main_window()
