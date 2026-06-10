"""Terminal visual representation for the A-Maze-ing project.

Renders a :class:`maze.Maze` as colored blocks using ANSI
truecolor escape codes, and offers an interactive menu to regenerate the
maze, show/hide the shortest path, and cycle the wall colors.
"""

import sys
from mazegen.maze import Maze

N: int = 1   # 0b0001 North
E: int = 2   # 0b0010 East
S: int = 4   # 0b0100 South
W: int = 8   # 0b1000 West

# Pixel kinds for the rendering grid.
WALL, OPEN, ENTRY, EXIT, PATH, PATTERN = range(6)

# A palette maps each pixel kind to an (r, g, b) color.
Palette = dict[int, tuple[int, int, int]]

PALETTES: list[tuple[str, Palette]] = [
    ("white", {
        WALL: (225, 225, 225), OPEN: (0, 0, 0),
        ENTRY: (200, 0, 200), EXIT: (220, 40, 40),
        PATH: (70, 170, 220), PATTERN: (130, 130, 130),
    }),
    ("green", {
        WALL: (60, 170, 70), OPEN: (0, 0, 0),
        ENTRY: (210, 70, 200), EXIT: (220, 40, 40),
        PATH: (120, 120, 230), PATTERN: (40, 110, 45),
    }),
    ("gold", {
        WALL: (200, 180, 40), OPEN: (0, 0, 0),
        ENTRY: (210, 70, 200), EXIT: (220, 40, 40),
        PATH: (70, 170, 220), PATTERN: (150, 135, 30),
    }),
    ("blue", {
        WALL: (60, 120, 220), OPEN: (0, 0, 0),
        ENTRY: (210, 70, 200), EXIT: (220, 40, 40),
        PATH: (230, 200, 60), PATTERN: (40, 80, 160),
    }),
]


def _block(rgb: tuple[int, int, int]) -> str:
    """Return a 2-char-wide colored block as an ANSI escape sequence."""
    r, g, b = rgb
    return f"\x1b[48;2;{r};{g};{b}m  \x1b[0m"


def _kind_grid(maze: Maze, show_path: bool) -> list[list[int]]:
    """Build the (2H+1) x (2W+1) grid of pixel kinds for the maze."""
    rows, cols = 2 * maze.height + 1, 2 * maze.width + 1
    grid = [[WALL] * cols for _ in range(rows)]
    walls = maze.grid()
    patt = maze.num42
    for y in range(maze.height):
        for x in range(maze.width):
            cy, cx = 2 * y + 1, 2 * x + 1
            if (x, y) in patt:
                grid[cy][cx] = PATTERN
                continue
            grid[cy][cx] = OPEN
            value = walls[y][x]
            if not value & N:
                grid[cy - 1][cx] = OPEN
            if not value & S:
                grid[cy + 1][cx] = OPEN
            if not value & W:
                grid[cy][cx - 1] = OPEN
            if not value & E:
                grid[cy][cx + 1] = OPEN
    _fill_pattern_edges(grid, patt)
    if show_path:
        _draw_path(grid, maze.path_cells())
    ex, ey = maze.entry
    xx, xy = maze.exit
    grid[2 * ey + 1][2 * ex + 1] = ENTRY
    grid[2 * xy + 1][2 * xx + 1] = EXIT
    return grid


def _fill_pattern_edges(
    grid: list[list[int]], patt: set[tuple[int, int]]
) -> None:
    """Color the gaps between adjacent "42" cells so it looks solid."""
    for x, y in patt:
        cy, cx = 2 * y + 1, 2 * x + 1
        if (x + 1, y) in patt:
            grid[cy][cx + 1] = PATTERN
        if (x, y + 1) in patt:
            grid[cy + 1][cx] = PATTERN
        if (x + 1, y) in patt and (x, y + 1) in patt \
                and (x + 1, y + 1) in patt:
            grid[cy + 1][cx + 1] = PATTERN


def _draw_path(
    grid: list[list[int]], path: list[tuple[int, int]]
) -> None:
    """Mark the solution cells and the passages joining them."""
    for x, y in path:
        grid[2 * y + 1][2 * x + 1] = PATH
    for (ax, ay), (bx, by) in zip(path, path[1:]):
        my = (2 * ay + 1 + 2 * by + 1) // 2
        mx = (2 * ax + 1 + 2 * bx + 1) // 2
        grid[my][mx] = PATH


def render(
    maze: Maze, palette: Palette, show_path: bool
) -> str:
    """Return the full maze as a printable string of colored blocks."""
    grid = _kind_grid(maze, show_path)
    lines = ["".join(_block(palette[kind]) for kind in row) for row in grid]
    return "\n".join(lines)


def _print_menu(color_name: str, show_path: bool) -> None:
    """Print the interactive menu"""
    state = "shown" if show_path else "hidden"
    print("\n=== A-Maze-ing ===")
    print("1. Re-generate a new maze")
    print(f"2. Show/Hide path from entry to exit (path: {state})")
    print(f"3. Rotate maze colors (current: {color_name})")
    print("4. Quit")


def run_visual(maze: Maze) -> None:
    """Run the interactive terminal loop for the given maze."""
    color_idx = 0
    show_path = False
    while True:
        name, palette = PALETTES[color_idx]
        sys.stdout.write("\x1b[2J\x1b[H")
        sys.stdout.write(render(maze, palette, show_path) + "\n")
        sys.stdout.flush()
        _print_menu(name, show_path)
        try:
            choice = input("Choice? (1-4): ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if choice == "1":
            maze.regenerate()
        elif choice == "2":
            show_path = not show_path
        elif choice == "3":
            color_idx = (color_idx + 1) % len(PALETTES)
        elif choice == "4":
            break
