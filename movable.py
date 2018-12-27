"""A movable is a tile that can move (ghost or pacman)"""

from utils import *

def voidnonblocking(fn):
    """This decorator allows movables to got outside of the map (anything
    outside of the map is just space)"""
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except IndexError as e:
            return SPACE
    return wrapper

class Movable:

    # think of it as speed = 1 / 10
    # frames per tiles
    fpt = 10

    def __init__(self, x, y, wdx, wdy, tiles):
        # x and y are the tile position
        self.x, self.y = x, y
        # dx and dy are the direction the pacman is moving towards
        self.dx, self.dy = wdx, wdy
        # wdx and wdy are the wanted dx and dy.
        # None means nothing is wanted, 0 means they want to stop
        self.wdx, self.wdy = None, None
        # ax and ay are the absolute position (in pixel)
        # note: this is the top-left corner of the image
        self.ax, self.ay = x * TILE_SIZE, y * TILE_SIZE

        self.ax, self.ay = x * TILE_SIZE, y * TILE_SIZE

        # the representation of the map
        self.tiles = tiles

    @property
    def pos(self):
        return self.x, self.y
    
    def tile(self):
        """returns the representation of the current tile"""
        if self.y < 0:
            raise IndexError(f"Index should be positive, got {self.y}")
        if self.x < 0:
            raise IndexError(f"Index should be positive, got {self.x}")
        return self.tiles[self.y][self.x]

    @voidnonblocking
    def next_tile(self):
        """returns the next tile's representation the pacman is going to be on
        if it kept going in this direction"""
        if self.y + self.dy < 0:
            raise IndexError(f"Index should be positive, got {self.y + self.dy}")
        if self.x + self.dx < 0:
            raise IndexError(f"Index should be positive, got {self.x + self.dx}")
        return self.tiles[self.y + self.dy][self.x + self.dx]

    @voidnonblocking
    def next_wanted_tile(self):
        """Same as next tile, but using self.wd[xy]"""
        if self.y + self.wdy < 0:
            raise IndexError(f"Index should be positive, got {self.y + self.wdy}")
        if self.x + self.wdx < 0:
            raise IndexError(f"Index should be positive, got {self.x + self.wdx}")
        return self.tiles[self.y + self.wdy][self.x + self.wdx]

    def update(self, ufc):
        rest = ufc % self.fpt

        if rest == 0:
            self.x += self.dx
            self.y += self.dy
            if self.dx or self.dy:
                EventManager.emit('movable reached tile', self)
            if is_blocking(self.next_tile()):
                self.dx = self.dy = 0

        self.ax = int(self.x * TILE_SIZE + self.dx * TILE_SIZE * rest / self.fpt)
        self.ay = int(self.y * TILE_SIZE + self.dy * TILE_SIZE * rest / self.fpt)

        if (self.wdx or self.wdy) and rest == 0 \
            and not is_blocking(self.next_wanted_tile()) and self.tile() != TELEPORT:
            self.dx, self.dy = self.wdx, self.wdy
            self.wdx = self.wdy = None

        if self.wdx == self.wdy == 0 and rest == 0:
            self.dx = self.dy = 0
            self.wdx = self.wdy = None
        return rest