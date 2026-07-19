# screens/game_screen.py – основной игровой экран
import pygame
from settings import *
import game.audio as audio
from game.entities import Paddle, Ball, Bonus, LaserBullet
from game.level import load_level

LASER_COOLDOWN = 300  # мс между выстрелами

def _new_ball(paddle):
    return Ball(paddle.rect.centerx, paddle.rect.top - BALL_RADIUS)

def _bounce_off_rect(ball, rect):
    """Отталкивает мяч от прямоугольника rect, определяя сторону удара."""
    overlap_left = ball.rect.right - rect.left
    overlap_right = rect.right - ball.rect.left
    overlap_top = ball.rect.bottom - rect.top
    overlap_bottom = rect.bottom - ball.rect.top

    min_overlap = min(overlap_left, overlap_right, overlap_top, overlap_bottom)
    if min_overlap == overlap_top and ball.vy > 0:
        ball.rect.bottom = rect.top
        ball.vy *= -1
    elif min_overlap == overlap_bottom and ball.vy < 0:
        ball.rect.top = rect.bottom
        ball.vy *= -1
    elif min_overlap == overlap_left and ball.vx > 0:
        ball.rect.right = rect.left
        ball.vx *= -1
    elif min_overlap == overlap_right and ball.vx < 0:
        ball.rect.left = rect.right
        ball.vx *= -1

def run(screen, clock, level):
    font = pygame.font.Font(None, 36)

    bricks, rows, cols = load_level(f"levels/level{level}.txt")
    paddle = Paddle()
    balls = [_new_ball(paddle)]
    bonuses = []
    lasers = []
    lives = 3
    score = 0
    last_shot = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return QUIT

        keys = pygame.key.get_pressed()
        paddle.move(keys)

        now = pygame.time.get_ticks()
        if keys[pygame.K_SPACE] and paddle.laser and now - last_shot > LASER_COOLDOWN:
            lasers.append(LaserBullet(paddle.rect.centerx, paddle.rect.top))
            last_shot = now

        # мяч(и)
        for ball in balls[:]:
            ball.update()

            if ball.rect.left <= 0 or ball.rect.right >= WIDTH:
                ball.vx *= -1
            if ball.rect.top <= 0:
                ball.vy *= -1

            if ball.rect.colliderect(paddle.rect) and ball.vy > 0:
                _bounce_off_rect(ball, paddle.rect)
                offset = (ball.rect.centerx - paddle.rect.centerx) / (paddle.rect.width / 2)
                ball.vx = max(-MAX_BALL_SPEED_X, min(MAX_BALL_SPEED_X, offset * MAX_BALL_SPEED_X))

            for brick in bricks[:]:
                if brick.hp == -1:
                    if ball.rect.colliderect(brick.rect):
                        _bounce_off_rect(ball, brick.rect)
                    continue
                if ball.rect.colliderect(brick.rect):
                    _bounce_off_rect(ball, brick.rect)
                    bonus_type = brick.hit()
                    audio.play_sound(audio.hit_sound)
                    if brick.hp <= 0:
                        bricks.remove(brick)
                        score += 10
                        if bonus_type:
                            bonuses.append(Bonus(brick.rect.center, bonus_type))

            if ball.rect.top > HEIGHT:
                balls.remove(ball)

        if not balls:
            lives -= 1
            if lives <= 0:
                return GAMEOVER
            balls.append(_new_ball(paddle))

        # бонусы
        for bonus in bonuses[:]:
            bonus.update()
            if bonus.rect.colliderect(paddle.rect):
                bonuses.remove(bonus)
                audio.play_sound(audio.bonus_sound)
                if bonus.type == 'extend':
                    paddle.extend()
                elif bonus.type == 'multiball':
                    balls.append(_new_ball(paddle))
                elif bonus.type == 'laser':
                    paddle.laser = True
                elif bonus.type == 'extra_life':
                    lives += 1
            elif bonus.rect.top > HEIGHT:
                bonuses.remove(bonus)

        # лазерные выстрелы
        for laser in lasers[:]:
            laser.update()
            hit_something = False
            for brick in bricks[:]:
                if brick.hp == -1:
                    continue
                if laser.rect.colliderect(brick.rect):
                    bonus_type = brick.hit()
                    audio.play_sound(audio.hit_sound)
                    if brick.hp <= 0:
                        bricks.remove(brick)
                        score += 10
                        if bonus_type:
                            bonuses.append(Bonus(brick.rect.center, bonus_type))
                    hit_something = True
                    break
            if hit_something or laser.rect.bottom < 0:
                lasers.remove(laser)

        # победа: не осталось разрушаемых кирпичей (не стен)
        if not any(brick.hp != -1 for brick in bricks):
            return WIN

        # отрисовка
        screen.fill(BLACK)
        paddle.draw(screen)
        for ball in balls:
            ball.draw(screen)
        for brick in bricks:
            brick.draw(screen)
        for bonus in bonuses:
            bonus.draw(screen)
        for laser in lasers:
            laser.draw(screen)

        hud = font.render(f"Очки: {score}   Жизни: {lives}", True, WHITE)
        screen.blit(hud, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)
