import pygame as pg
from .settings import *
from .tilemap import collide_hit_rect
from .bullet import Bullet
vect = pg.math.Vector2


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_img
        self.rect = self.image.get_rect()
        self.hit_rect = PLAYER_RECT
        self.hit_rect.center = self.rect.center
        self.vel = vect(0, 0)
        self.pos = vect(x, y)*TILESIZE
        self.rot = 0
        self.last_shot = 0

    def get_keys(self):
        self.rot_speed = 0
        self.vel = vect(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.rot_speed = PLAYER_ROT
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.rot_speed = -PLAYER_ROT
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel = vect(PLAYER_SPEED, 0).rotate(-self.rot)
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel = vect(-PLAYER_SPEED, 0).rotate(-self.rot)
        if(keys[pg.K_SPACE]):
            now = pg.time.get_ticks()
            if(now - self.last_shot > 150):
                self.last_shot = now
                dire = vect(1, 0).rotate(-self.rot)
                pos = self.pos + vect(30,10).rotate(-self.rot)
                Bullet(self.game,pos,dire)

    def collide_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False,collide_hit_rect)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.hit_rect.width / 2
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right + self.hit_rect.width / 2
                self.vel.x = 0
                self.hit_rect.centerx = self.pos.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False,collide_hit_rect)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.hit_rect.height / 2
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom + self.hit_rect.width / 2
                self.vel.y = 0
                self.hit_rect.centery = self.pos.y

    def update(self):
        self.get_keys()
        self.rot = (self.rot + self.rot_speed * self.game.dt) % 360
        self.image = pg.transform.rotate(self.game.player_img,self.rot)
        self.rect = self.image.get_rect()
        self.rect.center =  self.pos
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        self.collide_walls('x')
        self.hit_rect.centery = self.pos.y
        self.collide_walls('y')
