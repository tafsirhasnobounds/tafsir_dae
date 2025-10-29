import pygame, sys, random
pygame.init()

# Window setup
info = pygame.display.Info()  # Get full screen info
WIDTH, HEIGHT = info.current_w, info.current_h  # Match display resolution
CELL_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)  # Enables fullscreen mode
pygame.display.set_caption("Snake Game")

# Colors
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

# font
font = pygame.font.SysFont("Arial", 25)

# Snake and Apple setup 
snake = [(100, 100), (80, 100), (60, 100)]  # Snake body made of 3 blocks
direction = "RIGHT"  # Starting direction
apple = (random.randrange(0, WIDTH, CELL_SIZE), random.randrange(0, HEIGHT, CELL_SIZE))  # Random apple spawn
score = 0  # Starting score

#  Clock to control game speed 
clock = pygame.time.Clock()

#  Draw background grid (helps visualize cells) 
def draw_grid():
    for x in range(0, WIDTH, CELL_SIZE):
        for y in range(0, HEIGHT, CELL_SIZE):
            pygame.draw.rect(screen, (30, 30, 30), (x, y, CELL_SIZE, CELL_SIZE), 1)

#  Draw the snake (blue body + white eyes) 
def draw_snake():
    for segment in snake:
        pygame.draw.rect(screen, BLUE, (*segment, CELL_SIZE, CELL_SIZE))
    # Snake eyes on the head
    head_x, head_y = snake[0]
    eye_size = 4
    pygame.draw.circle(screen, WHITE, (head_x + 5, head_y + 5), eye_size)
    pygame.draw.circle(screen, WHITE, (head_x + 15, head_y + 5), eye_size)

#  Draw the apple (red block) 
def draw_apple():
    pygame.draw.rect(screen, RED, (*apple, CELL_SIZE, CELL_SIZE))

#  Display the score in the top-left corner 
def draw_score():
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

#  Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Closes game window
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            # Escape key lets player quit fullscreen
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            # Arrow key movement
            if event.key == pygame.K_UP and direction != "DOWN":
                direction = "UP"
            elif event.key == pygame.K_DOWN and direction != "UP":
                direction = "DOWN"
            elif event.key == pygame.K_LEFT and direction != "RIGHT":
                direction = "LEFT"
            elif event.key == pygame.K_RIGHT and direction != "LEFT":
                direction = "RIGHT"

    # Snake movement logic
    head_x, head_y = snake[0]
    if direction == "UP":
        head_y -= CELL_SIZE
    elif direction == "DOWN":
        head_y += CELL_SIZE
    elif direction == "LEFT":
        head_x -= CELL_SIZE
    elif direction == "RIGHT":
        head_x += CELL_SIZE
    new_head = (head_x, head_y)
    snake.insert(0, new_head)

    # Apple eating logic 
    if new_head == apple:
        score += 1  # Increase score
        apple = (random.randrange(0, WIDTH, CELL_SIZE), random.randrange(0, HEIGHT, CELL_SIZE))  # Respawn apple
    else:
        snake.pop()  # Keep same length if not eating apple

    # Collision detection (walls or self)
    if (
        head_x < 0 or head_x >= WIDTH or
        head_y < 0 or head_y >= HEIGHT or
        new_head in snake[1:]
    ):
        pygame.quit()
        sys.exit()

    #  Drawing everything on screen 
    screen.fill(BLACK)      # Reset screen
    draw_grid()             # Draw cell background
    draw_snake()            # Draw snake
    draw_apple()            # Draw apple
    draw_score()            # Show score

    pygame.display.update()  # Refresh display
    clock.tick(10)  # Controls speed (10 fps)