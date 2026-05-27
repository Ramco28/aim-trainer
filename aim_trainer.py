import pygame
import random
import time

pygame.init()

WIDTH, HEIGHT = 900, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aim Trainer")

BG_COLOR = (20, 20, 20)
TARGET_COLOR = (255, 80, 80)
TEXT_COLOR = (255, 255, 255)

FONT = pygame.font.SysFont("arial", 28)
BIG_FONT = pygame.font.SysFont("arial", 48)

TARGET_RADIUS = 30
GAME_TIME = 30


def new_target():
    x = random.randint(TARGET_RADIUS, WIDTH - TARGET_RADIUS)
    y = random.randint(TARGET_RADIUS + 60, HEIGHT - TARGET_RADIUS)
    return x, y


def draw(target, score, clicks, start_time):
    WIN.fill(BG_COLOR)

    elapsed = time.time() - start_time
    time_left = max(0, GAME_TIME - int(elapsed))

    accuracy = 0 if clicks == 0 else round((score / clicks) * 100, 1)

    info = FONT.render(
        f"Score: {score}   Clicks: {clicks}   Accuracy: {accuracy}%   Time: {time_left}s",
        True,
        TEXT_COLOR
    )
    WIN.blit(info, (20, 20))

    pygame.draw.circle(WIN, TARGET_COLOR, target, TARGET_RADIUS)

    pygame.display.update()


def end_screen(score, clicks):
    accuracy = 0 if clicks == 0 else round((score / clicks) * 100, 1)

    WIN.fill(BG_COLOR)

    title = BIG_FONT.render("Game Over", True, TEXT_COLOR)
    stats = FONT.render(f"Score: {score} | Clicks: {clicks} | Accuracy: {accuracy}%", True, TEXT_COLOR)
    restart = FONT.render("Press R to restart or Q to quit", True, TEXT_COLOR)

    WIN.blit(title, (WIDTH // 2 - title.get_width() // 2, 200))
    WIN.blit(stats, (WIDTH // 2 - stats.get_width() // 2, 280))
    WIN.blit(restart, (WIDTH // 2 - restart.get_width() // 2, 340))

    pygame.display.update()


def main():
    running = True
    target = new_target()
    score = 0
    clicks = 0
    start_time = time.time()

    while running:
        elapsed = time.time() - start_time

        if elapsed >= GAME_TIME:
            end_screen(score, clicks)

            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            main()
                            return
                        elif event.key == pygame.K_q:
                            pygame.quit()
                            return

        draw(target, score, clicks, start_time)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                clicks += 1
                mouse_x, mouse_y = pygame.mouse.get_pos()

                target_x, target_y = target
                distance = ((mouse_x - target_x) ** 2 + (mouse_y - target_y) ** 2) ** 0.5

                if distance <= TARGET_RADIUS:
                    score += 1
                    target = new_target()

    pygame.quit()


if __name__ == "__main__":
    main()