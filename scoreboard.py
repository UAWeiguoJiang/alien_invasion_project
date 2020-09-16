import pygame.font
from pygame.sprite import Group

from ship import Ship

class Scoreboard():
	"""show score information class"""
	
	def __init__(self, ai_settings, screen, stats):
		"""initialize characteristics relating to scoring"""
		self.screen = screen
		self.screen_rect = screen.get_rect()
		self.ai_settings = ai_settings
		self.stats = stats
		
		# show score's font information
		self.text_color = (30, 30, 30)
		self.font = pygame.font.SysFont(None, 48)
		
		# prepare for initial scoring picture
		self.prep_score()
		
		# prepare for highest score picture
		self.prep_high_score()
		
		self.prep_level()
		self.prep_ships()
	
	def prep_score(self):
		"""change the score into a picture"""
		rounded_score = int(round(self.stats.score, -1))
		score_str = "{:,}".format(rounded_score)
		self.score_image = self.font.render(score_str, True, self.text_color,
			self.ai_settings.bg_color)
			
		self.score_rect = self.score_image.get_rect()
		self.score_rect.right = self.screen_rect.right - 20
		self.score_rect.top = 20
	
	def show_score(self):
		"""show the score on the screen and the remaining number of ships"""
		self.screen.blit(self.score_image, self.score_rect)
		self.screen.blit(self.high_score_image, self.high_score_rect)
		self.screen.blit(self.level_image, self.level_rect)
		# draw the ship
		self.ships.draw(self.screen)
		
	def prep_high_score(self):
		high_score = int(round(self.stats.high_score, -1))
		high_score_str = "{:,}".format(high_score)
		self.high_score_image = self.font.render(high_score_str, True,
			self.text_color, self.ai_settings.bg_color)
			
		# put the highest score in the top middle of the screen
		self.high_score_rect = self.high_score_image.get_rect()
		self.high_score_rect.centerx = self.screen_rect.centerx
		self.high_score_rect.top = self.score_rect.top
		
	def prep_level(self):
		"""turn level into a picture"""
		self.level_image = self.font.render(str(self.stats.level), True,
				self.text_color, self.ai_settings.bg_color)
		self.level_rect = self.level_image.get_rect()
		self.level_rect.right = self.score_rect.right
		self.level_rect.top = self.score_rect.bottom + 10
		
	def prep_ships(self):
		"""show the remaining number of ships"""
		self.ships = Group()
		for ship_number in range(self.stats.ships_left):
			ship = Ship(self.ai_settings, self.screen)
			ship.rect.x = 10 + ship_number * ship.rect.width
			ship.rect.y = 10
			self.ships.add(ship)
		 
