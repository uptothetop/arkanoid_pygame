# screens/menu.py – главное меню
import pygame
from settings import *
from game.audio import play_music

def run(screen, clock):
    play_music()
    font = pygame.font.Font(None, 74)
    title = font.render("ARCANOID", True, WHITE)
    font_small = pygame.font.Font(None, 36)

    buttons = [
        {"text": "Играть", "rect": pygame.Rect(300, 250, 200, 50)},
        {"text": "Настройки", "rect": pygame.Rect(300, 320, 200, 50)},
        {"text": "Выход", "rect": pygame.Rect(300, 390, 200, 50)},
    ]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return QUIT
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                for btn in buttons:
                    if btn["rect"].collidepoint(pos):
                        if btn["text"] == "Играть":
                            return GAME
                        elif btn["text"] == "Настройки":
                            return SETTINGS
                        elif btn["text"] == "Выход":
                            return QUIT

        screen.fill(BLACK)
        screen.blit(title, title.get_rect(centerx=WIDTH//2, y=100))
        for btn in buttons:
            pygame.draw.rect(screen, GRAY, btn["rect"], border_radius=8)
            text = font_small.render(btn["text"], True, WHITE)
            screen.blit(text, text.get_rect(center=btn["rect"].center))
        pygame.display.flip()
        clock.tick(FPS)
