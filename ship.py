import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
	
	def __init__(self, ai_settings, screen):
		"""initialize ship and set its initial location"""
		super(Ship, self).__init__()
		
		self.screen = screen
		self.ai_settings = ai_settings
		
		# load the ship image and acquire its minimum bounding rectangle
		self.image = pygame.image.load('images/ship.bmp')
		self.rect = self.image.get_rect()
		self.screen_rect = screen.get_rect()
		
		# put every new ship in the bottom center of the screen
		self.rect.centerx = self.screen_rect.centerx
		self.rect.bottom = self.screen_rect.bottom
		
		# store the decimals of the ship's center characteristic
		self.center = float(self.rect.centerx)
		
		# moving sign
		self.moving_right = False
		self.moving_left = False
	
	def update(self):
		"""modify the ship's location according to the moving sign"""
		# update the ship's center value instead of rect value
		if self.moving_right and self.rect.right < self.screen_rect.right:
			self.center += self.ai_settings.ship_speed_factor
		if self.moving_left and self.rect.left > 0:
			self.center -= self.ai_settings.ship_speed_factor
			
		# update object rect according to self.center
		self.rect.centerx = self.center
		
	def blitme(self):
		"""paint the ship in designated area"""
		self.screen.blit(self.image, self.rect)
	
	def center_ship(self):
		"""put the ship in the middle of the screen"""
		self.center = self.screen_rect.centerx
		
