import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
BALL_SPEED = 7
PADDLE_SPEED = 7
WHITE = (255, 255, 255)
BALL_SIZE = 15
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 90

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Pong')

# Game variables
ball_x, ball_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
ball_dx, ball_dy = BALL_SPEED * random.choice((1, -1)), BALL_SPEED * random.choice((1, -1))
player_paddle_y, opponent_paddle_y = SCREEN_HEIGHT // 2, SCREEN_HEIGHT // 2
player_score, opponent_score = 0, 0

# Font for scoring
font = pygame.font.Font(None, 74)

def reset_ball():
    global ball_x, ball_y, ball_dx, ball_dy
    ball_x, ball_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
    ball_dx *= random.choice((1, -1))
    ball_dy *= random.choice((1, -1))

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle paddle movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player_paddle_y > 0:
        player_paddle_y -= PADDLE_SPEED
    if keys[pygame.K_s] and player_paddle_y < SCREEN_HEIGHT - PADDLE_HEIGHT:
        player_paddle_y += PADDLE_SPEED

    # Update ball position
    ball_x += ball_dx
    ball_y += ball_dy

    # Collision with top and bottom
    if ball_y <= 0 or ball_y >= SCREEN_HEIGHT - BALL_SIZE:
        ball_dy *= -1

    # Collision with paddles
    if (ball_x <= PADDLE_WIDTH and player_paddle_y < ball_y < player_paddle_y + PADDLE_HEIGHT) or \
       (ball_x >= SCREEN_WIDTH - PADDLE_WIDTH - BALL_SIZE and opponent_paddle_y < ball_y < opponent_paddle_y + PADDLE_HEIGHT):
        ball_dx *= -1

    # Update opponent paddle
    if opponent_paddle_y + PADDLE_HEIGHT // 2 < ball_y:
        opponent_paddle_y += PADDLE_SPEED
    elif opponent_paddle_y + PADDLE_HEIGHT // 2 > ball_y:
        opponent_paddle_y -= PADDLE_SPEED

    # Ball out of bounds
    if ball_x < 0:
        opponent_score += 1
        reset_ball()
    elif ball_x > SCREEN_WIDTH - BALL_SIZE:
        player_score += 1
        reset_ball()

    # Draw everything
    screen.fill((0, 0, 0))
    player_paddle = pygame.draw.rect(screen, WHITE, (0, player_paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT))
    opponent_paddle = pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH - PADDLE_WIDTH, opponent_paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT))
    ball = pygame.draw.rect(screen, WHITE, (ball_x, ball_y, BALL_SIZE, BALL_SIZE))

    # Display scores
    player_text = font.render(str(player_score), True, WHITE)
    screen.blit(player_text, (50, 10))
    opponent_text = font.render(str(opponent_score), True, WHITE)
    screen.blit(opponent_text, (SCREEN_WIDTH - 100, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
        
