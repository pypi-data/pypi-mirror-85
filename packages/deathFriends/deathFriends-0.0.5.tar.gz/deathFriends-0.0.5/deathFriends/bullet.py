import pygame as pg
from .settings import *
from random import uniform
vect = pg.math.Vector2
class Bullet(pg.sprite.Sprite):
    def __init__(self,game,pos,dire):
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.bullet_img
        self.rect = self.image.get_rect()
        self.pos = vect(pos)
        self.rect.center = pos
        spread = uniform(-5, 5)
        self.vel = dire.rotate(spread) * BULLET_SPEED
        self.life = pg.time.get_ticks()
    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pg.sprite.spritecollideany(self,self.game.walls):
            self.kill()

        if pg.time.get_ticks() - self.life > BULLET_LIFE:
           self.kill()
