import pygame
from Player import Player
from Enemy import Enemy
from Bullet import Bullet

# Inicialización de Pygame
pygame.init()

# Dimensiones de la pantalla
WIDTH, HEIGHT = 1200, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hell Tunes - Boss Battle")

# Reloj
clock = pygame.time.Clock()
FPS = 60

# Colores
BLACK = (0, 0, 0)

# Instanciar jugador y enemigo
player = Player(x=WIDTH // 3, y=HEIGHT - 80, size=30, speed=5,
                screen_width=WIDTH, screen_height=HEIGHT)
enemy = Enemy(x=WIDTH // 2 - 50, y=50, width=100, height=60, max_health=100)

# Loop principal
running = True
while running:
    clock.tick(FPS)
    screen.fill(BLACK)

    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Entrada de teclado
    keys = pygame.key.get_pressed()
    player.update(keys)
    enemy.update(WIDTH)

    # --- Detección de colisiones ---
    # Balas del jugador que impactan al jefe
    for bullet in player.bullets[:]:
        if enemy.rect.colliderect(bullet.rect) and bullet.from_player:
            enemy.take_damage(1)
            player.bullets.remove(bullet)

    # Balas del jefe que impactan al jugador
    for bullet in enemy.bullets[:]:
        if player.rect.colliderect(bullet.rect) and not bullet.from_player:
            if player.take_damage():
                print("¡Jugador recibió daño!")
            enemy.bullets.remove(bullet)

    # Dibujar
    enemy.draw(screen)
    player.draw(screen)

    # Actualizar pantalla
    pygame.display.flip()

pygame.quit()
