# screens/menu.py – главное меню
import pygame
from settings import *
from game.audio import play_music
from screens.common import draw_button


def run(screen, clock):
    play_music()
    title_font = pygame.font.Font(None, 74)
    button_font = pygame.font.Font(None, 36)
    title = title_font.render("ARCANOID", True, WHITE)

    # У каждой кнопки уже записано, в какое состояние переходить по клику
    buttons = [
        ("Играть", pygame.Rect(300, 250, 200, 50), GAME),
        ("Настройки", pygame.Rect(300, 320, 200, 50), SETTINGS),
        ("Выход", pygame.Rect(300, 390, 200, 50), QUIT),
    ]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return QUIT
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for _text, rect, next_state in buttons:
                    if rect.collidepoint(event.pos):
                        return next_state

        screen.fill(BLACK)
        screen.blit(title, title.get_rect(centerx=WIDTH // 2, y=100))
        for text, rect, _next_state in buttons:
            draw_button(screen, rect, text, button_font)

        pygame.display.flip()
        clock.tick(FPS)
