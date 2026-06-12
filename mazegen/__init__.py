"""Reusable maze generator module (42 ``A-Maze-ing`` project).

This single module exposes one class `Maze`, that
builds a rectangular maze (optionally *perfect*) and gives access to both
the maze structure and a shortest solution path. It is meant to be built
as a pip package (``mazegen-*``) and reused in a later project.

Wall encoding
-------------
Each cell stores its closed walls as a 4-bit integer (one hexadecimal
digit per cell)::

    bit 0 (LSB) -> North
    bit 1       -> East
    bit 2       -> South
    bit 3       -> West

A closed wall sets its bit to ``1``; an open wall sets it to ``0``. A cell
fully closed on the four sides therefore equals ``0xF`` (15).

Quick start
-----------
Instantiate, then read the structure and the solution::

    from mazegen import Maze

    maze = Maze("config.txt")

    # 1) Pass the name of a config file as arg.
    the config file must have this format (example values are given):
    WIDTH=20
    HEIGHT=20
    ENTRY=1,0
    EXIT=19,18
    OUTPUT_FILE=maze.txt
    PERFECT=True
    SEED=42
    (SEED is optional, other keys are mandatory.)

    # 2) Access the structure: matrix[y][x] is a cell object.
    matrix = maze.matrix
    maze.matrix[y][x].walls_closed() is the 4-bit hexadecimal code of a cell.

    # 3) Access a solution: list of cells and the N/E/S/W string.
    cells = maze.path_cells()
    # cells = [(0, 0), (1, 0), ...]
    moves string:
    string = ""
    for dir in maze.path_finder():
        string += dir[0].upper()
    # string = "ESSEEN..."

Custom parameters inside config file
-----------------
``width`` / ``height`` set the size, ``entry`` / ``exit`` set the
coordinates of the two endpoints, ``seed`` makes the generation
reproducible, ``perfect`` chooses a single-path maze (``True``)
or a braided one (``False``).
Call `regenerate` to produce a new maze
(a fresh random seed unless one is given).
"""


from .maze import Maze
from .visual import run_visual

__all__ = ["Maze", "run_visual"]
