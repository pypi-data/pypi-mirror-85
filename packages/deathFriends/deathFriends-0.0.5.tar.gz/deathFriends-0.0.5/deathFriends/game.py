import pygame as pg
import sys
from os import path

from .player import Player
from .wall import Wall
from .tilemap import Map
from .camera import Camera
from .settings import *
from .mapAll import map1
from .bullet import Bullet

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(100, 100)
        self.load_data()

    def load_data(self):

        game_folder = path.dirname(__file__)

        image_folder = path.join(game_folder, 'sprints')
        text_folder = path.join(game_folder, 'fonts')

        self.backgroudMenu_img = pg.image.load(
            path.join(image_folder, BACKGROUNDMENU))

        self.player_img = pg.image.load(
            path.join(image_folder, PLAYER_IMG)).convert_alpha()

        self.wall_img = pg.image.load(
            path.join(image_folder, WALL_IMG)).convert_alpha()

        self.bullet_img = pg.image.load(
            path.join(image_folder, BULLET_IMG)).convert_alpha()

        self.titleFont = pg.font.Font(path.join(text_folder, TILEFONT), 45)

        self.fontMenu = pg.font.Font(path.join(text_folder, MENUFONT), 35)

        self.map = Map(map1)

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        for line, dataLine in enumerate(self.map.map):
            for row, dataRow in enumerate(dataLine):
                if(dataRow == '1'):
                    Wall(self, row, line)
                if(dataRow == 'P'):
                    self.player = Player(self, row, line)
        self.camera = Camera(self.map.width, self.map.height)

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)

    def draw(self):
        self.screen.fill(BGCOLOR)
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()

    def show_start_screen(self):
        while(True):
            for e in pg.event.get():
                if(e.type == pg.QUIT):
                    self.quit()
            self.screen.blit(self.backgroudMenu_img, (0, 0))

            # Titulo do jogo
            self.textObjetc('death friends', self.titleFont, 5)

            # Botoes
            self.textObjetc('Iniciar jogo', self.fontMenu, 2.5)
            self.textObjetc('Configurações', self.fontMenu, 2)
            self.textObjetc('Sair', self.fontMenu, 1.7)

            mousePosition = pg.mouse.get_pos()
            click = pg.mouse.get_pressed()
            if(400 < mousePosition[0] < 565 and 245 < mousePosition[1] < 275) and click[0] == 1:
                return 1
            if(370 < mousePosition[0] < 585 and 305 < mousePosition[1] < 330 and click[0] == 1):
                self.quit()
            if(450 < mousePosition[0] < 510 and 360 < mousePosition[1] < 385 and click[0] == 1):
                self.quit()

            self.clock.tick(FPS)
            pg.display.flip()

    def show_go_screen(self):
        pass

    def textObjetc(self, text, font, location):
        textSurf = font.render(text, True, WHITE)
        textReact = textSurf.get_rect()
        textReact.center = (int(WIDTH/2), int(HEIGHT/location))
        self.screen.blit(textSurf, textReact)
