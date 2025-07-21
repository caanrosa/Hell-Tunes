# Hell Tunesimport pygame

import sys
import pygame

# Inicializar Pygame
pygame.init()

# Dimensiones de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bullet Hell Rítmico")

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Jugador
player_size = 40
player_x = WIDTH // 2
player_y = HEIGHT - 60
player_speed = 5

clock = pygame.time.Clock()

# Bucle principal del juego
running = True
while running:
    clock.tick(60)  # 60 FPS
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movimiento del jugador
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_size:
        player_x += player_speed
    if keys[pygame.K_UP] and player_y > 0:
        player_y -= player_speed
    if keys[pygame.K_DOWN] and player_y < HEIGHT - player_size:
        player_y += player_speed

    # Dibujar jugador
    pygame.draw.rect(screen, WHITE, (player_x, player_y, player_size, player_size))

    pygame.display.flip()

pygame.quit()
sys.exit()
