import pygame
from scene import Scene
from utils import *
from pacman import Pacman
from ghost import Ghost
from strategies import strategies

# TODO: put countdown at the beginning of the game

class Game(Scene):

    def __init__(self, pacman_strategy, ghosts_strategy):
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

        self.score = dotdict(current=0, max=0, center=None)

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
                        self.score.max += 1
                    elif char == DOT:
                        fline.append(char)
                        self.score.max += 1
                    elif char == SCORE:
                        self.score.center = (x * TILE_SIZE,
                                             y * TILE_SIZE + TILE_SIZE // 2)
                        fline.append(SPACE)
                    elif char not in (SPACE, WALL):
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
        EventManager.on('movable reached tile', self.eatdot)

        # instantiate the strategies
        args = self.tiles, self.pacman, self.ghosts
        self.strategy = dotdict(
            pacman=strategies.pacman[pacman_strategy](*args),
            ghosts=strategies.ghosts[ghosts_strategy](*args),
        )

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
        self.strategy.pacman.handle_event(e)
        self.strategy.ghosts.handle_event(e)

    def update(self):
        if self.paused:
            return
        self.ufc += 1

        self.pacman.update(self.ufc)

        # TODO: only check when a movable has reached a tile
        for ghost in self.ghosts:
            ghost.update(self.ufc)
            if ghost.collides(self.pacman):
                self.end(winner='ghosts')

        # TODO: only check when a movable has reached a tile
        if self.score.current == self.score.max:
            self.end(winner='pacman')

        self.strategy.pacman.update(self.ufc)
        self.strategy.ghosts.update(self.ufc)

    def render(self, surface, rect):
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

        with fontedit(self.fonts.arcade, size=30) as font:
            text = f'{self.score.max - self.score.current}'
            r = font.get_rect(text)
            r.center = self.score.center
            font.render_to(surface, r, text)

        self.strategy.pacman.render(surface, rect, self.rfc)
        self.strategy.ghosts.render(surface, rect, self.rfc)

        self.pacman.render(surface, self.rfc)
        for ghost in self.ghosts:
            ghost.render(surface, self.rfc)

    def done(self):
        EventManager.off('toggle-pause-game', self.togglepause)
        EventManager.off('ghost turn', self.ghostturn)
        EventManager.off('pacman turn', self.pacmanturn)
        EventManager.off('movable reached tile', self.eatdot)

        self.strategy.pacman.done()
        self.strategy.ghosts.done()

    def togglepause(self):
        self.paused = not self.paused

    def ghostturn(self, color, direction):
        """Makes the ghost turn"""
        for ghost in self.ghosts:
            if ghost.color == color:
                ghost.wdx, ghost.wdy = direction
                return
        raise ValueError(f"There is no ghost with color {color!r}")

    def eatdot(self, movable):
        if not isinstance(movable, Pacman):
            return
        x, y = movable.pos
        if self.tiles[y][x] == DOT:
            self.tiles[y][x] = SPACE
            self.score.current += 1

    def pacmanturn(self, direction):
        self.pacman.wdx, self.pacman.wdy = direction

    def end(self, winner):
        # retrieve the name of the pacman and ghost strategy
        for name, strategy in strategies.pacman.items():
            if isinstance(self.strategy.pacman, strategy):
                sp = name
                break
        for name, strategy in strategies.ghosts.items():
            if isinstance(self.strategy.ghosts, strategy):
                sg = name
                break

        EventManager.emit('switch scene', 'end', winner, sp, sg)
