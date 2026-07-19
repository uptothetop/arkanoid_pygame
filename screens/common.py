"""screens/common.py – общие для всех экранов вспомогательные функции.

menu.py, settings.py, win.py и gameover.py устроены одинаково: залить фон,
нарисовать пару кнопок-прямоугольников с подписью и подождать клика. Этот
модуль вынесен, чтобы не повторять код рисования кнопки и целый
экран-результат в каждом файле.
"""

import pygame

import settings as cfg
from game.states import GameState

Color = tuple[int, int, int]


def draw_button(
    screen: pygame.Surface,
    rect: pygame.Rect,
    text: str,
    font: pygame.font.Font,
    color: Color = cfg.GRAY,
    text_color: Color = cfg.WHITE,
) -> None:
    """Рисует прямоугольную кнопку с текстом по центру."""
    pygame.draw.rect(screen, color, rect, border_radius=8)
    label = font.render(text, True, text_color)
    screen.blit(label, label.get_rect(center=rect.center))


def result_screen(
    screen: pygame.Surface,
    clock: pygame.time.Clock,
    title_text: str,
    title_color: Color,
) -> GameState:
    """
    Экран-заглушка с крупным заголовком и кнопкой "В меню".
    Общий код для экранов победы (win.py) и поражения (gameover.py) —
    они отличаются только текстом и цветом заголовка.
    """
    title_font = pygame.font.Font(None, 74)
    button_font = pygame.font.Font(None, 36)
    menu_btn = pygame.Rect(300, 350, 200, 50)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GameState.QUIT
            if (
                event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and menu_btn.collidepoint(event.pos)
            ):
                return GameState.MAIN_MENU

        screen.fill(cfg.BLACK)
        title = title_font.render(title_text, True, title_color)
        screen.blit(title, title.get_rect(centerx=cfg.WIDTH // 2, y=150))
        draw_button(screen, menu_btn, "В меню", button_font)

        pygame.display.flip()
        clock.tick(cfg.FPS)
