import pygame
from pygame.locals import *
from utils import *
from movable import Movable

DEBUG_INFO = 'position'

class Pacman(Movable):

    """Pacman is basically a regular movable, except it can teleport"""

    fpt = 5

    def __init__(self, x, y, wdx, wdy, tiles):
        super().__init__(x, y, wdx, wdy, tiles)

        self.just_tp = False

    def update(self, ufc):
        rest = super().update(ufc)
        if self.tile() == TELEPORT:
            if self.just_tp:
                self.just_tp = False
            elif rest == 0:
                # teleport to the other gate
                if self.tiles.teleports[0] == (self.x, self.y):
                    self.x, self.y = self.tiles.teleports[1]
                else:
                    self.x, self.y = self.tiles.teleports[0]
                self.just_tp = True

    def render(self, surface, rfc):
        center = (self.ax + TILE_SIZE // 2,
                  self.ay + TILE_SIZE // 2)
        pygame.draw.circle(surface, pygame.Color('yellow'), center,
                           TILE_SIZE // 2)
        if DEBUG_INFO == 'position':
            self.show_debug(surface, self.pos)