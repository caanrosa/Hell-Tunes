import pygame
import math
from Bullet import Bullet

class Enemy:
    def __init__(self, x, y, width, height, max_health, sound_manager):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (255, 255, 0)
        self.health = max_health
        self.max_health = max_health
        self.direction = 1
        self.speed = 4
        self.bullets = []
        self.shoot_timer = 0
        self.shoot_interval = 60
        self.sound_manager = sound_manager

        self.attack_pattern = "normal"
        self.pattern_timer = 0
        self.pattern_interval = 600  # cambia cada 10 segundos (60fps * 10)

    def update(self, screen_width):
        self.rect.x += self.direction * self.speed
        if self.rect.right >= screen_width or self.rect.left <= 0:
            self.direction *= -1

        # Cambiar color y velocidad según salud
        phase = self.health / self.max_health
        if phase > 0.66:
            self.color = (255, 255, 0)
            self.speed = 4
        elif phase > 0.33:
            self.color = (255, 165, 0)
            self.speed = 6
        else:
            self.color = (255, 0, 0)
            self.speed = 8

        # Cambiar patrón de ataque periódicamente
        self.pattern_timer += 1
        if self.pattern_timer >= self.pattern_interval:
            self.pattern_timer = 0
            self.attack_pattern = "flower" if self.attack_pattern == "normal" else "normal"

        # Disparo según patrón actual
        self.shoot_timer += 1
        if self.shoot_timer >= self.shoot_interval:
            if self.attack_pattern == "normal":
                self.shoot()
            elif self.attack_pattern == "flower":
                self.shoot_flower()
            self.shoot_timer = 0

        # Actualizar balas
        for bullet in self.bullets:
            bullet.update()
        self.bullets = [b for b in self.bullets if b.rect.y <= 900]

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.bottom, 0, 7, from_player=False)
        self.bullets.append(bullet)
        self.sound_manager.play("enemy_shoot")

    def shoot_flower(self):
        num_bullets = 12
        angle_step = 360 / num_bullets
        for i in range(num_bullets):
            angle = math.radians(i * angle_step)
            dx = math.cos(angle)
            dy = math.sin(angle)
            bullet = Bullet(self.rect.centerx, self.rect.centery, dx * 5, dy * 5, from_player=False)
            self.bullets.append(bullet)
        self.sound_manager.play("enemy_shoot")

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        for bullet in self.bullets:
            bullet.draw(screen)
        self.draw_health_bar(screen)

    def draw_health_bar(self, screen):
        bar_width = self.rect.width
        bar_height = 8
        fill = int(bar_width * (self.health / self.max_health))
        border_rect = pygame.Rect(self.rect.x, self.rect.y - 20, bar_width, bar_height)
        fill_rect = pygame.Rect(self.rect.x, self.rect.y - 20, fill, bar_height)
        pygame.draw.rect(screen, (255, 0, 0), fill_rect)
        pygame.draw.rect(screen, (255, 255, 255), border_rect, 2)

    def take_damage(self, amount):
        self.health -= amount
        self.health = max(0, self.health)

    def is_dead(self):
        return self.health <= 0
