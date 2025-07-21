import pygame
import random

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.radius = random.randint(2, 5)
        self.color = color
        self.lifetime = 30  # <-- ESTA LÍNEA ES CLAVE

        self.dx = random.uniform(-2, 2)
        self.dy = random.uniform(-2, 2)

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.lifetime -= 1
        self.radius = max(0, self.radius - 0.1)

    def draw(self, screen):
        if self.lifetime > 0:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.radius))

    def is_dead(self):
        return self.lifetime <= 0 or self.radius <= 0
