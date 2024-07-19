import pygame
import pygame_gui
import sys

# Constants
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 20, 20
SQUARE_SIZE = WIDTH // COLS

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Pygame Initialization
pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Advanced IDS Pathfinding")

# Pygame GUI Manager
manager = pygame_gui.UIManager((WIDTH, HEIGHT))

# Buttons
exit_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((WIDTH - 100, HEIGHT - 50), (80, 40)),
    text='Exit',
    manager=manager
)
start_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((WIDTH - 200, HEIGHT - 50), (80, 40)),
    text='Start',
    manager=manager
)
set_start_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((WIDTH - 300, HEIGHT - 50), (80, 40)),
    text='Set Start',
    manager=manager
)
set_end_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((WIDTH - 400, HEIGHT - 50), (80, 40)),
    text='Set End',
    manager=manager
)

class Grid:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]
        self.start = (0, 0)
        self.end = (rows - 1, cols - 1)
        self.path = []
        self.setting_start = False
        self.setting_end = False

    def draw(self):
        WIN.fill(WHITE)
        for row in range(self.rows):
            for col in range(self.cols):
                color = WHITE
                if (row, col) == self.start:
                    color = RED
                elif (row, col) == self.end:
                    color = BLUE
                elif (row, col) in self.path:
                    color = GREEN
                elif self.grid[row][col] == 1:
                    color = BLACK
                pygame.draw.rect(WIN, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                pygame.draw.rect(WIN, BLACK, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 1)
        manager.draw_ui(WIN)
        pygame.display.update()

    def toggle_obstacle(self, row, col):
        if (row, col) != self.start and (row, col) != self.end:
            self.grid[row][col] = 1 if self.grid[row][col] == 0 else 0

    def set_start(self, row, col):
        self.start = (row, col)

    def set_end(self, row, col):
        self.end = (row, col)

    def is_valid(self, row, col):
        return 0 <= row < self.rows and 0 <= col < self.cols and self.grid[row][col] == 0

    def ids(self):
        def dls(node, depth, path):
            if node == self.end:
                return path + [node]
            if depth == 0:
                return None
            row, col = node
            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                next_node = (row + dr, col + dc)
                if self.is_valid(*next_node) and next_node not in path:
                    result = dls(next_node, depth - 1, path + [node])
                    if result:
                        return result
            return None

        depth = 0
        while True:
            result = dls(self.start, depth, [])
            if result:
                return result
            depth += 1

def main():
    clock = pygame.time.Clock()
    grid = Grid(ROWS, COLS)

    running = True
    while running:
        time_delta = clock.tick(30)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == exit_button:
                        running = False
                    elif event.ui_element == start_button:
                        grid.path = grid.ids()
                    elif event.ui_element == set_start_button:
                        grid.setting_start = True
                    elif event.ui_element == set_end_button:
                        grid.setting_end = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                row, col = y // SQUARE_SIZE, x // SQUARE_SIZE
                if grid.setting_start:
                    grid.set_start(row, col)
                    grid.setting_start = False
                elif grid.setting_end:
                    grid.set_end(row, col)
                    grid.setting_end = False
                else:
                    grid.toggle_obstacle(row, col)

            manager.process_events(event)

        manager.update(time_delta)
        grid.draw()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
