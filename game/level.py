"""game/level.py – загрузка уровня из текстового файла сетки."""

import settings as cfg
from game.entities import Brick


def load_level(level_number: int) -> tuple[list[Brick], int, int]:
    """
    Читает levels/level{level_number}.txt, возвращает список кирпичей
    (включая автоматические стены) и размеры сетки, заданные в файле
    (количество строк и столбцов).
    """
    path = cfg.LEVELS_DIR / f"level{level_number}.txt"
    with path.open(encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    rows = len(lines)
    cols = max(len(line.split()) for line in lines)

    bricks: list[Brick] = []
    for r, line in enumerate(lines):
        tokens = line.split()
        for c, token in enumerate(tokens):
            if token == ".":  # пустое место
                continue
            if token.isdigit() or (token.startswith("-") and token[1:].isdigit()):
                hp = int(token)
                if hp in (0, 1, 2):
                    bricks.append(Brick(c, r, hp))

    # Автоматические границы (hp = -1) — всегда по краям игрового поля,
    # независимо от ширины конкретного уровня
    wall_rows = (cfg.HEIGHT - cfg.TOP_OFFSET) // cfg.BRICK_HEIGHT + 2

    # Верхняя стена (row = -1)
    for c in range(cfg.FIELD_COLS):
        bricks.append(Brick(c, -1, -1))
    # Левая и правая стены — от верха до самого низа экрана
    for r in range(-1, wall_rows):
        bricks.append(Brick(-1, r, -1))
        bricks.append(Brick(cfg.FIELD_COLS, r, -1))

    return bricks, rows, cols
