class GameStats():
	"""monitor the game's statistical information"""
	
	def __init__(self, ai_settings):
		"""initialize statistical information"""
		self.ai_settings = ai_settings
		self.reset_stats()
		
		# make the game inert at the beginning
		self.game_active = False
		
		# do not reset the highest score under any circumstance
		self.high_score = 0
		
	def reset_stats(self):
		"""initialize possible variables in statistical information"""
		self.ships_left = self.ai_settings.ship_limit
		self.score = 0
		self.level = 1
		
	
