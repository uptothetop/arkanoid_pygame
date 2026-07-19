# screens/settings.py – настройки звука
import pygame
from settings import *
import game.audio as audio
from game.audio import toggle_sound, play_sound
from screens.common import draw_button


def run(screen, clock):
    title_font = pygame.font.Font(None, 48)
    button_font = pygame.font.Font(None, 36)

    back_btn = pygame.Rect(50, 500, 150, 50)
    toggle_btn = pygame.Rect(300, 250, 200, 50)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return QUIT
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if back_btn.collidepoint(event.pos):
                    return MAIN_MENU
                if toggle_btn.collidepoint(event.pos):
                    toggle_sound()
                    play_sound(audio.hit_sound)  # звук клика для проверки

        screen.fill(BLACK)
        title = title_font.render("Настройки", True, WHITE)
        screen.blit(title, title.get_rect(centerx=WIDTH // 2, y=100))

        sound_text = "Звук: ВКЛ" if audio.sound_enabled else "Звук: ВЫКЛ"
        draw_button(screen, toggle_btn, sound_text, button_font)
        draw_button(screen, back_btn, "Назад", button_font)

        pygame.display.flip()
        clock.tick(FPS)
