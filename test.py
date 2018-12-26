import pygame
from time import time
from Scene import Scene

class Test(Scene):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.plan = []
		self.width = 0
		self.height = 0
		with open('./plans/original.txt', 'r') as fp:
			next(fp)
			for line in fp:
				self.height += 1
				self.plan.append(list(line))
			self.width = len(line)

		self.sprites = {
			'wall': pygame.Surface((20, 20))
		}
		self.sprites['wall'].fill(pygame.Color('gray'))
		self.highlighted = None
		self.distance_plan = None

	def handle_event(self, e):
		if e.type == pygame.QUIT:
			self.quit()
		elif e.type == pygame.MOUSEBUTTONDOWN:
			if e.button == 1:
				x = int(e.pos[0] / 20)
				y = int(e.pos[1] / 20)
				if self.plan[y][x] == ' ':
					self.highlighted = (x, y)
					self.map_distances(x, y)
				else:
					self.highlighted = None
					self.distance_plan = None

	def map_distances(self, x, y):
		self.distance_plan = [[float('inf') for _ in range(self.width)]
							  for _ in range(self.height)]
		def map(x, y, distance):
			self.distance_plan[y][x] = distance
			if y > 0 and self.plan[y-1][x] == ' ' \
				and self.distance_plan[y-1][x] > distance + 1:
				map(x, y - 1, distance + 1)
			if y < self.height - 1 and self.plan[y+1][x] == ' ' \
				and self.distance_plan[y+1][x] > distance + 1:
				map(x, y + 1, distance + 1)
			if x > 0 and self.plan[y][x-1] == ' ' \
				and self.distance_plan[y][x-1] > distance + 1:
				map(x - 1, y, distance + 1)
			if x < self.width - 1 and self.plan[y][x+1] == ' ' \
				and self.distance_plan[y][x+1] > distance + 1:
				map(x + 1, y, distance + 1)

		map(x, y, 0)

	def render(self, surface):
		for y, row in enumerate(self.plan):
			for x, char in enumerate(row):
				if char == ' ' and self.distance_plan:
					color = ((255 - self.distance_plan[y][x] * 5) % 255, ) * 3
					pygame.draw.rect(surface, color,
						pygame.Rect((x * 20, y * 20), (20, 20)))
				elif char == '0':
					pygame.draw.rect(surface, pygame.Color('skyblue'),
						pygame.Rect((x * 20, y * 20), (20, 20)))

		if self.highlighted:
			pygame.draw.rect(surface, pygame.Color('yellow'),
				pygame.Rect((self.highlighted[0] * 20, self.highlighted[1] * 20),
							(20, 20)))
