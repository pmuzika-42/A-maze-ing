import sys
from mazegen import Maze, run_visual
from write_output import write_output_file


def main() -> None:
    """Instantiate Maze, write output and draw maze"""
    if len(sys.argv) != 2:
        print(f"Usage: python3 {sys.argv[0]} <config_file>")
        return
    try:
        maze = Maze(sys.argv[1])
    except Exception as e:
        print(e)
        return
    write_output_file(maze, maze.config)
    run_visual(maze)


if __name__ == "__main__":
    main()
