import sys
from time import sleep

import pygame

from bullet import Bullet
from alien import Alien

def check_keydown_events(event, ai_settings, screen, ship, bullets):
	"""respond to typing"""
	if event.key == pygame.K_RIGHT:
		ship.moving_right = True
	elif event.key == pygame.K_LEFT:
		ship.moving_left = True
	elif event.key == pygame.K_SPACE:
		# create a bullet and add it to class bullets
		fire_bullet(ai_settings, screen, ship, bullets)
	elif event.key == pygame.K_q:
		sys.exit()
		
def fire_bullet(ai_settings, screen, ship, bullets):
	if len(bullets) < ai_settings.bullets_allowed:
		new_bullet = Bullet(ai_settings, screen, ship)
		bullets.add(new_bullet)
				
def check_keyup_events(event, ship):
				
	if event.key == pygame.K_RIGHT:
		ship.moving_right = False
	elif event.key == pygame.K_LEFT:
		ship.moving_left = False
				
def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, 
		bullets):
	"""respond to mouse and keyboard events"""
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			check_keydown_events(event, ai_settings, screen, ship, bullets)
		elif event.type == pygame.KEYUP:
			check_keyup_events(event, ship)
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			check_play_button(ai_settings, screen, stats, sb, play_button, 
				ship, aliens, bullets, mouse_x, mouse_y)

def check_play_button(ai_settings, screen, stats, sb, play_button, ship, 
		aliens,bullets, mouse_x, mouse_y):
	"""start a new game when the play clicks the Play button"""
	button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
	if button_clicked and not stats.game_active:
		# reset the game settings
		ai_settings.initialize_dynamic_settings()
		
		# hide the mouse
		pygame.mouse.set_visible(False)
		
		# reset the game's stats
		stats.reset_stats()
		stats.game_active = True
		
		# reset scoreboard image
		sb.prep_score()
		sb.prep_high_score()
		sb.prep_level()
		sb.prep_ships()
		
		# empty alien and bullet lists
		aliens.empty()
		bullets.empty()
		
		# create a new group of aliens and put the ship in the middle
		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()
		
def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets,
		play_button):
	"""update images on the screen and switch to new screen"""
	# resketch the screen per loop
	screen.fill(ai_settings.bg_color)
	# redraw all bullets after the ship and the aliens
	for bullet in bullets.sprites():
		bullet.draw_bullet()
	ship.blitme()
	aliens.draw(screen)
	
	# show the score
	sb.show_score()
	
	# if the game is inert, draw the Play button
	if not stats.game_active:
		play_button.draw_button()
	
	# make recently sketched screen visible
	pygame.display.flip()
	
def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
	"""update bullets' location and delete disappeared bullets"""
	# update bullets' location
	bullets.update()
	
	# delete bullets that have disappeared
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)
	check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, 
		aliens, bullets)
	
def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,
		aliens, bullets):
	# check if any bullet has hit the alien
	collisions = pygame.sprite.groupcollide(bullets, aliens, False, True)
	# use can use the combination (False, True)if you want the bullets to be penetrable
	
	if collisions:
		for aliens in collisions.values():
			stats.score += ai_settings.alien_points * len(aliens)
			sb.prep_score()
		check_high_score(stats, sb)
	
	if len(aliens) == 0:
		# delete current bullets and create a new group of aliens
		bullets.empty()
		ai_settings.increase_speed()
		
		#level up
		stats.level += 1
		sb.prep_level()
		
		create_fleet(ai_settings, screen, ship, aliens)
			
def get_number_aliens_x(ai_settings, alien_width):
	available_space_x = ai_settings.screen_width - 2* alien_width
	number_aliens_x = int(available_space_x / (2 * alien_width))
	return number_aliens_x
	
def create_alien(ai_settings, screen, aliens, alien_number, row_number):
	"""create an alien and put it in current line"""
	alien = Alien(ai_settings, screen)
	alien_width = alien.rect.width
	alien.x = alien_width + 2 * alien_width * alien_number
	alien.rect.x = alien.x
	alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
	aliens.add(alien)
			
def create_fleet(ai_settings, screen, ship, aliens):
	"""create alien group"""
	# create an alien and calculate how many aliens can exist in one line
	alien = Alien(ai_settings, screen)
	number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
	number_rows = get_number_rows(ai_settings, ship.rect.height,
		alien.rect.height)
	
	# create first line of aliens
	for row_number in range(number_rows):
		for alien_number in range(number_aliens_x):
			create_alien(ai_settings, screen, aliens, alien_number,
				row_number)

def get_number_rows(ai_settings, ship_height, alien_height):
	"""calculate how many aliens can exist on the screen"""
	available_space_y = (ai_settings.screen_height -
							(3 * alien_height) - ship_height)
	number_rows = int(available_space_y / (2 * alien_height))
	return number_rows
	
def check_fleet_edges(ai_settings, aliens):
    """Respond appropriately if any aliens have reached an edge."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break
        
def change_fleet_direction(ai_settings, aliens):
    """Drop the entire fleet, and change the fleet's direction."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
	check_fleet_edges(ai_settings, aliens)
	"""update all aliens' locations in the group"""
	aliens.update()
	
	# detect collisions between aliens and the ship
	if pygame.sprite.spritecollideany(ship, aliens):
		ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
		print("Ship hit!!!")
	
	check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)
		
def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
	"""respond to ship hit by aliens"""
	if stats.ships_left > 0:
		# minus 1 to ships_left
		stats.ships_left -= 1
		
		# update scoreboard
		sb.prep_ships()
	
		# empty alien & bullet lists
		aliens.empty()
		bullets.empty()
	
		# create a new group of aliens and put the ship in middle bottom of the screen
		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()
		
		# pause
		sleep(0.5)
		
	else:
		stats.game_active = False 
		pygame.mouse.set_visible(True)
	
def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, 
		bullets):
	"""detect if any alien have reached the bottom of the screen"""
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			# respond as if the ship has crashed
			ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
			break
			
def check_high_score(stats, sb):
	"""check if any new highest score has appeared"""
	if stats.score > stats.high_score:
		stats.high_score = stats.score
		sb.prep_high_score()



	
	
	

	
