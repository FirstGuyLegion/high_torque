#player.py
import pygame
import math

class Player:

	def __init__(self, start, dj):
		self.angle = 90
		self.xy = [start[1][0]*32,start[1][1]*32]
		self.alive = True
		self.on_line = True
		self.start_pos = start

		self.laps = 1

		self.rv = 2 * 30
		self.mv = 0
		self.max_v = 15
		self.min_v = 4

		self.v_record = 0
		self.dj = dj

	def move(self, keys, dt):
		if self.alive and self.laps < 6:
			a = 0.1 * 30 * self.laps * dt
			if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
				if   keys[pygame.K_LSHIFT]: self.angle -= self.rv*dt
				elif keys[pygame.K_RSHIFT]: self.angle += self.rv*dt
				if self.mv > self.min_v: self.mv -= a
			else: 
				if self.mv < self.max_v: self.mv += a

			if self.mv > self.v_record: self.v_record = self.mv

			self.xy[0] += self.mv * math.sin(math.radians(self.angle))
			self.xy[1] += self.mv * math.cos(math.radians(self.angle))
			self.check()

		elif self.alive:
			if self.mv >= 0: self.mv -= 0.2
			else: self.alive = False
			if self.alive:
				self.xy[0] += self.mv * math.sin(math.radians(self.angle))
				self.xy[1] += self.mv * math.cos(math.radians(self.angle))

	def get(self):
		return self.angle, self.xy, self.laps

	def crashed(self, roads):
		x,y = self.xy
		x = int((x+16)/32)
		y = int((y+16)/32)

		self.alive = (x,y) in roads

	def check(self):
		x,y = self.xy
		x = int((x+16)/32)
		y = int((y+16)/32)

		if (x,y) in self.start_pos:
			if not self.on_line:
				self.on_line = True
				self.laps += 1
				self.dj.play()
		else:
			self.on_line = False

	def reset(self, start):
		self.angle = 90
		self.xy = [start[1][0]*32,start[1][1]*32]
		self.alive = True
		self.on_line = True
		self.start_pos = start
		self.mv = 0
		self.laps = 1
		self.v_record = 0