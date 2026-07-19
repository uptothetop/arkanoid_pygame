# settings.py – константы игры
WIDTH, HEIGHT = 800, 600
FPS = 60

# Состояния конечного автомата экранов
MAIN_MENU = 0
SETTINGS = 1
GAME = 2
WIN = 3
GAMEOVER = 4
QUIT = 5

BRICK_WIDTH, BRICK_HEIGHT = 60, 20
TOP_OFFSET = 60  # отступ сверху для UI и верхней границы
FIELD_LEFT = 40  # левый отступ для кирпичей

# Игровое поле фиксированного размера — не зависит от конкретного уровня
FIELD_COLS = (WIDTH - 2 * FIELD_LEFT) // BRICK_WIDTH
FIELD_RIGHT = FIELD_LEFT + FIELD_COLS * BRICK_WIDTH

PADDLE_WIDTH, PADDLE_HEIGHT = 100, 12
PADDLE_SPEED = 7

BALL_RADIUS = 8
BALL_SPEED_X = 4
BALL_SPEED_Y = -5
SLIDE_FACTOR = 0.8
MAX_BALL_SPEED_X = 8

BONUS_PROBABILITY = 0.3  # шанс выпадения бонуса из разрушаемого кирпича
BONUS_TYPES = ["extend", "multiball", "laser", "extra_life"]

# Визуальные эффекты
TRAIL_LENGTH = 6  # сколько прошлых позиций мяча хранить для трейла
PARTICLE_COUNT = 10  # частиц в одном взрыве кирпича
PARTICLE_LIFETIME = (12, 24)  # мин/макс кадров жизни частицы
PARTICLE_SPEED = (1.5, 4.0)  # мин/макс начальная скорость частицы
PARTICLE_GRAVITY = 0.15  # ускорение вниз, кадр за кадром
MAX_PARTICLES = 200  # предохранитель: не даёт частицам разрастись при частых взрывах

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)
DARK_GRAY = (60, 60, 60)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
PADDLE_COLOR = CYAN
BALL_COLOR = WHITE

# Соответствие hp -> цвет
BRICK_COLORS = {
    2: ORANGE,
    1: RED,
    0: GRAY,
    -1: DARK_GRAY,  # стена
}
