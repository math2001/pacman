import pygame
from Scene import Scene
from utils import *
from pacman import Pacman

class Game(Scene):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.debug = True
		self.tiles = []

		self.height = 0
		self.width = 0
		self.pacman = None

		with open(f'plans/original.txt') as fp:
			dx, dy = intall(next(fp).split(','))
			for line in fp:
				index = line.find('s')
				if index != -1:
					self.pacman = Pacman(index, self.height, dx, dy, self.tiles)
				self.height += 1
				self.tiles.append(list(line.strip()))
		if not self.pacman:
			raise ValueError("tiles doesn't have a starting position ('s')")

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