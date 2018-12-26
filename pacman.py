"""The pacman is a simple interface that simply emits an event 'pacman-turn'
with (x, y) where x and y are -1, 0 or 1, with exactly one 0. It's just to give
the direction"""

import pygame
from pygame.locals import *
from utils import *

def abs(n):
	return n if n > 0 else -n

class Pacman:

	speed = 5 # pixel per frame

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

	def handle_keydown(self, e):
		if e.key in (K_UP, K_w):
			self.wdx, self.wdy = 0, -1
		elif e.key in (K_DOWN, K_s):
			self.wdx, self.wdy = 0, 1
		elif e.key in (K_LEFT, K_a):
			self.wdx, self.wdy = -1, 0
		elif e.key in (K_RIGHT, K_d):
			self.wdx, self.wdy = 1, 0

	def to_next_tile(self):
		"""returns 0 <= x <= 1 depending on how close we are to be completely
		over the next tile in one direction (since only changes at a time)"""
		if self.dx != 0:
			difference = self.x * TILE_SIZE - self.ax
		else:
			difference = self.y * TILE_SIZE - self.ay
		return abs(difference / TILE_SIZE)

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

		# moves the pacman pixel wise
		self.ax += self.dx * Pacman.speed
		self.ay += self.dy * Pacman.speed

		# update the current tile position based on the pixel position
		if self.to_next_tile() == 1:
			self.x += self.dx
			self.y += self.dy

		if self.tile() == 't':
			if self.just_tp:
				self.just_tp = False
			elif self.to_next_tile() == 0:
				# teleport to the *other* gate
				if self.tiles.teleports[0] == (self.x, self.y):
					self.x, self.y = self.tiles.teleports[1]
				else:
					self.x, self.y = self.tiles.teleports[0]

				self.ax = self.x * TILE_SIZE
				self.ay = self.y * TILE_SIZE
				self.just_tp = True
			return

		if is_blocking(self.next_tile()):
			# stop moving
			self.dx = self.dy = 0

		if self.wdx + self.wdy != 0 and not is_blocking(self.next_wanted_tile()):
			# there are 2 different case. Either the pacman is going in the
			# opposite direction, in which case we can just change dy and dx,
			# or it's turning, in which case we have to wait until we get to the
			# next tile and *then* turn
			if (self.dx, self.dy) == (-self.wdx, -self.wdy) \
				or self.to_next_tile() == 0:
				self.dx, self.dy = self.wdx, self.wdy
				self.wdx = self.wdy = 0

	def render(self, surface):
		center = (self.ax + TILE_SIZE // 2,
				  self.ay + TILE_SIZE // 2)
		pygame.draw.circle(surface, pygame.Color('yellow'), center,
						   TILE_SIZE // 2)