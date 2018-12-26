"""The pacman is a simple interface that simply emits an event 'pacman-turn'
with (x, y) where x and y are -1, 0 or 1, with exactly one 0. It's just to give
the direction"""

import pygame
from pygame.locals import *
from utils import *
from movable import Movable

class Pacman(Movable):

	# think of it as speed = 1 / 10
	# frames per tiles
	fpt = 5

	def __init__(self, x, y, wdx, wdy, tiles):
		super().__init__(x, y, wdx, wdy, tiles)

		self.just_tp = False

	def handle_keydown(self, e):
		if e.key in (K_UP, K_w):
			self.wdx, self.wdy = 0, -1
		elif e.key in (K_DOWN, K_s):
			self.wdx, self.wdy = 0, 1
		elif e.key in (K_LEFT, K_a):
			self.wdx, self.wdy = -1, 0
		elif e.key in (K_RIGHT, K_d):
			self.wdx, self.wdy = 1, 0
	
	def update(self):
		rest = super().update()
		if self.tile() == TELEPORT:
			if self.just_tp:
				self.just_tp = False
			elif rest == 0:
				# teleport to the other gate
				if self.tiles.teleports[0] == (self.x, self.y):
					self.x, self.y = self.tiles.teleports[1]
				else:
					self.x, self.y = self.tiles.teleports[0]
				self.just_tp = True

	def render(self, surface):
		center = (self.ax + TILE_SIZE // 2,
				  self.ay + TILE_SIZE // 2)
		pygame.draw.circle(surface, pygame.Color('yellow'), center,
						   TILE_SIZE // 2)