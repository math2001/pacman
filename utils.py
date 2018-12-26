from pygame.display import get_surface

TILE_SIZE = 20 # pixels per tile
WALL = '0'
SPACE = ' '
TELEPORT = 't'
START = 's'

is_blocking = lambda c: c in (WALL, )

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
        for func in cls.events.get(event, ()):
            func(*args, **kwargs)