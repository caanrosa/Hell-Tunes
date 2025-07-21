from Bullet import Bullet
import pygame

class Player:
    def __init__(self, x, y, size, speed, screen_width, screen_height):
        self.rect = pygame.Rect(x, y, size, size)
        self.speed = speed
        self.bullets = []
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.cooldown = 0
        self.immunity_timer = 0
        self.immunity_duration = 20  # frames

    def update(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < self.screen_width:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < self.screen_height:
            self.rect.y += self.speed

        # Disparo
        if keys[pygame.K_SPACE] and self.cooldown == 0:
            self.shoot()
            self.cooldown = 10  # cooldown frames

        if self.cooldown > 0:
            self.cooldown -= 1

        # Inmunidad
        if self.immunity_timer > 0:
            self.immunity_timer -= 1

        # Actualizar balas
        for bullet in self.bullets:
            bullet.update()

        # Eliminar balas fuera de pantalla
        self.bullets = [b for b in self.bullets if b.rect.y >= 0]

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top, 0, -10, from_player=True)
        self.bullets.append(bullet)

    def draw(self, screen):
        color = (0, 255, 0) if self.immunity_timer == 0 else (0, 100, 0)
        pygame.draw.rect(screen, color, self.rect)
        for bullet in self.bullets:
            bullet.draw(screen)

    def take_damage(self):
        if self.immunity_timer == 0:
            self.immunity_timer = self.immunity_duration
            return True
        return False
