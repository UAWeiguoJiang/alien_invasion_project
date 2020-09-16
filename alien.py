import pygame
from pygame.sprite import Sprite
class Alien(Sprite):
	"""class representing each alien"""
	
	def __init__(self, ai_settings, screen):
		"""initialize aliens and set their locations"""
		super(Alien, self).__init__()
		self.screen = screen
		self.ai_settings = ai_settings
		
		# load alien images and set its rectangle characteristic
		self.image = pygame.image.load('images/alien.bmp')
		self.rect = self.image.get_rect()
		
		# every alien is initially on the upper left corner of the screen
		self.rect.x = self.rect.width
		self.rect.y = self.rect.height
		
		# store alien's exact location
		self.x = float(self.rect.x)
		
	def blitme(self):
		"""draw aliens in designated area"""
		self.screen.blit(self.image, self.rect)
	
	def update(self):
		"""move the aliens to the left"""
		self.x += (self.ai_settings.alien_speed_factor * 
						self.ai_settings.fleet_direction)
		self.rect.x = self.x
	
	def check_edges(self):
		"""return True if aliens are on edges"""
		screen_rect = self.screen.get_rect()
		if self.rect.right >= screen_rect.right:
			return True
		elif self.rect.left <- 0:
			return True
