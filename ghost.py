import pygame
from movable import Movable
from utils import *

class Ghost(Movable):

    def __init__(self, x, y, wdx, wdy, tiles, color):
        super().__init__(x, y, wdx, wdy, tiles)
        self.color = pygame.Color(color) if isinstance(color, str) else color

        self.frame_count = 0
        self.angle = 0
        # (scale, direction) the direction is added every x frame to the scale
        self.scale = [1, 0.1]

        # generate ghost image
        self.surf = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        # do the maths, it's the largest diagonal in a square. 0.707 = 1/sqrt(2)
        side = 0.707 * TILE_SIZE
        rect = pygame.Rect((0, 0), (side, side))
        rect.center = self.surf.get_rect().center
        pygame.draw.rect(self.surf, self.color, rect)

    def update(self):
        pass

    def render(self, surface):
        self.frame_count += 1
        center = (self.ax + TILE_SIZE // 2,
                  self.ay + TILE_SIZE // 2)

        if self.frame_count % 2 == 0:
            self.angle += 10
            self.angle %= 360
        if self.frame_count % 3 == 0:
            self.scale[0] += self.scale[1]
            if self.scale[0] > 1.2 or self.scale[0] < .8:
                self.scale[1] = -self.scale[1]


        surf = pygame.transform.rotozoom(self.surf, self.angle, self.scale[0])

        surface.blit(surf, surf.get_rect(center=center))