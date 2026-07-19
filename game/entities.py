"""game/entities.py – игровые объекты: платформа, мяч, кирпичи, бонусы, лазер."""

import random
from collections import deque

import pygame

import settings as cfg


class Paddle:
    """Платформа игрока: двигается по горизонтали и ловит мяч."""

    def __init__(self) -> None:
        self.rect = pygame.Rect(0, 0, cfg.PADDLE_WIDTH, cfg.PADDLE_HEIGHT)
        self.rect.midbottom = (cfg.WIDTH // 2, cfg.HEIGHT - 20)
        self.speed = cfg.PADDLE_SPEED
        self.vx = 0
        self.extended = False
        self.laser = False

    def move(self, keys: pygame.key.ScancodeWrapper) -> None:
        self.vx = 0
        if keys[pygame.K_LEFT]:
            self.vx = -self.speed
        elif keys[pygame.K_RIGHT]:
            self.vx = self.speed
        self.rect.x += self.vx
        if self.rect.left < cfg.FIELD_LEFT:
            self.rect.left = cfg.FIELD_LEFT
        if self.rect.right > cfg.FIELD_RIGHT:
            self.rect.right = cfg.FIELD_RIGHT

    def extend(self) -> None:
        if not self.extended:
            self.rect.width *= 2
            self.extended = True

    def shrink(self) -> None:
        if self.extended:
            self.rect.width //= 2
            self.extended = False

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(screen, cfg.PADDLE_COLOR, self.rect, border_radius=5)


class Ball:
    """Мяч: летит по прямой между столкновениями, отскакивая от rect'ов."""

    def __init__(self, x: int, y: int) -> None:
        self.radius = cfg.BALL_RADIUS
        self.rect = pygame.Rect(x - self.radius, y - self.radius, 2 * self.radius, 2 * self.radius)
        self.vx = cfg.BALL_SPEED_X
        self.vy = cfg.BALL_SPEED_Y
        # deque(maxlen=...) сам выкидывает старые точки за O(1) — не нужно
        # вручную обрезать список кадр за кадром, как пришлось бы с list.pop(0)
        self.trail: deque[tuple[int, int]] = deque(maxlen=cfg.TRAIL_LENGTH)

    def update(self) -> None:
        self.trail.append(self.rect.center)
        self.rect.x += self.vx
        self.rect.y += self.vy

    def draw(self, screen: pygame.Surface) -> None:
        trail_len = len(self.trail)
        for i, pos in enumerate(self.trail):
            fade = (i + 1) / (trail_len + 1)  # старые точки темнее
            color = tuple(int(channel * fade) for channel in cfg.BALL_COLOR)
            radius = max(1, round(self.radius * fade))
            pygame.draw.circle(screen, color, pos, radius)
        pygame.draw.circle(screen, cfg.BALL_COLOR, self.rect.center, self.radius)


class Brick:
    """
    Один кирпич сетки уровня.
    hp = -1     → стена, неразрушима
    hp =  0     → разрушается с одного удара
    hp =  1, 2  → выдерживает несколько ударов, меняя цвет
    """

    def __init__(self, col: int, row: int, hp: int) -> None:
        self.hp = hp
        self.max_hp = hp if hp > 0 else 0
        self.color = cfg.BRICK_COLORS[hp]
        self.rect = pygame.Rect(
            cfg.FIELD_LEFT + col * cfg.BRICK_WIDTH,
            cfg.TOP_OFFSET + row * cfg.BRICK_HEIGHT,
            cfg.BRICK_WIDTH,
            cfg.BRICK_HEIGHT,
        )

    def hit(self) -> str | None:
        """Удар по кирпичу. Возвращает тип бонуса или None."""
        if self.hp > 0:  # только разрушаемые
            self.hp -= 1
            if self.hp > 0:
                self.color = cfg.BRICK_COLORS[self.hp]
                return None
            # hp стало 0 — кирпич уничтожен, есть шанс выпадения бонуса
            if random.random() < cfg.BONUS_PROBABILITY:
                return random.choice(cfg.BONUS_TYPES)
        return None

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, cfg.DARK_GRAY, self.rect, 2)  # рамка


class Bonus:
    """Бонус, выпавший из разрушенного кирпича; падает вниз, пока его не поймает платформа."""

    TYPES = {
        "extend": {"color": cfg.GREEN, "letter": "E"},
        "multiball": {"color": cfg.MAGENTA, "letter": "M"},
        "laser": {"color": cfg.YELLOW, "letter": "L"},
        "extra_life": {"color": cfg.CYAN, "letter": "1"},
    }

    _label_font: pygame.font.Font | None = None  # создаётся лениво, см. _get_label_font

    def __init__(self, center: tuple[int, int], bonus_type: str) -> None:
        self.type = bonus_type
        self.rect = pygame.Rect(0, 0, 24, 24)
        self.rect.center = center
        self.vy = 3
        props = Bonus.TYPES[bonus_type]
        self.color = props["color"]
        self.letter = props["letter"]

    @classmethod
    def _get_label_font(cls) -> pygame.font.Font:
        # pygame.font.Font(...) нельзя создать до pygame.init(), поэтому его
        # нельзя объявить прямо в теле класса при импорте модуля — только
        # лениво, при первом реальном вызове draw().
        if cls._label_font is None:
            cls._label_font = pygame.font.Font(None, 24)
        return cls._label_font

    def update(self) -> None:
        self.rect.y += self.vy

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(screen, self.color, self.rect, border_radius=5)
        text = self._get_label_font().render(self.letter, True, cfg.BLACK)
        screen.blit(text, text.get_rect(center=self.rect.center))


class LaserBullet:
    """Выстрел платформы после подбора бонуса 'laser'; летит вверх и разрушает кирпичи."""

    def __init__(self, x: int, y: int) -> None:
        self.rect = pygame.Rect(x - 2, y, 4, 10)
        self.vy = -10

    def update(self) -> None:
        self.rect.y += self.vy

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(screen, cfg.YELLOW, self.rect)
