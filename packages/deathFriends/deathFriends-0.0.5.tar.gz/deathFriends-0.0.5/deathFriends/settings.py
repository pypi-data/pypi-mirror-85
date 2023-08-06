import pygame as pg

# cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# game settings

WIDTH = 960
HEIGHT = 640
FPS = 60
TITLE = "Death Friends"
BGCOLOR = DARKGREY
BACKGROUNDMENU='fundo.jpg'

TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE  
GRIDHEIGHT = HEIGHT / TILESIZE  

# Player Settings

PLAYER_SPEED = 250
PLAYER_IMG = 'player.png'
PLAYER_ROT = 200
PLAYER_RECT =  pg.Rect(0, 0, 35, 35)

#Gun Settings

BULLET_IMG =  'gun.png'
BULLET_SPEED = 500
BULLET_LIFE = 1000

#Wall Settings

WALL_IMG='wall.png'

#Fonts Settings

TILEFONT='begok.ttf'
MENUFONT='Prototype.ttf'

