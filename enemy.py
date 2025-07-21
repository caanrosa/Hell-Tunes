import pygame
import time

class Enemy:
    def __init__(self, x, y, width, height, max_health):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (255, 255, 0)  # Amarillo al inicio
        self.max_health = max_health
        self.health = max_health
        self.speed = 4
        self.direction = 1  # 1 = derecha, -1 = izquierda
        self.last_hit_time = 0
        self.iframe_duration = 0.5  # segundos de invulnerabilidad

    def move(self, screen_width):
        self.rect.x += self.speed * self.direction
        if self.rect.right >= screen_width or self.rect.left <= 0:
            self.direction *= -1  # Cambiar dirección

    def take_damage(self, amount):
        current_time = time.time()
        if current_time - self.last_hit_time > self.iframe_duration:
            self.health -= amount
            self.last_hit_time = current_time
            self.update_color()

    def update_color(self):
        ratio = self.health / self.max_health
        if ratio > 0.66:
            self.color = (255, 255, 0)  # Amarillo
        elif ratio > 0.33:
            self.color = (255, 165, 0)  # Naranja
        else:
            self.color = (255, 0, 0)    # Rojo

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
