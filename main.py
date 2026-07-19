# main.py – точка входа, конечный автомат экранов
#
# Каждый экран — это функция run(screen, clock) -> следующее состояние
# (экран GAME дополнительно принимает номер уровня). Главный цикл просто
# вызывает функцию текущего состояния и переходит в то состояние, которое
# она вернула.
import pygame
from settings import *
from game.audio import init_audio, stop_music
from screens.menu import run as menu_screen
from screens.settings import run as settings_screen
from screens.game_screen import run as game_screen
from screens.win import run as win_screen
from screens.gameover import run as gameover_screen


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Arkanoid")
    clock = pygame.time.Clock()
    init_audio()

    state = MAIN_MENU
    level = 1

    while state != QUIT:
        if state == MAIN_MENU:
            state = menu_screen(screen, clock)
            if state == GAME:
                level = 1  # начинаем с первого уровня
        elif state == SETTINGS:
            state = settings_screen(screen, clock)
        elif state == GAME:
            # TODO: при переходе в WIN можно увеличивать level, если появятся новые уровни
            state = game_screen(screen, clock, level)
        elif state == WIN:
            state = win_screen(screen, clock)
        elif state == GAMEOVER:
            state = gameover_screen(screen, clock)
        else:
            state = QUIT

    stop_music()
    pygame.quit()


if __name__ == "__main__":
    main()
