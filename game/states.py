"""game/states.py – состояния конечного автомата экранов.

Раньше состояния были обычными целыми константами (MAIN_MENU = 0 и т.д.).
IntEnum ведёт себя как обычное число (сравнение через ==, можно передавать
куда угодно), но при этом в отладчике, трейсбеке или логе видно осмысленное
имя — GameState.MAIN_MENU, а не безликий 0.
"""

from enum import IntEnum, auto


class GameState(IntEnum):
    MAIN_MENU = 0
    SETTINGS = auto()
    GAME = auto()
    WIN = auto()
    GAMEOVER = auto()
    QUIT = auto()
