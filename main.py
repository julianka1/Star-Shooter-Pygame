import pygame
import sys
import random

pygame.init()

width, height = 800, 600

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Star Shooter')

print('Star Shooter dessigned by Julian Kaints')

background = pygame.image.load('background.jpg')
raumschiff = pygame.image.load('Raumschiff.png')
ufo = pygame.image.load('ufo.png')
healthbar = pygame.image.load('healthbar.png')

# Game-Variablen für das Raumschiff
pos_x = 350
pos_y = 450
geschwindigkeit = 5
schuesse_raumschiff = []
raumschiff_health = 1.0

# Game-Variablen für das UFO
ufo_pos_x = 350
ufo_pos_y = 150
ufo_speed = 3
schuesse_ufo = []
ufo_last_shot_time = pygame.time.get_ticks()
ufo_shoot_delay = 500 
ufo_health = 1.0

bullet_speed = 5
bullet_delay = 250  
last_shot_time = pygame.time.get_ticks()

running = True
clock = pygame.time.Clock()

def fire_bullet(x, y, bullet_list, color, target_x, target_y):
    dx = target_x - x
    dy = target_y - y
    length = max(abs(dx), abs(dy))
    if length != 0:
        bullet_list.append([x + raumschiff.get_width() // 2, y, color, dx / length * bullet_speed, dy / length * bullet_speed])

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and pos_x > 0:
        pos_x -= geschwindigkeit

    if keys[pygame.K_RIGHT] and pos_x < width - raumschiff.get_width():
        pos_x += geschwindigkeit

    current_time = pygame.time.get_ticks()
    if current_time - last_shot_time >= bullet_delay:
        fire_bullet(pos_x, pos_y, schuesse_raumschiff, (255, 0, 0), ufo_pos_x + ufo.get_width() // 2, ufo_pos_y + ufo.get_height() // 2)
        last_shot_time = current_time

    current_time = pygame.time.get_ticks()
    if current_time - ufo_last_shot_time >= ufo_shoot_delay:
        fire_bullet(ufo_pos_x, ufo_pos_y, schuesse_ufo, (0, 255, 0), pos_x + raumschiff.get_width() // 2, pos_y + raumschiff.get_height() // 2)
        ufo_last_shot_time = current_time

    removed_bullets = []
    for bullet in schuesse_raumschiff:
        bullet[0] += bullet[3]
        bullet[1] += bullet[4]
        if bullet[1] < 0 or bullet[1] > height or bullet[0] < 0 or bullet[0] > width:
            removed_bullets.append(bullet)
    for bullet in removed_bullets:
        schuesse_raumschiff.remove(bullet)

    removed_bullets = []
    for bullet in schuesse_ufo:
        bullet[0] += bullet[3]
        bullet[1] += bullet[4]
        if bullet[1] > pos_y + raumschiff.get_height() // 2:
            bullet[3] = 0
            bullet[4] = bullet_speed
        if bullet[1] > height:
            removed_bullets.append(bullet)
        if pos_x < bullet[0] < pos_x + raumschiff.get_width() and pos_y < bullet[1] < pos_y + raumschiff.get_height():
            raumschiff_health -= 0.05
            removed_bullets.append(bullet)
    for bullet in removed_bullets:
        schuesse_ufo.remove(bullet)

    for bullet in schuesse_raumschiff:
        if ufo_pos_x < bullet[0] < ufo_pos_x + ufo.get_width() and ufo_pos_y < bullet[1] < ufo_pos_y + ufo.get_height():
            ufo_health -= 0.0025
            schuesse_raumschiff.remove(bullet)

    screen.blit(background, (0, 0))
    screen.blit(raumschiff, (pos_x, pos_y))
    screen.blit(ufo, (ufo_pos_x, ufo_pos_y))
    
    screen.blit(healthbar, (250, 550))
    screen.blit(healthbar, (250, 20))

    pygame.draw.rect(screen, "red", (253, 553, 294, 34))
    pygame.draw.rect(screen, "green", (253, 553, 294*raumschiff_health, 34))
    
    pygame.draw.rect(screen, "red", (253, 23, 294, 34))
    pygame.draw.rect(screen, "green", (253, 23, 294*ufo_health, 34))
    
    for bullet in schuesse_raumschiff:
        pygame.draw.line(screen, bullet[2], (bullet[0], bullet[1]), (bullet[0], bullet[1] + 10), 2)

    for bullet in schuesse_ufo:
        pygame.draw.line(screen, bullet[2], (bullet[0], bullet[1]), (bullet[0], bullet[1] + 10), 2)

    pygame.display.flip()
    clock.tick(60)
