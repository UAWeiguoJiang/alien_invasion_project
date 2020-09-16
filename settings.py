class Settings():
	"""store every classes in Alien Invasion"""
	
	def __init__(self):
		"""initialize settings of the game"""
		# screen settings
		self.screen_width = 1000
		self.screen_height = 600
		self.bg_color = (230, 230, 230)
		
		# the ship's settings
		self.ship_speed_factor = 25
		self.ship_limit = 3
		
		# bullet settings
		self.bullet_speed_factor = 10
		self.bullet_width = 10
		self.bullet_height = 35
		self.bullet_color = 60, 60, 60
		self.bullets_allowed = 6
		
		# alien settings
		self.alien_speed_factor = 1
		self.fleet_drop_speed = 10
		# fleet_direction = 1 represents moving right, -1 represents moving left
		self.fleet_direction = 1
		
		# speed how much up when you pass 1 level
		self.speedup_scale = 1.2
		
		# increase in alien points after passing one level
		self.score_scale = 1.8
		
		self.initialize_dynamic_settings
		
	def initialize_dynamic_settings(self):
		"""initialize settings that changes as the game proceeds"""
		self.ship_speed_factor = 3
		self.bullet_speed_factor = 3
		self.alien_speed_factor = 1
		
		# record score
		self.alien_points = 7500
		
		# when fleet_direction = 1, it means the fleet going right, -1 means going left
		self.fleet_direction = 1
		
	def increase_speed(self):
		"""increase speed settings and points per alien"""
		self.ship_speed_factor *= self.speedup_scale
		self.bullet_speed_factor *= self.speedup_scale
		self.alien_speed_factor *= self.speedup_scale
		
		self.alien_points = int(self.alien_points * self.score_scale)
		print(self.alien_points)
		
