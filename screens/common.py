# screens/common.py – общие для всех экранов вспомогательные функции
#
# screens/menu.py, settings.py, win.py и gameover.py устроены одинаково:
# заполнить фон, нарисовать пару кнопок-прямоугольников с подписью и ждать
# клика. Этот модуль вынесен, чтобы не повторять один и тот же код рисования
# кнопки в каждом файле.
import pygame
from settings import *


def draw_button(screen, rect, text, font, color=GRAY, text_color=WHITE):
    """Рисует прямоугольную кнопку с текстом по центру."""
    pygame.draw.rect(screen, color, rect, border_radius=8)
    label = font.render(text, True, text_color)
    screen.blit(label, label.get_rect(center=rect.center))


def result_screen(screen, clock, title_text, title_color):
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
                return QUIT
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if menu_btn.collidepoint(event.pos):
                    return MAIN_MENU

        screen.fill(BLACK)
        title = title_font.render(title_text, True, title_color)
        screen.blit(title, title.get_rect(centerx=WIDTH // 2, y=150))
        draw_button(screen, menu_btn, "В меню", button_font)

        pygame.display.flip()
        clock.tick(FPS)
