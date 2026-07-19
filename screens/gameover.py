# screens/gameover.py – экран поражения
import pygame
from settings import *

def run(screen, clock):
    font = pygame.font.Font(None, 74)
    font_small = pygame.font.Font(None, 36)

    retry_btn = pygame.Rect(300, 350, 200, 50)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return QUIT
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                if retry_btn.collidepoint(pos):
                    return MAIN_MENU

        screen.fill(BLACK)
        title = font.render("GAME OVER", True, RED)
        screen.blit(title, title.get_rect(centerx=WIDTH//2, y=150))

        pygame.draw.rect(screen, GRAY, retry_btn, border_radius=8)
        retry_text = font_small.render("В меню", True, WHITE)
        screen.blit(retry_text, retry_text.get_rect(center=retry_btn.center))

        pygame.display.flip()
        clock.tick(FPS)
