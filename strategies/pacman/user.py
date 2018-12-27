from strategies import Strategy
from utils import EventManager
from pygame.locals import *

class User(Strategy):

    """ The user controls the pacman """

    def handle_event(self, e):
        if e.type == KEYDOWN:
            if e.key in (K_UP, K_w):
                EventManager.emit('pacman turn', (0, -1))
            elif e.key in (K_DOWN, K_s):
                EventManager.emit('pacman turn', (0, 1))
            elif e.key in (K_LEFT, K_a):
                EventManager.emit('pacman turn', (-1, 0))
            elif e.key in (K_RIGHT, K_d):
                EventManager.emit('pacman turn', (1, 0))
