import random
import pygame

# Dodge the Falling Blocks
# Install Pygame first: python -m pip install pygame

pygame.init()

WIDTH, HEIGHT = 600, 700
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge the Falling Blocks")
clock = pygame.time.Clock()

WHITE = (245, 245, 245)
DARK = (22, 27, 40)
BLUE = (70, 160, 255)
RED = (245, 75, 85)
YELLOW = (255, 210, 70)
GRAY = (155, 165, 180)

font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 64)

PLAYER_W, PLAYER_H = 54, 24
PLAYER_SPEED = 7
BLOCK_SIZE = 34


def reset_game():
    player = pygame.Rect(WIDTH // 2 - PLAYER_W // 2, HEIGHT - 75, PLAYER_W, PLAYER_H)
    blocks = []
    score = 0
    spawn_timer = 0
    game_over = False
    return player, blocks, score, spawn_timer, game_over


player, blocks, score, spawn_timer, game_over = reset_game()
running = True

while running:
    dt = clock.tick(FPS)
    screen.fill(DARK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if game_over and event.key == pygame.K_r:
                player, blocks, score, spawn_timer, game_over = reset_game()

    keys = pygame.key.get_pressed()

    if not game_over:
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.x += PLAYER_SPEED

        player.x = max(0, min(WIDTH - PLAYER_W, player.x))

        # Spawn blocks more frequently as the score rises.
        spawn_timer += dt
        spawn_interval = max(260, 850 - score * 4)
        if spawn_timer >= spawn_interval:
            spawn_timer = 0
            x = random.randint(0, WIDTH - BLOCK_SIZE)
            speed = random.randint(4, 7) + min(score // 10, 8)
            blocks.append({
                "rect": pygame.Rect(x, -BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                "speed": speed
            })

        for block in blocks:
            block["rect"].y += block["speed"]

        blocks = [block for block in blocks if block["rect"].top < HEIGHT]

        for block in blocks:
            if player.colliderect(block["rect"]):
                game_over = True
                break

        score += dt / 1000

    # Draw a subtle grid.
    for x in range(0, WIDTH, 50):
        pygame.draw.line(screen, (31, 37, 52), (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, 50):
        pygame.draw.line(screen, (31, 37, 52), (0, y), (WIDTH, y))

    # Draw player and falling blocks.
    pygame.draw.rect(screen, BLUE, player, border_radius=8)
    pygame.draw.rect(screen, WHITE, (player.x + 10, player.y + 5, 7, 5), border_radius=2)
    pygame.draw.rect(screen, WHITE, (player.x + PLAYER_W - 17, player.y + 5, 7, 5), border_radius=2)

    for block in blocks:
        pygame.draw.rect(screen, RED, block["rect"], border_radius=6)
        pygame.draw.rect(screen, YELLOW, (block["rect"].x + 7, block["rect"].y + 7, 8, 8), border_radius=2)

    score_surface = font.render(f"Score: {int(score)}", True, WHITE)
    screen.blit(score_surface, (18, 18))
    help_surface = pygame.font.Font(None, 25).render("Move: ← → or A/D   |   ESC: Quit", True, GRAY)
    screen.blit(help_surface, (18, HEIGHT - 32))

    if game_over:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 175))
        screen.blit(overlay, (0, 0))

        title = big_font.render("GAME OVER", True, RED)
        final_score = font.render(f"Your score: {int(score)}", True, WHITE)
        restart = font.render("Press R to play again", True, YELLOW)
        quit_text = pygame.font.Font(None, 28).render("Press ESC to quit", True, GRAY)

        screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 75)))
        screen.blit(final_score, final_score.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20)))
        screen.blit(restart, restart.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 35)))
        screen.blit(quit_text, quit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 75)))

    pygame.display.flip()

pygame.quit()
