import pygame

class Bullet:
    def __init__(self, x, y, radius, speed, color, direction):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.color = color
        self.direction = direction  # -1 = arriba, +1 = abajo
        self.rect = pygame.Rect(x - radius, y - radius, radius * 2, radius * 2)

    def update(self):
        self.y += self.speed * self.direction
        self.rect.y = self.y - self.radius

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def is_off_screen(self, screen_height):
        return self.y < 0 or self.y > screen_height
