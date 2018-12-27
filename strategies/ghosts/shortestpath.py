from strategies import Strategy
import pygame.draw
from utils import *

class ShortestPath(Strategy):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.distances = None

        EventManager.on('movable reached tile', self.map_distances)

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

    def render(self, surface):
        return
        for y, row in enumerate(self.tiles):
            for x, char in enumerate(row):
                if not is_blocking(char) and self.distances:
                    if self.distances[y][x] == float('inf'):
                        continue
                    color = (self.distances[y][x] * 5 % 255, ) * 3
                    # print(x, y, color, self.distances[y][x])
                    pygame.draw.rect(surface, color,
                        pygame.Rect((x * TILE_SIZE, y * TILE_SIZE),
                                    (TILE_SIZE, TILE_SIZE)))
