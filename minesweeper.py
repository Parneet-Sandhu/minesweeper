import pygame
import random

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 10
TILE_SIZE = WIDTH // GRID_SIZE
MINE_COUNT = 15

# Colors
WHITE = (255, 255, 255)
GRAY = (192, 192, 192)
BLACK = (0, 0, 0)

# Create a grid
grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Create a list to store mine locations
mines = []

# Create a screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper")

# Function to draw the grid
def draw_grid():
    for x in range(0, WIDTH, TILE_SIZE):
        for y in range(0, HEIGHT, TILE_SIZE):
            rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, GRAY, rect, 1)

# Function to plant mines
def plant_mines():
    while len(mines) < MINE_COUNT:
        x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
        if (x, y) not in mines:
            mines.append((x, y))
            grid[y][x] = -1

# Function to count mines in neighboring cells
def count_neighbors(x, y):
    if grid[y][x] == -1:
        return -1

    count = 0
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and grid[ny][nx] == -1:
                count += 1
    return count

# Function to reveal empty cells
def reveal_empty(x, y):
    if grid[y][x] == 0:
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and not revealed[ny][nx]:
                    revealed[ny][nx] = True
                    if grid[ny][nx] == 0:
                        reveal_empty(nx, ny)

# Create a 2D list to track revealed cells
revealed = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Plant mines
plant_mines()

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos[0] // TILE_SIZE, event.pos[1] // TILE_SIZE
            if (x, y) in mines:
                print("Game Over")
                running = False
            else:
                revealed[y][x] = True
                if grid[y][x] == 0:
                    reveal_empty(x, y)

    # Draw the grid
    screen.fill(WHITE)
    draw_grid()

    # Draw mines and numbers
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            if revealed[y][x]:
                if (x, y) in mines:
                    pygame.draw.circle(screen, BLACK, (x * TILE_SIZE + TILE_SIZE // 2, y * TILE_SIZE + TILE_SIZE // 2), TILE_SIZE // 2)
                else:
                    count = count_neighbors(x, y)
                    if count > 0:
                        font = pygame.font.Font(None, 36)
                        text = font.render(str(count), True, BLACK)
                        screen.blit(text, (x * TILE_SIZE + TILE_SIZE // 2 - 10, y * TILE_SIZE + TILE_SIZE // 2 - 15))

    pygame.display.flip()

pygame.quit()
