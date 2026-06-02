from typing import Any
from maze import Maze


def write_output_file(maze: Maze, config: dict[str, Any]) -> None:
    """Write cell codes, entry, exit and path in a file .txt"""
    filename = config["OUTPUT_FILE"]
    with open(filename, "w") as f:
        for row in maze.matrix:
            for cell in row:
                f.write(cell.walls_code())
            f.write("\n")
        f.write("\n")
        coord = (config["ENTRY"], config["EXIT"])
        for pos in coord:
            x, y = pos
            f.write(f"{x},{y}")
            f.write("\n")
        for dir in maze.path_finder():
            f.write(dir)
        f.write("\n")
