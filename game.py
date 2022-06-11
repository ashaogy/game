import game_object
from game_menu import *
import cv2


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode([WIN_WIDTH, WIN_HEIGHT])
        pygame.display.set_caption('Platformer Dev')
        self.background_img = pygame.image.load("background_wide.png").convert()
        self.all_sprite_list = pygame.sprite.Group()

        # Скорость движения врага
        self.speed = 2

        # Платформы
        self.platform_list = pygame.sprite.Group()
        self.create_walls()

        # Артефакты
        self.artifact_list = pygame.sprite.Group()
        self.create_artifacts()

        # Враги
        self.enemy_list = pygame.sprite.Group()
        self.create_enemies()

        # Girl
        self.player = game_object.Player(0, 0)
        self.player.platforms = self.platform_list
        self.player.artifacts = self.artifact_list
        self.all_sprite_list.add(self.player)

        # MainMenu
        self.top_panel = TopPanel(20, 10)
        self.main_menu = MainMenu(300, 200)

        # Меню Settings
        self.settings_menu = SettingsMenu(300, 200)

        # Смещение игрового мира:
        self.shift = 0
        self.player_global_x = self.player.rect.x
        self.game_width = self.background_img.get_rect().width

        self.clock = pygame.time.Clock()
        self.time = 0
        self.hit_time = 0

        # Игровые сцены state: 'START', MENU', 'SETTINGS', 'GAME', 'PAUSE' ' 'FINISH', 'GAME_OVER'
        self.state = 'PREVIU'
        self.music = pygame.mixer.Sound('intro.mp3')

    @property
    def play_movie(self):

        filename = 'intro.mp4'

        cap = cv2.VideoCapture(filename)

        ret, img = cap.read()
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        print(ret)
        if not ret:
            print("Видео невозможно прочитать")
            return quit()
        img = cv2.resize(img, (WIN_WIDTH, WIN_HEIGHT))

        img = cv2.transpose(img)

        # создаю поверхность Surface соответствующего размера, на которой будет отображаться видео:
        surface = pygame.surface.Surface((img.shape[0], img.shape[1]))
        clock = pygame.time.Clock()
        # Устанавливаю частоту кадров в соответствии с частотой кадров в видео:
        FPS = 50

        # Начинаем воспроизведение звука
        self.music.play(0)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        running = False
                        self.state = "START"
            ret, img = cap.read()
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            if not ret:
                running = False
                break
            else:
                # изменяем изображение под размер формы
                img = cv2.resize(img, (WIN_WIDTH, WIN_HEIGHT))
                # Транспонируем полученное изображение:
                img = cv2.transpose(img)
                pygame.surfarray.blit_array(surface, img)
                self.screen.blit(surface, (0, 0))
            pygame.display.flip()
            clock.tick(FPS)
        if running == False:
            self.music.stop()

    # Создаем стены и платформы
    def create_walls(self):
        platform_coords = [
            [100, 600],
            [200, 550],
            [250, 550],
            [300, 450],
            [300, 500],
            [300, 550],
            [300, 500],
            [300, 550],
            [450, 450],
            [550, 350],
            [600, 350],
            [700, 300],
            [750, 300],
            [850, 250],
            [900, 250],
            [850, 550],
            [900, 550],
            [950, 450],
            [1100, 500],
            [1100, 550],
            [1150, 400],
            [1150, 450],
            [1150, 500],
            [1150, 550],
            [1300, 400],
            [1350, 400],
            [1400, 400],
            [1500, 400]
        ]
        for coord in platform_coords:
            platform = game_object.Platform(coord[0], coord[1], 2)
            self.platform_list.add(platform)
            self.all_sprite_list.add(platform)

    # Создаем артефакты (ягоды) в игре
    def create_artifacts(self):
        artifact_coords = [
            [150, 450],
            [200, 450],
            [350, 450],
            [300, 250],
            [300, 300],
            [300, 350],
            [200, 400],
            [450, 400],
            [600, 200],
            [600, 300],
            [600, 550],
            [750, 550],
            [750, 250],
            [750, 150],
            [900, 150],
            [900, 100],
            [900, 150],
            [900, 200],
            [1150, 300],
            [1150, 350],
            [1300, 200],
            [1300, 250],
            [1400, 200],
            [1400, 250],
            [1500, 200],
            [1500, 250],
        ]
        for coord in artifact_coords:
            artifact = game_object.Artifact(coord[0], coord[1])
            self.artifact_list.add(artifact)
            self.all_sprite_list.add(artifact)

    # Создаем противников
    def create_enemies(self):

        enemies_coords = [
            [1200, 200, 1600],
            [100, 300, 400],
            [450, 500, 800],
            [1200, 500, 1600]
        ]
        for coord in enemies_coords:
            enemy = game_object.Enemy(coord[0], coord[1], self.speed)
            enemy.stop = coord[2]
            self.enemy_list.add(enemy)
            self.all_sprite_list.add(enemy)

    # Выполняем сдвиг игрового мира при перемещении игрока
    def shift_world(self, shift_x):
        self.shift += shift_x

        for platform in self.platform_list:
            platform.rect.x += shift_x

        for artifact in self.artifact_list:
            artifact.rect.x += shift_x

        for enemy in self.enemy_list:
            enemy.shift(shift_x)

    # Обработка события для разных сотояний в игре
    def handle_states(self, event):
        if self.state in ['START', 'FINISH', 'GAME OVER']:
            if event.type == pygame.KEYDOWN:
                self.state = 'MENU'

        # Обрабатываем события главного меню:
        elif self.state in ['MENU', 'PAUSE']:
            active_button = self.main_menu.handle_mouse_event(event.type)
            if active_button:
                active_button.state = 'normal'
                if active_button.name == 'START':
                    self.__init__()
                    self.state = 'GAME'
                elif active_button.name == 'CONTINUE':
                    self.state = 'GAME'
                elif active_button.name == 'SETTINGS':
                    self.state = 'SETTINGS'
                elif active_button.name == 'QUIT':
                    pygame.quit()

        # Обрабатотка события меню настроек:
        elif self.state == 'SETTINGS':
            active_button = self.settings_menu.handle_mouse_event(event.type)
            if active_button:
                if active_button.name in ['OK', 'CANCEL']:
                    active_button.state = 'normal'
                    if active_button.name == 'OK':
                        for enemy in self.enemy_list:
                            enemy.speed = self.speed
                        self.state = 'MENU'
                    else:
                        self.state = 'MENU'
                else:
                    # Нажали на кнопку FAST, меняем скорость движения врагов:
                    if active_button.name == 'FAST':
                        self.speed = 10
                        active_button.state = 'active'

                    # Нажали на кнопку MEDIUM, меняем скорость движения врагов:
                    elif active_button.name == 'MEDIUM':
                        self.speed = 5
                        active_button.state = 'active'

                    # Нажали на кнопку SLOW, меняем скорость движения врагов:
                    elif active_button.name == 'SLOW':
                        self.speed = 1
                        active_button.state = 'active'


        # Обработка событий, когда идет игра
        elif self.state == 'GAME':
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.go_left()
                elif event.key == pygame.K_RIGHT:
                    self.player.go_right()
                elif event.key == pygame.K_UP:
                    self.player.jump()

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and self.player.change_x < 0:
                    self.player.stop()
                if event.key == pygame.K_RIGHT and self.player.change_x > 0:
                    self.player.stop()
                elif event.key == pygame.K_ESCAPE:
                    self.state = 'MENU'

    # Прорисовка сцены
    def draw(self):
        if self.state == 'START':
            self.screen.blit(pygame.image.load("start_screen.png").convert(), [0, 0])
        elif self.state == 'MENU':
            self.screen.blit(pygame.image.load("background.png").convert(), [0, 0])
            self.main_menu.draw(self.screen)
        elif self.state == 'SETTINGS':
            self.screen.blit(pygame.image.load("background.png").convert(), [0, 0])
            self.settings_menu.draw(self.screen)
        elif self.state == 'GAME':
            self.screen.blit(self.background_img, [self.shift, 0])
            self.top_panel.draw(self.screen)
            self.all_sprite_list.draw(self.screen)
        elif self.state == "PREVIU":
            self.play_movie
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.state = "START"

        elif self.state == 'FINISH':
            # фон
            self.screen.blit(pygame.image.load("background.png").convert(), [0, 0])
            # надпись

            self.label = FONT.render('YOU WIN!', True, GREEN)
            self.screen.blit(self.label, [WIN_WIDTH / 2.3, WIN_HEIGHT // 1.5])
            self.label = FONT.render('BERRIES SCORE: ', True, BLACK)
            self.screen.blit(self.label, [WIN_WIDTH / 2.9, WIN_HEIGHT // 1.3])
            self.label = FONT.render(str(self.player.score), True, RED)
            self.screen.blit(self.label, [WIN_WIDTH / 1.5, WIN_HEIGHT // 1.3])

        elif self.state == 'GAME OVER':
            # фон
            self.screen.blit(pygame.image.load("background.png").convert(), [0, 0])
            self.label = FONT.render('GAME OVER', True, RED)
            self.screen.blit(self.label, [WIN_WIDTH / 2.5, WIN_HEIGHT / 1.3])

    # Обновление текущего состояния игры
    def update(self):

        if self.state == 'GAME':
            self.time += 1
            self.all_sprite_list.update()
            self.top_panel.update(berry=self.player.score, lives=self.player.lives)

            # Проверка стокновения игрока с противником:
            if pygame.sprite.spritecollideany(self.player, self.enemy_list):
                if self.time - self.hit_time > FPS:
                    self.player.lives -= 1
                    self.hit_time = self.time
                self.player.change_x = -5

            if self.player.rect.x > WIN_WIDTH - 71 and self.player.rect.y > WIN_HEIGHT - 71:
                self.state = 'FINISH'

            if self.player.lives <= 0:
                self.state = 'GAME OVER'

        elif self.state == 'SETTINGS':

            self.settings_menu.update()
        else:
            self.main_menu.update()

    def run(self):
        done = False
        # Запуск главного игрового цикла:
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                self.handle_states(event)

            # Если игрок приближается к правому краю экрана, мир смещается влево
            if self.player.rect.right >= 500 and abs(self.shift) < self.game_width - WIN_WIDTH:
                diff = self.player.rect.right - 500
                self.player.rect.right = 500
                self.shift_world(-diff)

            # Если игрок приближается к левому краю экрана, мир смещается вправо
            if self.player.rect.left <= 120 and abs(self.shift) > 0:
                diff = 120 - self.player.rect.left
                self.player.rect.left = 120
                self.shift_world(diff)

            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()


game = Game()
game.run()
