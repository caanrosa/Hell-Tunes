import pygame

class SoundManager:
    def __init__(self):
        pygame.mixer.init()

        # Ruta base de los sonidos
        base_path = "assets/sounds/"

        # Cargar sonidos individualmente
        self.sounds = {
            "player_shoot": pygame.mixer.Sound(base_path + "mus_sfx_a_bullet.wav"),
            "enemy_shoot": pygame.mixer.Sound(base_path + "snd_spearappear.wav"),
            "enemy_hit": pygame.mixer.Sound(base_path + "snd_mtt_hit.wav"),
            "player_hit": pygame.mixer.Sound(base_path + "snd_hurt1.wav"),
        }

        # Asignar volúmenes personalizados (0.0 a 1.0)
        self.sounds["player_shoot"].set_volume(0.02)
        self.sounds["enemy_shoot"].set_volume(0.08)
        self.sounds["enemy_hit"].set_volume(0.05)
        self.sounds["player_hit"].set_volume(0.05)

    def play(self, sound_name):
        if sound_name in self.sounds:
            self.sounds[sound_name].play()
