# screens/game_screen.py – основной игровой экран
#
# run() описывает один кадр игры на самом верхнем уровне: ввод -> мячи ->
# бонусы -> лазеры -> проверка победы -> отрисовка. Вся "механика" каждого
# шага вынесена в отдельные функции ниже, чтобы run() можно было читать
# как оглавление, а не как одну большую простыню кода.
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

def _handle_ball_vs_paddle(ball, paddle):
    """Отскок от платформы: угол вылета зависит от точки удара, а не только от стороны."""
    _bounce_off_rect(ball, paddle.rect)
    offset = (ball.rect.centerx - paddle.rect.centerx) / (paddle.rect.width / 2)
    ball.vx = max(-MAX_BALL_SPEED_X, min(MAX_BALL_SPEED_X, offset * MAX_BALL_SPEED_X))

def _handle_ball_vs_bricks(ball, bricks, bonuses):
    """Отскакивает мяч от кирпичей, по пути разрушая их. Возвращает заработанные очки."""
    scored = 0
    for brick in bricks[:]:  # копия списка: brick.remove() ниже меняет оригинал
        if not ball.rect.colliderect(brick.rect):
            continue
        _bounce_off_rect(ball, brick.rect)
        if brick.hp == -1:          # стена — неразрушима, только отскок
            continue
        bonus_type = brick.hit()
        audio.play_sound(audio.hit_sound)
        if brick.hp <= 0:           # кирпич уничтожен
            bricks.remove(brick)
            scored += 10
            if bonus_type:
                bonuses.append(Bonus(brick.rect.center, bonus_type))
    return scored

def _update_balls(balls, paddle, bricks, bonuses):
    """Двигает все мячи и обрабатывает их столкновения. Возвращает заработанные очки."""
    scored = 0
    for ball in balls[:]:
        ball.update()
        if ball.rect.colliderect(paddle.rect) and ball.vy > 0:
            _handle_ball_vs_paddle(ball, paddle)
        scored += _handle_ball_vs_bricks(ball, bricks, bonuses)
        if ball.rect.top > HEIGHT:   # мяч улетел за нижний край поля — потерян
            balls.remove(ball)
    return scored

def _apply_bonus(bonus_type, paddle, balls, lives):
    """Применяет эффект подобранного бонуса. Возвращает обновлённое число жизней."""
    if bonus_type == 'extend':
        paddle.extend()
    elif bonus_type == 'multiball':
        balls.append(_new_ball(paddle))
    elif bonus_type == 'laser':
        paddle.laser = True
    elif bonus_type == 'extra_life':
        lives += 1
    return lives

def _update_bonuses(bonuses, paddle, balls, lives):
    """Двигает падающие бонусы и ловит их платформой. Возвращает обновлённое число жизней."""
    for bonus in bonuses[:]:
        bonus.update()
        if bonus.rect.colliderect(paddle.rect):
            bonuses.remove(bonus)
            audio.play_sound(audio.bonus_sound)
            lives = _apply_bonus(bonus.type, paddle, balls, lives)
        elif bonus.rect.top > HEIGHT:
            bonuses.remove(bonus)
    return lives

def _update_lasers(lasers, bricks, bonuses):
    """Двигает лазерные выстрелы и обрабатывает попадания в кирпичи. Возвращает очки."""
    scored = 0
    for laser in lasers[:]:
        laser.update()
        hit_brick = False
        for brick in bricks[:]:
            if brick.hp == -1 or not laser.rect.colliderect(brick.rect):
                continue
            bonus_type = brick.hit()
            audio.play_sound(audio.hit_sound)
            if brick.hp <= 0:
                bricks.remove(brick)
                scored += 10
                if bonus_type:
                    bonuses.append(Bonus(brick.rect.center, bonus_type))
            hit_brick = True
            break
        if hit_brick or laser.rect.bottom < 0:
            lasers.remove(laser)
    return scored

def _level_cleared(bricks):
    """Уровень пройден, когда среди кирпичей остались только неразрушимые стены (hp == -1)."""
    return not any(brick.hp != -1 for brick in bricks)

def _draw_frame(screen, font, paddle, balls, bricks, bonuses, lasers, score, lives):
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

def run(screen, clock, level):
    font = pygame.font.Font(None, 36)

    bricks, _rows, _cols = load_level(f"levels/level{level}.txt")
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

        score += _update_balls(balls, paddle, bricks, bonuses)

        if not balls:
            lives -= 1
            if lives <= 0:
                return GAMEOVER
            balls.append(_new_ball(paddle))

        lives = _update_bonuses(bonuses, paddle, balls, lives)
        score += _update_lasers(lasers, bricks, bonuses)

        if _level_cleared(bricks):
            return WIN

        _draw_frame(screen, font, paddle, balls, bricks, bonuses, lasers, score, lives)
        pygame.display.flip()
        clock.tick(FPS)
