import pygame
from Scene import Scene
from utils import *
from pacman import Pacman

class Game(Scene):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.debug = True
		self.tiles = Tiles()
		self.tiles.teleports = []

		self.pacman = None

		with open(f'plans/original.txt') as fp:
			dx, dy = intall(next(fp).split(','))
			for line in fp:
				index = line.find(TELEPORT)
				while index != -1:
					self.tiles.teleports.append((index, self.tiles.height))
					index = line.find(TELEPORT, index + 1)
				index = line.find(START)
				if index != -1:
					# note that height isn't the final height yet
					self.pacman = Pacman(index, self.tiles.height, dx, dy,
										 self.tiles)
				self.tiles.append(list(line.strip()))

		if len(self.tiles.teleports) not in (0, 2):
			raise ValueError("tiles should have 0 or 2 teleport points, got "
							 f"{len(self.tiles.teleports)}")
		if not self.pacman:
			raise ValueError(f"tiles doesn't have a starting position ({START!r})")

		self.set_mode((self.tiles.width * TILE_SIZE,
					   self.tiles.height * TILE_SIZE))

	def handle_event(self, e):
		super().handle_event(e)
		if e.type == pygame.KEYDOWN:
			self.pacman.handle_keydown(e)

	def update(self):
		self.pacman.update()

	def render(self, surface):
		# render the maze
		# this can be heavily optimized. It can be rendered in __init__ on a 
		# surface and then just blited.
		for y, row in enumerate(self.tiles):
			for x, char in enumerate(row):
				if char == WALL:
					rect = pygame.Rect((x * TILE_SIZE, y * TILE_SIZE), (20, 20))
					pygame.draw.rect(surface, pygame.Color('gray'), rect)

		self.pacman.render(surface)