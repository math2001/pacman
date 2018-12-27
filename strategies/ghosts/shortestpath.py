from strategies.strategy import Strategy
import pygame.draw
from utils import *

DEBUG = 'none'

def around(x, y):
    yield x, y
    yield x-1, y
    yield x+1, y
    yield x, y-1
    yield x, y+1

class ShortestPath(Strategy):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.map_distances(self.pacman)
        for ghost in self.ghosts:
            self.__update_ghost(ghost)

        EventManager.on('movable reached tile', self.notify_ghosts)

    def __update_ghost(self, ghost):
        closer = min(around(*(ghost.x, ghost.y)),
                     key=lambda pos: self.distances[pos[1]][pos[0]])
        EventManager.emit("ghost turn", ghost.color, (
            closer[0] - ghost.x,
            closer[1] - ghost.y
        ))

    def notify_ghosts(self, movable):
        if movable.__class__.__name__ == 'Pacman':
            self.map_distances(movable)
            for ghost in self.ghosts:
                self.__update_ghost(ghost)
        else:
            self.__update_ghost(movable)

    def map_distances(self, movable):
        self.distances = [[float('inf') for _ in range(self.tiles.width)] \
                          for _ in range(self.tiles.height)]

        def map(x, y, distance):
            self.distances[y][x] = distance
            if y > 0 and not is_blocking(self.tiles[y-1][x]) \
                and self.distances[y-1][x] > distance + 1:
                map(x, y - 1, distance + 1)

            if y < self.tiles.height - 1 and not is_blocking(self.tiles[y+1][x]) \
                and self.distances[y+1][x] > distance + 1:
                map(x, y + 1, distance + 1)

            if x > 0 and not is_blocking(self.tiles[y][x-1]) \
                and self.distances[y][x-1] > distance + 1:
                map(x - 1, y, distance + 1)

            if x < self.tiles.width - 1 and not is_blocking(self.tiles[y][x+1]) \
                and self.distances[y][x+1] > distance + 1:
                map(x + 1, y, distance + 1)

        map(movable.x, movable.y, 0)

    def render(self, surface, ufc):
        for y, row in enumerate(self.tiles):
            for x, char in enumerate(row):
                if not is_blocking(char) and self.distances:
                    if DEBUG == 'color':
                        if self.distances[y][x] == float('inf'):
                            color = (100, 50, 50)
                        else:
                            color = (self.distances[y][x] * 5 % 255, ) * 3
                        pygame.draw.rect(surface, color,
                            pygame.Rect((x * TILE_SIZE, y * TILE_SIZE),
                                        (TILE_SIZE, TILE_SIZE)))
                    elif DEBUG == 'numbers':
                        coef = str(self.distances[y][x])
                        rect = font.get_rect(coef)
                        rect.center = (x * TILE_SIZE + TILE_SIZE // 2,
                                       y * TILE_SIZE + TILE_SIZE // 2)
                        font.render_to(surface, rect, coef, WHITE)
