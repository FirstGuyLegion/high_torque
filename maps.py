#maps.py
import pygame
import random

class P2M:
	"""
	PNG to Map
	"""

	def __init__(self):
		self.map = [[0 for _ in range(20)] for _ in range(20)]
		self.road = []
		self.goal = []
		self.last = -1
		self.load()

	def load(self):
		val = random.randint(0,3)
		if val == self.last: 
			val -= 1
			if val < 0: val = 3

		png_map = pygame.image.load(f"assets/maps/map{val}.png")
		self.last = val

		for y in range(20):
			for x in range(20):
				val = png_map.get_at((x,y))
				if val[0] < 100: self.map[y][x] = 0
				else: 
					if val[0] > 200: 
						self.goal.append((x,y))
						self.map[y][x] = 2
					else: self.map[y][x] = 1
					self.road.append((x,y))

	def get(self):
		return self.map

	def reset(self):
		self.goal = []
		self.road = []
		self.load()

	def map_id(self):
		return self.last