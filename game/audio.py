"""game/audio.py – менеджер звуков."""

import pygame

import settings as cfg

sound_enabled = True  # глобальный флаг, меняется из настроек

# Заранее объявлены как None: реальные Sound-объекты создаются только внутри
# init_audio() (там, где уже вызван pygame.mixer.init()). Без этой заглушки
# "import game.audio as audio; audio.hit_sound" падал бы с AttributeError,
# если обратиться к нему раньше, чем main() успевает вызвать init_audio().
hit_sound: pygame.mixer.Sound | None = None
bonus_sound: pygame.mixer.Sound | None = None
laser_sound: pygame.mixer.Sound | None = None


def init_audio() -> None:
    global hit_sound, bonus_sound, laser_sound
    pygame.mixer.init()
    try:
        hit_sound = pygame.mixer.Sound(cfg.ASSETS_DIR / "hit.mp3")
        bonus_sound = pygame.mixer.Sound(cfg.ASSETS_DIR / "bonus.mp3")
        laser_sound = pygame.mixer.Sound(cfg.ASSETS_DIR / "laser.mp3")
    except pygame.error:
        print("Не удалось загрузить звуки, проверьте файлы в assets/")


def play_sound(sound: pygame.mixer.Sound | None) -> None:
    if sound_enabled and sound is not None:
        sound.play()


def play_music() -> None:
    if sound_enabled:
        pygame.mixer.music.load(cfg.ASSETS_DIR / "music.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)  # бесконечно


def stop_music() -> None:
    pygame.mixer.music.stop()


def toggle_sound() -> None:
    global sound_enabled
    sound_enabled = not sound_enabled
    if sound_enabled:
        pygame.mixer.music.unpause()
    else:
        pygame.mixer.music.pause()
