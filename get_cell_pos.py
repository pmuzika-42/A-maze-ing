from maze import Maze


def get_cell(grid: Maze, pos: tuple[int, int]):
    x, y = pos
    return grid[y][x]
