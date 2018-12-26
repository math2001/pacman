import pygame
from Scene import Scene
from utils import *
from pacman import Pacman
from ghost import Ghost

class Game(Scene):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.debug = True
		self.tiles = Tiles()
		self.tiles.teleports = []

		self.ghosts = []

		self.pacman = None
		self.paused = False

		ghost_colors = {'r': 'red', 'c': 'cyan', 'p': 'pink', 'y': 'yellow'}

		with open(f'plans/original.txt') as fo:
			dx, dy = intall(next(fo).split(','))
			for y, line in enumerate(fo):
				line = line.strip()
				self.tiles.append(list(line))
				for x, char in enumerate(line):
					if char == TELEPORT:
						self.tiles.teleports.append((x, y))
					elif char == START:
						self.pacman = Pacman(x, y, dx, dy, self.tiles)
					elif char in ghost_colors:
						self.ghosts.append(Ghost(x, y, 0, 0, self.tiles,
						                         ghost_colors[char]))
					elif char not in (SPACE, WALL):
						raise ValueError(f"Invalid char {char!r} at {x, y}")

		if len(self.tiles.teleports) not in (0, 2):
			raise ValueError("tiles should have 0 or 2 teleport points, got "
							 f"{len(self.tiles.teleports)}")
		if not self.pacman:
			raise ValueError(f"tiles doesn't have a starting position ({START!r})")

		self.set_mode((self.tiles.width * TILE_SIZE,
					   self.tiles.height * TILE_SIZE))

		EventManager.on('toggle-pause-game', self.togglepause)

	def togglepause(self):
		self.paused = not self.paused

	def handle_event(self, e):
		super().handle_event(e)
		if e.type == pygame.KEYDOWN:
			if e.key == pygame.K_SPACE:
				self.paused = not self.paused
			elif e.key == pygame.K_n and self.paused:
				# go frame by frame
				self.paused = False
				self.update()
				self.paused = True
			self.pacman.handle_keydown(e)

	def update(self):
		if self.paused:
			return
		self.pacman.update()
		for ghost in self.ghosts:
			ghost.update()

	def render(self, surface):
		# render the maze
		# this can be heavily optimized. It can be rendered in __init__ on a 
		# surface and then just blited.
		for y, row in enumerate(self.tiles):
			for x, char in enumerate(row):
				if char == WALL:
					rect = pygame.Rect((x * TILE_SIZE, y * TILE_SIZE), (TILE_SIZE, TILE_SIZE))
					pygame.draw.rect(surface, pygame.Color('gray'), rect)

		self.pacman.render(surface)
		for ghost in self.ghosts:
			ghost.render(surface)