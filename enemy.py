import pygame
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
        self.sound_manager = sound_manager  # ✅ aquí

    def update(self, screen_width):
        self.rect.x += self.direction * self.speed
        if self.rect.right >= screen_width or self.rect.left <= 0:
            self.direction *= -1

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

        self.shoot_timer += 1
        if self.shoot_timer >= self.shoot_interval:
            self.shoot()
            self.shoot_timer = 0

        for bullet in self.bullets:
            bullet.update()
        self.bullets = [b for b in self.bullets if b.rect.y <= 900]

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.bottom, 0, 7, from_player=False)
        self.bullets.append(bullet)
        self.sound_manager.play("enemy_shoot")  # ✅ reproducir sonido

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
