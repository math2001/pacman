"""The pacman is a simple interface that simply emits an event 'pacman-turn'
with (x, y) where x and y are -1, 0 or 1, with exactly one 0. It's just to give
the direction"""

import pygame
from pygame.locals import *
from utils import *
import fractions

def abs(n):
	return n if n > 0 else -n

class Pacman:

	# think of it as speed = 1 / 10
	# frames per tiles
	fpt = 10

	def __init__(self, x, y, dx, dy, tiles):
		# x and y are the tile position
		self.x, self.y = x, y
		# dx and dy are the direction the pacman is moving towards
		self.dx, self.dy = dx, dy
		# wdx and wdy are the wanted dx and dy.
		self.wdx, self.wdy = 0, 0
		# ax and ay are the absolute position (in pixel)
		# note: this is the top-left corner of the image
		self.ax, self.ay = x * TILE_SIZE, y * TILE_SIZE

		# the representation of the map
		self.tiles = tiles
		self.just_tp = False

		self.frame_count = 0

	def handle_keydown(self, e):
		if e.key in (K_UP, K_w):
			self.wdx, self.wdy = 0, -1
		elif e.key in (K_DOWN, K_s):
			self.wdx, self.wdy = 0, 1
		elif e.key in (K_LEFT, K_a):
			self.wdx, self.wdy = -1, 0
		elif e.key in (K_RIGHT, K_d):
			self.wdx, self.wdy = 1, 0

	def tile(self):
		"""returns the representation of the current tile"""
		if self.y < 0:
			raise IndexError(f"Index should be positive, got {self.y}")
		if self.x < 0:
			raise IndexError(f"Index should be positive, got {self.x}")
		return self.tiles[self.y][self.x]

	def next_tile(self):
		"""returns the next tile's representation the pacman is going to be on
		if it kept going in this direction"""
		if self.y + self.dy < 0:
			raise IndexError(f"Index should be positive, got {self.y + self.dy}")
		if self.x + self.dx < 0:
			raise IndexError(f"Index should be positive, got {self.x + self.dx}")
		return self.tiles[self.y + self.dy][self.x + self.dx]

	def next_wanted_tile(self):
		"""Same as next tile, but using self.wd[xy]"""
		if self.y + self.wdy < 0:
			raise IndexError(f"Index should be positive, got {self.y + self.wdy}")
		if self.x + self.wdx < 0:
			raise IndexError(f"Index should be positive, got {self.x + self.wdx}")
		return self.tiles[self.y + self.wdy][self.x + self.wdx]

	def update(self):
		self.frame_count += 1
		rest = self.frame_count % Pacman.fpt
		# we are exactly on a tale
		if rest == 0:
			self.x += self.dx
			self.y += self.dy

		if self.tile() == 't':
			if self.just_tp:
				self.just_tp = False
			elif rest == 0:
				# teleport to the other gate
				if self.tiles.teleports[0] == (self.x, self.y):
					self.x, self.y = self.tiles.teleports[1]
				else:
					self.x, self.y = self.tiles.teleports[0]
				self.just_tp = True

		elif is_blocking(self.next_tile()):
			self.dx = self.dy = 0

		# set the absolute position
		self.ay = int(self.y * TILE_SIZE + self.dy * TILE_SIZE * rest / Pacman.fpt)
		self.ax = int(self.x * TILE_SIZE + self.dx * TILE_SIZE * rest / Pacman.fpt)

		if self.wdy + self.wdx != 0 and rest == 0 \
			and not is_blocking(self.next_wanted_tile()):
			self.dx, self.dy = self.wdx, self.wdy
			self.wdx = self.wdy = 0

	def render(self, surface):
		center = (self.ax + TILE_SIZE // 2,
				  self.ay + TILE_SIZE // 2)
		pygame.draw.circle(surface, pygame.Color('yellow'), center,
						   TILE_SIZE // 2)