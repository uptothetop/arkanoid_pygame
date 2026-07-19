"""game/particles.py – частицы для эффектов разрушения (пиксельные искры).

Частиц может быть много одновременно (несколько мячей/лазеров одновременно
бьют по кирпичам), поэтому важны простые решения:
  - Particle использует __slots__ — без __dict__ на каждый экземпляр;
  - затухание делается уменьшением размера, а не альфа-смешиванием — не
    нужна отдельная поверхность с SRCALPHA, которая заметно дороже обычного
    pygame.draw.rect на CPU-рендере pygame;
  - общее число частиц ограничено MAX_PARTICLES.
"""

import math
import random

import pygame

import settings as cfg

Color = tuple[int, int, int]


class Particle:
    __slots__ = ("x", "y", "vx", "vy", "color", "size", "life", "max_life")

    def __init__(self, x: float, y: float, color: Color) -> None:
        angle = random.uniform(0, math.tau)
        speed = random.uniform(*cfg.PARTICLE_SPEED)
        self.x = x
        self.y = y
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.color = color
        self.size = random.randint(2, 4)
        self.max_life = random.randint(*cfg.PARTICLE_LIFETIME)
        self.life = self.max_life

    @property
    def alive(self) -> bool:
        return self.life > 0

    def update(self) -> None:
        self.x += self.vx
        self.y += self.vy
        self.vy += cfg.PARTICLE_GRAVITY
        self.life -= 1

    def draw(self, screen: pygame.Surface) -> None:
        fade = self.life / self.max_life
        size = max(1, round(self.size * fade))
        pygame.draw.rect(screen, self.color, (int(self.x), int(self.y), size, size))


def spawn_burst(
    particles: list[Particle],
    center: tuple[int, int],
    color: Color,
    count: int = cfg.PARTICLE_COUNT,
) -> None:
    """Добавляет count частиц в список particles (список изменяется на месте)."""
    x, y = center
    particles.extend(Particle(x, y, color) for _ in range(count))
    overflow = len(particles) - cfg.MAX_PARTICLES
    if overflow > 0:
        del particles[:overflow]  # первыми гаснут самые старые частицы


def update_particles(particles: list[Particle]) -> None:
    """Обновляет частицы на месте и убирает умершие."""
    for particle in particles[:]:  # копия списка: remove() ниже меняет оригинал
        particle.update()
        if not particle.alive:
            particles.remove(particle)


def draw_particles(screen: pygame.Surface, particles: list[Particle]) -> None:
    for particle in particles:
        particle.draw(screen)
