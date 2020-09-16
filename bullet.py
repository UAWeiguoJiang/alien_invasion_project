import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
	"""a class that manages the bullets that the ship fired"""
	
	def __init__(self, ai_settings, screen, ship):
		"""create a bullet in the location of the ship"""
		super(Bullet, self).__init__()
		self.screen = screen
		
		# create a rectangle that represents the bullet at (0,0), then adjust it to the correct location
		self.rect = pygame.Rect(0, 0, ai_settings.bullet_width,
			ai_settings.bullet_height)
		self.rect.centerx = ship.rect.centerx
		self.rect.top = ship.rect.top
		# store location of the bullet in floats
		self.y = float(self.rect.y)
		
		self.color = ai_settings.bullet_color
		self.speed_factor = ai_settings.bullet_speed_factor
		
	def update(self):
		"""move the bullet upward"""
		# update the floats of the bullets
		self.y -= self.speed_factor
		# update the location of the rectangle
		self.rect.y = self.y
		
	def draw_bullet(self):
		"""draw the bullet on the screen"""
		pygame.draw.rect(self.screen, self.color, self.rect)
		
