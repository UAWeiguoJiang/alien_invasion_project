import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from alien import Alien
import game_functions as gf
from pygame.sprite import Group

def run_game():
	# initialize game and create a screen object
	pygame.init()
	ai_settings = Settings()
	screen = pygame.display.set_mode(
		(ai_settings.screen_width, ai_settings.screen_height))
	pygame.display.set_caption("Alien Invasion")
	
	# create a Play button
	play_button = Button(ai_settings, screen, "Play")
	
	# create an example for storing statistcial information
	stats = GameStats(ai_settings)
	sb = Scoreboard(ai_settings, screen, stats)
	
	# create an alien
	alien = Alien(ai_settings, screen)
	
	# create a ship
	ship = Ship(ai_settings, screen)
	# create a class used to store bullets
	bullets = Group()
	
	aliens = Group()
	
	# create alien group
	gf.create_fleet(ai_settings, screen, ship, aliens)
	
	# begin the main loop of the game
	while True:
		gf.check_events(ai_settings, screen, stats, sb, play_button, ship, 
			aliens, bullets)
		
		if stats.game_active:
			ship.update()
			gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, 
				bullets)
			gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, 
				bullets)
		
		gf.update_screen(ai_settings, screen, stats, sb, ship, 
			aliens, bullets, play_button)
		
		# delete bullets that have disappeared
		for bullet in bullets.copy():
			if bullet.rect.bottom <= 0 :
				bullets.remove(bullet)
		print(len(bullets))

run_game()
