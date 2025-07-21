import pygame
import time
from player import Player
from enemy import Enemy
from bullet import Bullet

# Inicialización
pygame.init()
WIDTH, HEIGHT = 1200, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hell Tunes")
clock = pygame.time.Clock()

# Jugador y jefe
player = Player(x=WIDTH // 3, y=HEIGHT - 80, size=30, speed=5, screen_width=WIDTH, screen_height=HEIGHT)
boss = Enemy(x=WIDTH // 2 - 75, y=50, width=150, height=60, max_health=300)

# Disparos del jugador
player_bullets = []
shoot_cooldown = 0.25  # segundos
last_shot_time = 0

# Bucle principal
running = True
while running:
    clock.tick(60)
    current_time = time.time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movimiento del jugador
    keys = pygame.key.get_pressed()
    player.move(keys)

    # Disparar con tecla Z
    if keys[pygame.K_z] and current_time - last_shot_time > shoot_cooldown:
        bullet = player.shoot()
        player_bullets.append(bullet)
        last_shot_time = current_time

    # Mover jefe
    boss.move(WIDTH)

    # Actualizar balas del jugador
    for bullet in player_bullets[:]:
        bullet.update()
        if bullet.is_off_screen(HEIGHT):
            player_bullets.remove(bullet)
        elif bullet.rect.colliderect(boss.rect):
            boss.take_damage(10)
            player_bullets.remove(bullet)

    # Dibujar todo
    screen.fill((0, 0, 0))
    boss.draw(screen)
    player.draw(screen)

    for bullet in player_bullets:
        bullet.draw(screen)

    pygame.display.flip()

pygame.quit()
