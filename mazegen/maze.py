import random
from typing import Any
import sys
from .parsers import (
    check_values,
    store,
    convert,
)


class Maze:
    def __init__(self, filename: str) -> None:
        """Receive name of config file and create the maze"""
        self.config: dict[str, Any] = self.parse_config(filename)
        self.width: int = self.config["WIDTH"]
        self.height: int = self.config["HEIGHT"]
        self.entry: tuple[int, int] = self.config["ENTRY"]
        self.exit: tuple[int, int] = self.config["EXIT"]
        self.perfect: bool = self.config["PERFECT"]
        self.reset_matrix()
        self.next = {"north": (0, -1),
                     "east": (1, 0),
                     "south": (0, 1),
                     "west": (-1, 0)}
        self.draw42 = self.Draw42(self)
        self.num42 = self.draw42.correct_42()
        if not self.num42:
            print("Maze too small for drawing '42'")
        self.seed = Maze.seed_value(self.config)
        self.digger()
        if not self.perfect:
            self.dig_imperfect()

    @staticmethod
    def parse_config(configfile: str) -> dict[str, Any]:
        """Call the parsing methods and return config as dict"""
        try:
            config: dict[str, str] = store(configfile)
            config = convert(config)
        except FileNotFoundError as e:
            print(f"File not found: {e}")
            sys.exit()
        except UnicodeDecodeError as e:
            print(f"Encoding error (file is not UTF-8): {e}")
            sys.exit()
        except ValueError as e:
            print(f"Invalid config format: {e}")
            sys.exit()
        if not check_values(config):
            print("config.txt is invalid. Try again")
            sys.exit()
        return config

    def reset_matrix(self) -> None:
        """Generate new matrix with all walls closed"""
        self.matrix: list[list[Maze.Cell]] = []
        for y in range(self.height):
            row: list[Maze.Cell] = []
            self.matrix.append(row)
            for x in range(self.width):
                row.append(Maze.Cell())

    def regenerate(self) -> None:
        """Generate a new maze (fresh random seed unless one is given)."""
        self.seed = random.randrange(2 ** 32)
        random.seed(self.seed)
        self.reset_matrix()
        self.digger()
        if not self.perfect:
            self.dig_imperfect()

    @staticmethod
    def seed_value(config: dict[str, Any]) -> Any:
        """Get seed value if it exists"""
        seed: Any = None
        if "SEED" in config:
            seed = config["SEED"]
        return seed

    @staticmethod
    def add_coord(
            current: tuple[int, int], add_x_y: tuple[int, int]
    ) -> tuple[int, int]:
        """Calculate the coordinates of the 'next' cell"""
        x = current[0] + add_x_y[0]
        y = current[1] + add_x_y[1]
        return x, y

    def digger(self) -> None:
        """Open walls to create a perfect maze"""
        total: int = self.height * self.width
        len42: int = len(self.num42)
        random.seed(self.seed)
        first = (0, 0)
        if first in self.num42:
            first = (1, 0)
        self.road: list[tuple[int, int]] = [first]
        self.visited: list[tuple[int, int]] = [first]
        while total - len42 > len(self.visited):
            current = self.road[len(self.road) - 1]
            pending = list(self.next.keys())
            chosen = ""
            while (pending and not self.check_neighbour(current, chosen)):
                chosen = random.choice(pending)
                pending.remove(chosen)
            if self.check_neighbour(current, chosen):
                self.break_whole_wall(current, chosen)
            else:
                self.road.remove(current)

    def dig_imperfect(self) -> None:
        """If Perfect = False, break some more walls"""
        y = 0
        while y < self.height:
            x = 0
            while x < self.width:
                if (x, y) in self.num42:
                    break
                current = self.matrix[y][x]
                pending = current.closed()
                while pending:
                    self.visited = []
                    chosen = random.choice(pending)
                    pending.remove(chosen)
                    if self.check_neighbour((x, y), chosen):
                        self.break_whole_wall((x, y), chosen)
                        break
                x += 3
            y += 3

    def break_whole_wall(self, current: tuple[int, int], chosen: str) -> None:
        """Open current and next and add next to visited"""
        adjacent = {"north": "south",
                    "east": "west",
                    "south": "north",
                    "west": "east"}
        x, y = current
        self.matrix[y][x].open_wall(chosen)
        x, y = Maze.add_coord(current, self.next[chosen])
        self.matrix[y][x].open_wall(adjacent[chosen])
        self.visited.append((x, y))
        self.road.append((x, y))

    def check_neighbour(self, current: tuple[int, int], chosen: str) -> bool:
        """Check if visiting neighbour is possible"""
        if chosen == "":
            return False
        x, y = self.add_coord(current, self.next[chosen])
        if not all((x >= 0, x <= self.width - 1,
                   y >= 0, y <= self.height - 1,
                   (x, y) not in self.visited,
                   (x, y) not in self.num42)):
            return False
        return True

    def path_finder(self) -> list[str]:
        """Find path using Breadth-First Search algorithm"""
        path: list[str] = []
        paths: list[tuple[tuple[int, int], list[str]]] = [
            (self.entry, path)
        ]
        visited: set[tuple[int, int]] = {self.entry}
        while paths:
            current, current_path = paths.pop(0)
            x, y = current
            cell = self.matrix[y][x]
            for direction in cell.opened():
                next_coord = Maze.add_coord(current, self.next[direction])
                if next_coord not in visited:
                    visited.add(next_coord)
                    new_path = current_path + [direction]
                    if next_coord == self.exit:
                        return new_path
                    paths.append((next_coord, new_path))
        return []

    def path_cells(self) -> list[tuple[int, int]]:
        dir = self.path_finder()
        road = [self.entry]
        for i, d in enumerate(dir):
            next = Maze.add_coord(road[i], self.next[d])
            road.append(next)
        return road

    def grid(self) -> list[list[int]]:
        """Return grid with cell 4-bits code as int"""
        grid: list[list[int]] = []
        for y in range(self.height):
            row: list[int] = []
            grid.append(row)
            for c in self.matrix[y]:
                code = int(c.walls_code(), 16)
                row.append(code)
        return grid

    class Draw42:
        def __init__(self, maze: "Maze") -> None:
            """Receive the object Maze to use its attributes"""
            self.maze = maze

        @staticmethod
        def fourty_two_cells(first: tuple[int, int]) -> set[tuple[int, int]]:
            """Define the cells that draw a '42'"""
            n42_cells: set[tuple[int, int]] = set()
            coords = [
                (0, 0),
                (4, 0),
                (5, 0),
                (6, 0),
                (0, 1),
                (6, 1),
                (0, 2),
                (1, 2),
                (2, 2),
                (4, 2),
                (5, 2),
                (6, 2),
                (2, 3),
                (4, 3),
                (2, 4),
                (4, 4),
                (5, 4),
                (6, 4)
            ]
            for c in coords:
                n42_cells.add(Maze.add_coord(first, c))
            return n42_cells

        def correct_42(self) -> set[tuple[int, int]]:
            """Return a valid '42' even in case of exit/entry overlap"""
            n42_cells: set[tuple[int, int]] = set()
            if (self.maze.width < 8 or self.maze.height < 6):
                return n42_cells
            first = Maze.Draw42.coord_init(self.maze.width, self.maze.height)
            draw = self.fourty_two_cells(first)
            if self.maze.entry in draw or self.maze.exit in draw:
                stop = False
                for y in range(self.maze.height - 5):
                    for x in range(self.maze.width - 7):
                        draw = self.fourty_two_cells((x, y))
                        if self.maze.entry not in draw:
                            if self.maze.exit not in draw:
                                stop = True
                                break
                    if stop:
                        break
            if self.maze.entry in draw or self.maze.exit in draw:
                draw = set()
            return draw

        @staticmethod
        def coord_init(width: int, height: int) -> tuple[int, int]:
            """Calculate the first cell of the '42' draw"""
            x = int((width - 7) / 2)
            y = int((height - 5) / 2)
            return x, y

    class Cell:
        def __init__(self) -> None:
            """Define the closed walls of a cell"""
            self.closed_walls: dict[str, bool] = {"north": True,
                                                  "east": True,
                                                  "south": True,
                                                  "west": True}

        def open_wall(self, direction: str) -> None:
            """Open the wall in one direction (north, east, south or west)"""
            self.closed_walls.update({direction: False})

        def opened(self) -> list[str]:
            """Give the list of opened walls of the cell"""
            dir = self.closed_walls.keys()
            walls = [w for w in dir if self.closed_walls[w] is False]
            return walls

        def closed(self) -> list[str]:
            """Give the list of closed walls of the cell"""
            dir = self.closed_walls.keys()
            walls = [w for w in dir if self.closed_walls[w] is True]
            return walls

        def walls_code(self) -> str:
            """Return the hexadecimal code of the cell"""
            code = 0
            if self.closed_walls["north"]:
                code += 1
            if self.closed_walls["east"]:
                code += 2
            if self.closed_walls["south"]:
                code += 4
            if self.closed_walls["west"]:
                code += 8
            return format(code, 'X')
