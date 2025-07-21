import pygame

class Player:
    def __init__(self, x, y, size, speed, screen_width, screen_height):
        self.rect = pygame.Rect(x, y, size, size)
        self.speed = speed
        self.screen_width = screen_width
        self.screen_height = screen_height

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < self.screen_width:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < self.screen_height:
            self.rect.y += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 255), self.rect)
    
    def shoot(self):
        # Centro superior del jugador
        x = self.rect.centerx
        y = self.rect.top
        from bullet import Bullet
        return Bullet(x, y, radius=6, speed=8, color=(0, 255, 255), direction=-1)

    def get_position(self):
        return self.rect.center
