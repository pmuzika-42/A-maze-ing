from typing import Any
from mazegen import Maze
import sys


def write_output_file(maze: Maze, config: dict[str, Any]) -> None:
    """Write cell codes, entry, exit and path in a file .txt"""
    INVALID_CHARS = set('<>:"/\\|?*')
    UNTOUCHABLES = {
        "write_output.py",
        "README.md",
        "pyproject.toml",
        "mazegen-1.0.0-py3-none-any.whl",
        "Makefile",
        "config.txt",
        "a_maze_ing.py",
        ".gitignore",
    }
    filename = config["OUTPUT_FILE"]
    if any(c in INVALID_CHARS for c in filename):
        print("Invalid output filename: contains forbidden characters")
        print("Output file not created")
        sys.exit()
    if filename in UNTOUCHABLES:
        print("Invalid output filename: protected name")
        print("Output file not created")
        sys.exit()
    try:
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
                f.write(dir[0].upper())
            f.write("\n")
    except PermissionError:
        print("Permission denied: Output file not writable")
        sys.exit()
    except FileNotFoundError:
        print("Output file not found. Change file name in config")
        sys.exit()
