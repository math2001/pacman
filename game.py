import pygame
from Scene import Scene
from utils import *
from pacman import Pacman
from ghost import Ghost
import strategies.ghosts
import strategies.pacman

ghost_strategies = {
    "shortest path": strategies.ghosts.ShortestPath
}

pacman_strategies = {
    "user": strategies.pacman.User
}

class Game(Scene):

    def __init__(self, ghost_strategy, pacman_strategy):
        self.tiles = Tiles()
        self.tiles.teleports = []

        self.ghosts = []

        self.dots = []

        self.pacman = None
        self.paused = False

        # upate frame count (not updated when paused)
        self.ufc = 0
        # render frame count (always updated)
        self.rfc = 0

        # read tile's map and create corresponding objects

        ghost_colors = {'r': 'red', 'c': 'cyan', 'p': 'pink', 'y': 'yellow'}

        with open(f'plans/original.txt') as fo:
            dx, dy = intall(next(fo).split(','))
            for y, line in enumerate(fo):
                fline = []
                for x, char in enumerate(line.strip()):
                    if char == TELEPORT:
                        self.tiles.teleports.append((x, y))
                        fline.append(TELEPORT)
                    elif char == START:
                        self.pacman = Pacman(x, y, dx, dy, self.tiles)
                        fline.append(SPACE)
                    elif char in ghost_colors:
                        self.ghosts.append(Ghost(x, y, 0, 0, self.tiles,
                                                 ghost_colors[char]))
                        fline.append(DOT)
                    elif char not in (SPACE, DOT, WALL):
                        raise ValueError(f"Invalid char {char!r} at {x, y}")
                    else:
                        fline.append(char)
                self.tiles.append(fline)

        # a few safety checks
        if len(self.tiles.teleports) not in (0, 2):
            raise ValueError("tiles should have 0 or 2 teleport points, got "
                             f"{len(self.tiles.teleports)}")
        if not self.pacman:
            raise ValueError(f"tiles doesn't have a starting position ({START!r})")

        EventManager.emit("set mode", (self.tiles.width * TILE_SIZE,
                                       self.tiles.height * TILE_SIZE))

        EventManager.on('toggle-pause-game', self.togglepause)
        EventManager.on('ghost turn', self.ghostturn)
        EventManager.on('pacman turn', self.pacmanturn)

        # instantiate the strategies

        args = self.tiles, self.pacman, self.ghosts
        self.ghost_strategy = ghost_strategies[ghost_strategy](*args)
        self.pacman_strategy = pacman_strategies[pacman_strategy](*args)

    def togglepause(self):
        self.paused = not self.paused

    def ghostturn(self, color, direction):
        """Makes the ghost turn"""
        for ghost in self.ghosts:
            if ghost.color == color:
                ghost.wdx, ghost.wdy = direction
                return
        raise ValueError(f"There is no ghost with color {color!r}")

    def pacmanturn(self, direction):
        self.pacman.wdx, self.pacman.wdy = direction

    def handle_event(self, e):
        super().handle_event(e)
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_SPACE:
                self.togglepause()
            elif e.key == pygame.K_n and self.paused:
                # go frame by frame
                self.paused = False
                self.update()
                self.paused = True
        self.pacman_strategy.handle_event(e)
        self.ghost_strategy.handle_event(e)

    def update(self):
        if self.paused:
            return
        self.ufc += 1
        for ghost in self.ghosts:
            ghost.update(self.ufc)
        self.pacman_strategy.update(self.ufc)
        self.ghost_strategy.update(self.ufc)
        self.pacman.update(self.ufc)

    def render(self, surface):
        self.rfc += 1
        # render the maze
        # this can be heavily optimized. It can be rendered in __init__ on a 
        # surface and then just blited.
        for y, row in enumerate(self.tiles):
            for x, char in enumerate(row):
                if char == WALL:
                    rect = pygame.Rect((x * TILE_SIZE, y * TILE_SIZE), (TILE_SIZE, TILE_SIZE))
                    pygame.draw.rect(surface, pygame.Color('gray'), rect)
                if char == DOT:
                    center = (x * TILE_SIZE + TILE_SIZE // 2,
                              y * TILE_SIZE + TILE_SIZE // 2)
                    pygame.draw.circle(surface, WHITE, center, TILE_SIZE // 10)

        self.pacman_strategy.render(surface, self.rfc)
        self.ghost_strategy.render(surface, self.rfc)

        self.pacman.render(surface, self.rfc)
        for ghost in self.ghosts:
            ghost.render(surface, self.rfc)
