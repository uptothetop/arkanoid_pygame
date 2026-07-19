# game/particles.py – частицы для эффектов разрушения (пиксельные искры)
#
# Частиц может быть много одновременно (несколько мячей/лазеров одновременно
# бьют по кирпичам), поэтому важны простые решения:
#   - Particle использует __slots__ — без __dict__ на каждый экземпляр;
#   - затухание делается уменьшением размера, а не альфа-смешиванием —
#     не нужна отдельная поверхность с SRCALPHA, которая заметно дороже
#     обычного pygame.draw.rect на CPU-рендере pygame;
#   - общее число частиц ограничено MAX_PARTICLES.
import math
import random

import pygame

from settings import (
    MAX_PARTICLES,
    PARTICLE_COUNT,
    PARTICLE_GRAVITY,
    PARTICLE_LIFETIME,
    PARTICLE_SPEED,
)


class Particle:
    __slots__ = ("x", "y", "vx", "vy", "color", "size", "life", "max_life")

    def __init__(self, x, y, color):
        angle = random.uniform(0, math.tau)
        speed = random.uniform(*PARTICLE_SPEED)
        self.x = x
        self.y = y
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.color = color
        self.size = random.randint(2, 4)
        self.max_life = random.randint(*PARTICLE_LIFETIME)
        self.life = self.max_life

    @property
    def alive(self):
        return self.life > 0

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += PARTICLE_GRAVITY
        self.life -= 1

    def draw(self, screen):
        fade = self.life / self.max_life
        size = max(1, round(self.size * fade))
        pygame.draw.rect(screen, self.color, (int(self.x), int(self.y), size, size))


def spawn_burst(particles, center, color, count=PARTICLE_COUNT):
    """Добавляет count частиц в список particles (список изменяется на месте)."""
    x, y = center
    particles.extend(Particle(x, y, color) for _ in range(count))
    overflow = len(particles) - MAX_PARTICLES
    if overflow > 0:
        del particles[:overflow]  # первыми гаснут самые старые частицы


def update_particles(particles):
    """Обновляет частицы на месте и убирает умершие."""
    for particle in particles[:]:  # копия списка: remove() ниже меняет оригинал
        particle.update()
        if not particle.alive:
            particles.remove(particle)


def draw_particles(screen, particles):
    for particle in particles:
        particle.draw(screen)
