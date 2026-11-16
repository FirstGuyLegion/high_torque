#render.py
import pygame

class Render:

	def __init__(self, pngMap):
		self.sprites = {
			"background" : pygame.image.load("assets/sprites/background.png"),
			"road" : pygame.image.load("assets/sprites/road.png"),
			"goal" : pygame.image.load("assets/sprites/goal.png"),
			"player" : pygame.image.load("assets/sprites/player.png"),
			"mechanic" : pygame.image.load("assets/sprites/mechanic.png"),
			"empty" : pygame.image.load("assets/sprites/empty_p.png"),
			"phone" : pygame.image.load("assets/sprites/phone.png")
		}
		self.map = pngMap
		self.road = pygame.Surface((640,640), pygame.SRCALPHA)
		self.textbox = pygame.Surface((640,80))
		self.init_road()

		self.reset_menu_s = pygame.Surface((640,640), pygame.SRCALPHA)
		self.reset_menu_s.fill((50,50,50,200))

		self.font   = pygame.font.SysFont("Arial", 50)
		self.s_font = pygame.font.SysFont("Arial", 20)

	def init_road(self):
		self.road.fill((0,0,0,0))
		for y in range(20):
			for x in range(20):
				if self.map[y][x]: 
					self.road.blit(self.sprites["road"], (x*32,y*32))
					if self.map[y][x] == 2: self.road.blit(self.sprites["goal"], (x*32,y*32))
				
	def draw(self, screen:pygame.Surface, data):
		s,c, laps = self.draw_player(data)

		screen.blit(self.sprites["background"], (0,0))
		screen.blit(self.road, (0,0))
		screen.blit(s,c)
		self.draw_text(screen, str(laps), [], True)

	def draw_player(self, data):
		angle, cords, laps = data
		temp = pygame.transform.rotate(self.sprites["player"], angle)
		return temp, cords, laps

	def draw_text(self, screen, text, xy, lap=False):
		if lap:
			if len(text) == 1:
				suffix = "th"
				if int(text) == 1: suffix = "st"
				if int(text) == 2: suffix = "nd"
				if int(text) == 3: suffix = "rd"
				msg = f"{text}{suffix} Lap"
			else:
				msg = text

			spr = self.font.render(msg, True, "white")

			x = 320 - (spr.get_width() / 2)
			y = 320 - (spr.get_height() / 2)

			outline = self.font.render(msg, True, "black")
			for ox in [-2, -1, 0, 1, 2]:
				for oy in [-2, -1, 0, 1, 2]:
					if ox != 0 or oy != 0:
						screen.blit(outline, (x + ox, y + oy))

			screen.blit(spr, (x, y))

		else:
			spr = self.s_font.render(text, True, "black")
			screen.blit(spr, xy)

	def reset(self, pngMap):
		self.map = pngMap
		self.init_road()

	def draw_textbox(self, screen, data):
		name, line = data

		name_s = "Player:" if name == "empty" else "Howard T. Phillips:"

		self.textbox.fill("white")
		self.draw_text(self.textbox, name_s, [105,8])
		self.draw_text(self.textbox, line, [105,35])
		self.textbox.blit(self.sprites[name], (32,8))
		screen.blit(self.textbox, (0,560))

	def draw_menu(self, screen):
		screen.blit(self.sprites["background"], (0,0))

	def render_reset(self, screen, data):
		screen.blit(self.reset_menu_s, (0,0))
		self.draw_text(screen, "Press SHIFT to RESTART", [], True)

		self.show_data(screen, data)

	def show_data(self, screen, data):
		y = 384
		for i in range(len(data)):
			surf = pygame.Surface((256, 32))
			surf.fill("white")
			self.draw_text(surf, data[i], [6,6])

			screen.blit(surf, (6*32, y))
			y += 48