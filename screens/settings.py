# screens/settings.py – настройки звука
import pygame
from settings import *
import game.audio as audio
from game.audio import toggle_sound, play_sound

def run(screen, clock):
    font = pygame.font.Font(None, 48)
    font_small = pygame.font.Font(None, 36)

    back_btn = pygame.Rect(50, 500, 150, 50)
    toggle_btn = pygame.Rect(300, 250, 200, 50)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return QUIT
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                if back_btn.collidepoint(pos):
                    return MAIN_MENU
                if toggle_btn.collidepoint(pos):
                    toggle_sound()
                    play_sound(audio.hit_sound)  # звук клика для проверки

        screen.fill(BLACK)
        title = font.render("Настройки", True, WHITE)
        screen.blit(title, title.get_rect(centerx=WIDTH//2, y=100))

        # Кнопка переключения звука
        pygame.draw.rect(screen, GRAY, toggle_btn, border_radius=8)
        sound_text = "Звук: ВКЛ" if audio.sound_enabled else "Звук: ВЫКЛ"
        txt = font_small.render(sound_text, True, WHITE)
        screen.blit(txt, txt.get_rect(center=toggle_btn.center))

        # Кнопка "Назад"
        pygame.draw.rect(screen, GRAY, back_btn, border_radius=8)
        back_txt = font_small.render("Назад", True, WHITE)
        screen.blit(back_txt, back_txt.get_rect(center=back_btn.center))

        pygame.display.flip()
        clock.tick(FPS)
