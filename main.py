import pygame
import sys
from Player import Player
from Enemy import Enemy
from Particles import Particle
from SoundManager import SoundManager

# Inicialización de pygame
pygame.init()

# Configuración de pantalla
WIDTH, HEIGHT = 1200, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hell Tunes")
clock = pygame.time.Clock()

# Sonidos
sound_manager = SoundManager()

# Crear jugador
player = Player(
    x=WIDTH // 3,
    y=HEIGHT - 80,
    size=30,
    speed=5,
    screen_width=WIDTH,
    screen_height=HEIGHT,
    sound_manager=sound_manager
)

# Crear enemigo y pasarle al jugador como referencia
enemy = Enemy(
    x=WIDTH // 2 - 50,
    y=50,
    width= 250,
    height=95,
    max_health=100,
    sound_manager=sound_manager,
    player=player  # 🔧 <- Este es el cambio importante
)

# Lista de partículas
particles = []

# Bucle principal
running = True
while running:
    clock.tick(60)
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movimiento del jugador
    keys = pygame.key.get_pressed()
    player.update(keys)

    # Actualizar enemigo
    enemy.update(WIDTH)

    # Actualizar y dibujar partículas
    for particle in particles[:]:
        particle.update()
        particle.draw(screen)
        if particle.lifetime <= 0:
            particles.remove(particle)

    # Colisiones: balas del jugador al jefe
    for bullet in player.bullets[:]:
        if enemy.rect.colliderect(bullet.rect) and bullet.from_player:
            enemy.take_damage(1)
            player.bullets.remove(bullet)

            sound_manager.play("enemy_hit")

            for _ in range(10):
                particles.append(Particle(bullet.rect.centerx, bullet.rect.centery, (255, 255, 0)))

    # Colisiones: balas del jefe al jugador
    for bullet in enemy.bullets[:]:
        if player.rect.colliderect(bullet.rect) and not bullet.from_player:
            if player.take_damage():
                sound_manager.play("player_hit")
                print("¡Jugador recibió daño!")

    # Dibujar
    enemy.draw(screen)
    player.draw(screen)

    # Mostrar
    pygame.display.flip()

pygame.quit()
sys.exit()
