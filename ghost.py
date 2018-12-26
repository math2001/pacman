import pygame
from movable import Movable
from utils import *

class Ghost(Movable):

    def __init__(self, x, y, wdx, wdy, tiles, color):
        super().__init__(x, y, wdx, wdy, tiles)
        self.color = pygame.Color(color) if isinstance(color, str) else color

    def update(self):
        pass

    def render(self, surface):
        center = (
            self.ax + TILE_SIZE // 2,
            self.ay + TILE_SIZE // 2
        )
        pygame.draw.circle(surface, self.color, center, TILE_SIZE // 2)