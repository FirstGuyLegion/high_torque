import pygame

class DJ:

	def __init__(self):
		self.point = pygame.mixer.Sound("assets/sound/point.ogg")

	def activate(self):
		pygame.mixer.init()

	def play(self):
		self.point.play()