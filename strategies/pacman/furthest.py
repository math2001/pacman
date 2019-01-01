from itertools import chain
from strategies.strategy import Strategy
from utils import *

DEBUG = True

def oneify(n):
    if n > 0:
        return 1
    elif n < 0:
        return -1
    return 0

class Furthest(Strategy):

    """ Go as far as possible from the ghost.
    It's extremely dumb (and very painful to watch) for a few different reason

    1. It only takes into consideration the *average* ghost
    2. It is NOT maze aware. It doesn't take into consideration the wall

    We just hope that if we keep doing this long enough, it will eventually
    eat everything.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        EventManager.on('movable reached tile', self.notify_pacman)

        self.average_ghost = None

    def notify_pacman(self, movable):
        """ The algorithm is in essence quite simple.
        
        1. determine the average ghost position
        2. determine how close it is to the pacman
        3. prioritze the 4 different possible direction based on those 2
           distances (x and y).
        """

        if classname(movable) != 'Pacman':
            return

        # A simple average of the ghost position
        x, y = 0, 0
        for ghost in self.ghosts:
            x += ghost.x
            y += ghost.y

        self.average_ghost = x, y = x // len(self.ghosts), y // len(self.ghosts)

        # get the position relative to the pacman.
        # ie. 0 means the ghost is on the pacman. The bigger x and y are, the
        # better it is for the pacman.
        x, y = self.pacman.x - x, self.pacman.y - y

        # based on the ghost's weight position, we can rank the 4 direction
        # we can go (up, down, left, right). Note that this strategy doesn't
        # involve waiting. We are constantly moving.

        # remember that a direction is just (x, y) where x and y can only be 0
        # or 1. In this strategy, x and y are always different.

        opposite = [
            (oneify(x), 0),
            (0, oneify(y)),
        ]
        # by default, we consider that moving away in the opposite x direction
        # is better than moving in the y opposite direction. But, if the x
        # distance of the average ghost is bigger than the y distance, it means
        # that it isn't as urgent. Therefore, y is prioritized.
        if abs(x) > abs(y):
            opposite = reversed(opposite)

        # in case we can't move away from the average ghost position, we try 
        # to go in the direction that isn't as bad. This means that we go in
        # the direction that is the farthest from the average ghost
        towards = [
            (-oneify(x), 0),
            (0, -oneify(y)),
        ]

        if abs(x) < abs(y):
            towards = reversed(towards)

        # ranked direction. The first one is the best one
        directions = list(chain(opposite, towards))

        for rank, (x, y) in enumerate(directions):
            if not is_blocking(self.tiles[self.pacman.y+y][self.pacman.x+x],
                               is_pacman=True):
                EventManager.emit('pacman turn', (x, y))
                return
        print('not changing', self.pacman.x, self.pacman.y)

    def render(self, surface, rect, rfc):
        if self.average_ghost is None or not DEBUG:
            return
        rect = pygame.Rect((self.average_ghost[0] * TILE_SIZE,
                            self.average_ghost[1] * TILE_SIZE),
                           (TILE_SIZE, TILE_SIZE))
        pygame.draw.rect(surface, RED, rect)