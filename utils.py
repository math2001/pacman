import pygame
import warnings
from collections import namedtuple
from contextlib import contextmanager
from pygame.display import get_surface

TILE_SIZE = 20 # pixels per tile
WALL = '0'
SPACE = ' '
DOT = '.'
TELEPORT = 't'
START = 's'
SCORE = '1'

WHITE = 255, 255, 255
BLACK = pygame.Color('black')
PINK = pygame.Color('pink')
RED = pygame.Color('red')
BLUE = pygame.Color('blue')

Sprite = namedtuple('Sprite', 'surf rect')

def abs(n):
    return n if n >= 0 else -n

@contextmanager
def fontedit(font, **kwargs):
    """ Applies some settings to a font, and then removes them """
    defaults = {}
    for key in kwargs:
        try:
            defaults[key] = getattr(font, key)
        except AttributeError as e:
            raise AttributeError(f"Invalid parameter for font {key!r}")
        try:
            setattr(font, key, kwargs[key])
        except AttributeError:
            raise AttributeError(f"Could not set {key!r}. Probably read-only")
    yield font
    for key, value in defaults.items():
        try:
            setattr(font, key, value)
        except AttributeError:
            raise AttributeError(f"Could not reset {key!r} to its original value")

class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

def is_blocking(char, is_pacman=False):
    # also block on teleport gate if not the pacman
    return char in (WALL, ) + (() if is_pacman else (TELEPORT, ))

def classname(obj):
    return obj.__class__.__name__

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

    @classmethod
    def off(cls, event, func=None):
        try:
            funcs = cls.events[event]
        except KeyError:
            warnings.warn(f"Removing callback from non-existant event {event!r}")
        if func is None:
            del cls.events[event]
            return
        try:
            funcs.remove(func)
        except ValueError:
            warning.warn(f"Removing non-existant callback from {event!r}. "
                         f"({len(funcs)} other callback))")

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