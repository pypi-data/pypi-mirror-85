import pygame as pg
from os import path
from .settings import *

def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)
class Map():
    def __init__(self, mapOne):
        self.map = []
        for x in range(len(mapOne)):
            mapLine=[]
            for i in mapOne[x]:
                mapLine.append(i)
            self.map.append(mapLine)
        self.tilewidth = len(self.map[0])
        self.tileheight = len(self.map)
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE
