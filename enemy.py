import pygame
import math
import random
import os
from Bullet import Bullet


class Enemy:
    def __init__(self, x, y, width, height, max_health, sound_manager, player):
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
        self.player = player

        # Sistema de patrones
        self.patterns = [self.shoot_flower, self.shoot_spiral, self.shoot_multiple_flower, self.shoot_wave, self.shoot_crossburst]
        self.current_pattern_index = 0
        self.pattern_timer = 0
        self.pattern_interval = 600
        self.angle = 0
        self.last_flower_shot = 0
        
         # Imagen del jefe
        self.image = pygame.image.load(os.path.join("assets", "Boss.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))  # Escalamos al tamaño del rectángulo

    def update(self, screen_width):
        self.rect.x += self.direction * self.speed
        if self.rect.right >= screen_width or self.rect.left <= 0:
            self.direction *= -1

        phase = self.health / self.max_health
        if phase > 0.66:
            self.color = (0, 0, 0)
            self.speed = 4
            self.shoot_interval = 60
        elif phase > 0.33:
            self.color = (255, 165, 0)
            self.speed = 6
            self.shoot_interval = 40
        else:
            self.color = (255, 0, 0)
            self.speed = 8
            self.shoot_interval = 20

        self.pattern_timer += 1
        if self.pattern_timer >= self.pattern_interval:
            self.pattern_timer = 0
            self.current_pattern_index = (self.current_pattern_index + 1) % len(self.patterns)

        self.shoot_timer += 1
        if self.shoot_timer >= self.shoot_interval:
            self.patterns[self.current_pattern_index]()
            self.shoot_timer = 0

        for bullet in self.bullets:
            bullet.update()
        self.bullets = [b for b in self.bullets if 0 <= b.rect.y <= 900]

    def shoot_wave(self):
        self.sound_manager.play("enemy_shoot")
        for i in range(-3, 4):
            dx = math.sin(i)
            dy = 1
            bullet = Bullet(self.rect.centerx + i * 15, self.rect.bottom, dx, dy, from_player=False)
            self.bullets.append(bullet)

    def shoot_crossburst(self):
        self.sound_manager.play("enemy_shoot")
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1),
                      (1, 1), (-1, 1), (1, -1), (-1, -1)]
        for dx, dy in directions:
            bullet = Bullet(self.rect.centerx, self.rect.centery, dx * 6, dy * 6, from_player=False)
            self.bullets.append(bullet)

    def shoot_multiple_flower(self):
        offset = random.uniform(0, 2 * math.pi)
        now = pygame.time.get_ticks()

        if self.health > self.max_health * 0.66:
            n_flores = 3
            delay = 500
        elif self.health > self.max_health * 0.33:
            n_flores = 5
            delay = 300
        else:
            n_flores = 7
            delay = 100

        if now - self.last_flower_shot >= delay:
            self.last_flower_shot = now
            for j in range(n_flores):
                for i in range(8):
                    angle = i * (2 * math.pi / 8) + offset + j * 0.2
                    dx = math.cos(angle)
                    dy = math.sin(angle)
                    bullet = Bullet(self.rect.centerx, self.rect.centery, dx * 4, dy * 4, from_player=False)
                    self.bullets.append(bullet)
            self.sound_manager.play("enemy_shoot")

    def shoot_flower(self):
        num_bullets = 24
        angle_step = 360 / num_bullets
        for i in range(num_bullets):
            angle = math.radians(i * angle_step)
            dx = math.cos(angle)
            dy = math.sin(angle)
            bullet = Bullet(self.rect.centerx, self.rect.centery, dx * 5, dy * 5, from_player=False)
            self.bullets.append(bullet)
        self.sound_manager.play("enemy_shoot")

    def shoot_spiral(self):
        dx_player = self.player.rect.centerx - self.rect.centerx
        dy_player = self.player.rect.centery - self.rect.centery
        base_angle = math.atan2(dy_player, dx_player)

        for i in range(25):
            angle = base_angle + self.angle + i * (math.pi / 20)
            dx = math.cos(angle)
            dy = math.sin(angle)
            bullet = Bullet(self.rect.centerx, self.rect.centery, dx * 9, dy * 9, from_player=False)
            self.bullets.append(bullet)

        self.angle += math.pi / 10
        self.sound_manager.play("enemy_shoot")

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        for bullet in self.bullets:
            bullet.draw(screen)
        self.draw_health_bar(screen)

    def draw_health_bar(self, screen):
        
        screen.blit(self.image, self.rect)
        
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
