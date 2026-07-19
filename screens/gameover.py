# screens/gameover.py – экран поражения
from settings import RED
from screens.common import result_screen

def run(screen, clock):
    return result_screen(screen, clock, "GAME OVER", RED)
