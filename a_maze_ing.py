import sys
from typing import Any
from maze import Maze
from parsers import (
    check_keys,
    check_values,
    store,
    convert,
)
from write_output import write_output_file


def main() -> None:
    """Main function calling all the other functions"""
    if len(sys.argv) != 2:
        print(f"Usage: python3 {sys.argv[0]} <config_file>")
        return
    try:
        config: dict[str, Any] = store(sys.argv[1])
        config = convert(config)
    except Exception as e:
        print(f"Bad format in config file: {e}")
        return
    print(config)
    # Testing check_config function:
    if check_keys(config) and check_values(config):
        print("config.txt is valid")
    else:
        print("config.txt is invalid")
        return
    maze = Maze(config)
    write_output_file(maze, config)
    maze.display_maze()


if __name__ == "__main__":
    main()
