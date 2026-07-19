# game/level.py – загрузка уровня
from settings import *
from game.entities import Brick

def load_level(filename):
    """
    Читает файл уровня, возвращает список кирпичей (включая автоматические стены),
    количество строк и столбцов сетки.
    """
    bricks = []
    with open(filename, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]
    rows = len(lines)
    cols = max(len(line.split()) for line in lines)

    # Создаём кирпичи из сетки
    for r, line in enumerate(lines):
        tokens = line.split()
        for c, token in enumerate(tokens):
            if token == '.':      # пустое место
                continue
            if token.isdigit() or (token.startswith('-') and token[1:].isdigit()):
                hp = int(token)
                if hp in (0, 1, 2):
                    bricks.append(Brick(c, r, hp))

    # Автоматические границы (hp = -1)
    # Верхняя стена (row = -1)
    for c in range(cols):
        bricks.append(Brick(c, -1, -1))
    # Левая стена (col = -1)
    for r in range(rows):
        bricks.append(Brick(-1, r, -1))
    # Правая стена (col = cols)
    for r in range(rows):
        bricks.append(Brick(cols, r, -1))

    return bricks, rows, cols
