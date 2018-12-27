from pygame.display import get_surface
import pygame.freetype
import warnings

TILE_SIZE = 20 # pixels per tile
WALL = '0'
SPACE = ' '
DOT = '.'
TELEPORT = 't'
START = 's'

WHITE = 255, 255, 255
BLACK = 0  , 0  ,   0
PINK = pygame.Color('pink')
RED = pygame.Color('red')

def is_blocking(char, is_pacman=False):
    # also block on teleport gate if not the pacman
    return char in (WALL, ) + (() if is_pacman else (TELEPORT, ))

def classname(obj):
    return obj.__class__.__name__

pygame.freetype.init()
font = pygame.freetype.SysFont("Fira Mono", 10)

def intall(arr):
    return [int(n) for n in arr]

class Screen:

    @classmethod
    def update(cls):
        cls.surface = get_surface()
        cls.rect = cls.surface.get_rect()

class EventManager:

    events = {}

    @classmethod
    def on(cls, event, func):
        cls.events.setdefault(event, []).append(func)
    
    @classmethod
    def emit(cls, event, *args, **kwargs):
        try:
            cbs = cls.events[event]
        except KeyError:
            warnings.warn(f"Emitting event {event!r} that hasn't got any "
                          f"listener. Only know about {list(cls.events.keys())}")

        for cb in cbs:
            cb(*args, **kwargs)

class Tiles(list):

    @property
    def width(self):
        return len(self[0])
    
    @property
    def height(self):
        return len(self)
    
    def __getitem__(self, i):
        if i < 0:
            raise IndexError(f"Index should be positive, got {i}")
        return super().__getitem__(i)