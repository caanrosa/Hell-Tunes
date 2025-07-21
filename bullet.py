import pygame

class Bullet:
    def __init__(self, x, y, dx, dy, from_player=True):
        self.rect = pygame.Rect(x, y, 6, 12)
        self.dx = dx
        self.dy = dy
        self.from_player = from_player
        self.color = (0, 255, 255) if from_player else (255, 0, 255)

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
