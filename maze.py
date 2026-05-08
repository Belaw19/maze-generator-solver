import pygame
import random
import sys

# =========================
# SETTINGS
# =========================
ROWS = 20
COLS = 20
CELL_SIZE = 30

WIDTH = COLS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE

FPS = 60

# =========================
# COLORS
# =========================
WHITE = (255, 255, 255)      # Background
BLACK = (0, 0, 0)            # Maze walls

RED = (255, 0, 0)            # Solving path
BLUE = (0, 100, 255)         # Dead ends
GREEN = (0, 200, 0)          # Current mouse
      # Visited cells

# =========================
# PYGAME INIT
# =========================
pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Generator and Solver")

clock = pygame.time.Clock()

# =========================
# CELL CLASS
# =========================
class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col

        self.walls = {
            "top": True,
            "right": True,
            "bottom": True,
            "left": True
        }

        self.visited = False
        self.solved = False
        self.dead_end = False

    def draw(self):
        x = self.col * CELL_SIZE
        y = self.row * CELL_SIZE

        # Fill visited cells
        if self.visited:
            pygame.draw.rect(screen, WHITE, (x, y, CELL_SIZE, CELL_SIZE))

        # Solver colors
        if self.dead_end:
            pygame.draw.rect(screen, BLUE, (x + 4, y + 4, CELL_SIZE - 8, CELL_SIZE - 8))

        if self.solved:
            pygame.draw.rect(screen, RED, (x + 4, y + 4, CELL_SIZE - 8, CELL_SIZE - 8))

        # Draw walls
        if self.walls["top"]:
            pygame.draw.line(screen, BLACK, (x, y), (x + CELL_SIZE, y), 2)

        if self.walls["right"]:
            pygame.draw.line(screen, BLACK, (x + CELL_SIZE, y),
                             (x + CELL_SIZE, y + CELL_SIZE), 2)

        if self.walls["bottom"]:
            pygame.draw.line(screen, BLACK, (x + CELL_SIZE, y + CELL_SIZE),
                             (x, y + CELL_SIZE), 2)

        if self.walls["left"]:
            pygame.draw.line(screen, BLACK, (x, y + CELL_SIZE),
                             (x, y), 2)

# =========================
# GRID
# =========================
grid = [[Cell(r, c) for c in range(COLS)] for r in range(ROWS)]

def get_cell(row, col):
    if 0 <= row < ROWS and 0 <= col < COLS:
        return grid[row][col]
    return None

# =========================
# REMOVE WALLS
# =========================
def remove_walls(current, next_cell):
    dx = current.col - next_cell.col
    dy = current.row - next_cell.row

    if dx == 1:
        current.walls["left"] = False
        next_cell.walls["right"] = False

    elif dx == -1:
        current.walls["right"] = False
        next_cell.walls["left"] = False

    if dy == 1:
        current.walls["top"] = False
        next_cell.walls["bottom"] = False

    elif dy == -1:
        current.walls["bottom"] = False
        next_cell.walls["top"] = False

# =========================
# MAZE GENERATION
# =========================
def generate_maze():
    stack = []

    current = grid[0][0]
    current.visited = True

    visited_count = 1
    total_cells = ROWS * COLS

    while visited_count < total_cells:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        neighbors = []

        directions = [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1)
        ]

        for dr, dc in directions:
            neighbor = get_cell(current.row + dr, current.col + dc)

            if neighbor and not neighbor.visited:
                neighbors.append(neighbor)

        if neighbors:
            next_cell = random.choice(neighbors)

            stack.append(current)

            remove_walls(current, next_cell)

            current = next_cell
            current.visited = True

            visited_count += 1

        elif stack:
            current = stack.pop()

        # DRAW
        screen.fill(WHITE)

        for row in grid:
            for cell in row:
                cell.draw()

        # Current generation cell
        x = current.col * CELL_SIZE + CELL_SIZE // 2
        y = current.row * CELL_SIZE + CELL_SIZE // 2

        pygame.draw.circle(screen, GREEN, (x, y), CELL_SIZE // 4)

        pygame.display.update()
        clock.tick(FPS)

# =========================
# RESET SOLVER
# =========================
def reset_solver():
    for row in grid:
        for cell in row:
            cell.solved = False
            cell.dead_end = False

# =========================
# SOLVE MAZE
# =========================
def solve_maze(start, end):
    stack = []
    visited = set()

    stack.append(start)
    visited.add((start.row, start.col))

    while stack:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        current = stack[-1]
        current.solved = True

        if current == end:
            return True

        neighbors = []

        r = current.row
        c = current.col

        # TOP
        if not current.walls["top"]:
            neighbor = get_cell(r - 1, c)
            if neighbor and (neighbor.row, neighbor.col) not in visited:
                neighbors.append(neighbor)

        # RIGHT
        if not current.walls["right"]:
            neighbor = get_cell(r, c + 1)
            if neighbor and (neighbor.row, neighbor.col) not in visited:
                neighbors.append(neighbor)

        # BOTTOM
        if not current.walls["bottom"]:
            neighbor = get_cell(r + 1, c)
            if neighbor and (neighbor.row, neighbor.col) not in visited:
                neighbors.append(neighbor)

        # LEFT
        if not current.walls["left"]:
            neighbor = get_cell(r, c - 1)
            if neighbor and (neighbor.row, neighbor.col) not in visited:
                neighbors.append(neighbor)

        if neighbors:
            next_cell = random.choice(neighbors)

            visited.add((next_cell.row, next_cell.col))
            stack.append(next_cell)

        else:
            dead = stack.pop()
            dead.dead_end = True
            dead.solved = False

        # DRAW
        screen.fill(WHITE)

        for row in grid:
            for cell in row:
                cell.draw()

        # Start
        sx = start.col * CELL_SIZE + CELL_SIZE // 2
        sy = start.row * CELL_SIZE + CELL_SIZE // 2
        pygame.draw.circle(screen, GREEN, (sx, sy), CELL_SIZE // 4)

        # End
        ex = end.col * CELL_SIZE + CELL_SIZE // 2
        ey = end.row * CELL_SIZE + CELL_SIZE // 2
        pygame.draw.circle(screen, BLACK, (ex, ey), CELL_SIZE // 4)

        pygame.display.update()
        clock.tick(40)

    return False

# =========================
# MAIN
# =========================
def main():
    generate_maze()

    reset_solver()

    start = grid[0][0]
    end = grid[ROWS - 1][COLS - 1]

    solve_maze(start, end)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main()