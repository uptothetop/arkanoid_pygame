# screens/win.py – экран победы
from settings import GREEN
from screens.common import result_screen

def run(screen, clock):
    return result_screen(screen, clock, "ПОБЕДА!", GREEN)
