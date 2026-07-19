# game/audio.py – менеджер звуков
import pygame

sound_enabled = True  # глобальный флаг, меняется из настроек
hit_sound = bonus_sound = laser_sound = None

def init_audio():
    pygame.mixer.init()
    # Загружаем звуки (лучше .wav, но можно и .mp3)
    global hit_sound, bonus_sound, laser_sound
    try:
        hit_sound = pygame.mixer.Sound('assets/hit.mp3')
        bonus_sound = pygame.mixer.Sound('assets/bonus.mp3')
        laser_sound = pygame.mixer.Sound('assets/laser.mp3')
    except:
        print("Не удалось загрузить звуки, проверьте файлы в assets/")

def play_sound(sound):
    if sound_enabled and sound is not None:
        sound.play()

def play_music():
    if sound_enabled:
        pygame.mixer.music.load('assets/music.mp3')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)   # бесконечно

def stop_music():
    pygame.mixer.music.stop()

def toggle_sound():
    global sound_enabled
    sound_enabled = not sound_enabled
    if sound_enabled:
        pygame.mixer.music.unpause()
    else:
        pygame.mixer.music.pause()