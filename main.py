#main.py
import pygame
import asyncio
from player import Player
from maps import P2M
from render import Render
from story import Story
from dj import DJ

pygame.init()

screen = pygame.display.set_mode((640,640))
pygame.display.set_caption("High Torque")
clock = pygame.time.Clock()

maps = P2M()
dj = DJ()
player = Player(maps.goal, dj)
render = Render(maps.get())
story = Story()

map_names = [
	"Ring",
	"Hour glass",
	"Shield",
	"Clover"
]

async def main():
	game = True
	menu = True
	start = False

	while menu:
		screen.fill((245, 245, 230))

		render.draw_menu(screen)
		if story.started: render.draw_textbox(screen, story.line())
		render.draw_text(screen, "PRESS SHIFT", [], True)

		for event in pygame.event.get():
				if event.type == pygame.QUIT: game, menu = False, False
				if event.type == pygame.KEYUP:
					if event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT: 
						if story.End: menu = False
						elif not story.started: story.started = True
						else: story.start()

		await asyncio.sleep(0)
		pygame.display.flip()
		clock.tick(30)

	t_start = 0
	t_end = 0
	dj.activate()

	while game:
		screen.fill("black")
		dt = clock.tick(30)/1000

		render.draw(screen, player.get())
		end = (player.laps >= 6 and player.mv <= 0) or not player.alive

		if end: 
			if t_end == 0: t_end = pygame.time.get_ticks()
			data = [
				f"Map name: {map_names[maps.map_id()]}",
				f"Laps done: {player.laps-1}/5",
				f"Test completed: {str(player.laps >= 6)}",
				f"Test time: {str((t_end-t_start)/1000)} s",
				f"Top speed: {round(player.v_record*19.8)} km/h"
			]
			render.render_reset(screen, data)

		for event in pygame.event.get():
			if event.type == pygame.QUIT: game = False
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT:
					if not end:
						if t_start == 0: t_start = pygame.time.get_ticks()
						start = True
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT:
					if end:
						start = False
						maps.reset()
						render.reset(maps.get())
						player.reset(maps.goal)
						t_start = 0
						t_end = 0

		if start: 
			keys = pygame.key.get_pressed()
			player.move(keys, dt)
			player.crashed(maps.road)

		await asyncio.sleep(0)
		pygame.display.flip()

asyncio.run(main())
pygame.quit()