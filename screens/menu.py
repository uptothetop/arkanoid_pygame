"""screens/menu.py – главное меню."""

import pygame

import game.audio as audio
import settings as cfg
from game.states import GameState
from screens.common import draw_button


def run(screen: pygame.Surface, clock: pygame.time.Clock) -> GameState:
    audio.play_music()
    title_font = pygame.font.Font(None, 74)
    button_font = pygame.font.Font(None, 36)
    title = title_font.render("ARCANOID", True, cfg.WHITE)

    # У каждой кнопки уже записано, в какое состояние переходить по клику
    buttons = [
        ("Играть", pygame.Rect(300, 250, 200, 50), GameState.GAME),
        ("Настройки", pygame.Rect(300, 320, 200, 50), GameState.SETTINGS),
        ("Выход", pygame.Rect(300, 390, 200, 50), GameState.QUIT),
    ]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GameState.QUIT
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for _text, rect, next_state in buttons:
                    if rect.collidepoint(event.pos):
                        return next_state

        screen.fill(cfg.BLACK)
        screen.blit(title, title.get_rect(centerx=cfg.WIDTH // 2, y=100))
        for text, rect, _next_state in buttons:
            draw_button(screen, rect, text, button_font)

        pygame.display.flip()
        clock.tick(cfg.FPS)
