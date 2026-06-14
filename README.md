*This project has been created as part of the 42 curriculum by pabduran, pmuzika.*

## Description

A-maze-ing is a program that takes a configuration file, generates a maze and writes it to a file using a hexadecimal wall representation.
It also provides a visual representation of the maze.

Part of the project is the maze generator **mazegen** which is implemented as a single reusable package and can be used in later projects.

## Instructions

### Installation

You can install the package directly from the repository:

```bash
python3 -m pip install mazegen-1.0.0-py3-none-any.whl
```

### Configuration

The package uses a configuration file (config.txt) with the following structure (example values):

```text
WIDTH=20
HEIGHT=20
ENTRY=1,0
EXIT=19,18
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=42
```

**Width** / **height**: define the maze dimensions.
**Entry** / **Exit**: define the start and end points of the maze.
**Output_file**: name of the file where the maze is written.
**Perfect**: defines whether the maze is perfect or imperfect.
**Seed**: random seed for reproducibility (optional; all other fields are mandatory).

### Usage

#### Import module

```python
from mazegen import Maze
```

#### Create a maze using a configuration file

```python
maze = Maze("config.txt")
```

The maze is generated automatically upon initialization.

#### Access the maze structure

```python
grid = maze.matrix
```

#### Access a specific cell (x, y)

```python
cell = maze.matrix[y][x]
```

#### Access the solution path

```python
solution = maze.path_cells()
```

#### Command-line usage

```bash
python3 a_maze_ing.py config.txt
```

### Wall encoding

Each cell stores its walls as a 4-bit integer (one hexadecimal digit per cell):

```text
bit 0 (LSB) -> North
bit 1       -> East
bit 2       -> South
bit 3       -> West
```

A wall set to 1 is closed, and 0 is open.
A fully enclosed cell is therefore represented as 0xF (15).

## Choice of Algorithms

### Maze Generation Algorithm

#### Depth-First Search (DFS)

Reasons:

- Simple and easy to implement
- Produces perfect mazes (no loops, one unique solution)
- Efficient for small to medium mazes
- Works well for educational purposes and visualization

### Maze Solving Algorithm

#### Breadth-First Search (BFS)

Reasons:

- Simple and easy to implement
- Guarantees the shortest path in imperfect mazes
- Works well for pathfinding between two points

## Reusability

The mazegen module is fully reusable:

- Can be imported into any Python project
- Offers customizable parameters for maze size, seed, and algorithm
- Provides access to the maze grid and solution paths
- Fully documented with docstrings for easy integration

Installation:

```bash
python3 -m pip install mazegen-1.0.0-py3-none-any.whl
```

Usage:

```python
from mazegen import Maze
```

## Team and Project Management

### The roles of each member

The project was developed collaboratively, and most design and implementation decisions were made as a team. Nevertheless, each member contributed more extensively to specific components:

- **pabduran**: maze generation and solving algorithms, visualization module.
- **pmuzika** configuration parsing, class design, and overall architecture.

### Anticipated Planning and How It Evolved

The project was initially planned as a two-week effort. Due to the time required for implementation, testing, and documentation, the final duration was approximately four weeks.

### What Worked Well and What Could Be Improved

What worked well:

- The DFS generation algorithm was straightforward to implement and produced well-structured perfect mazes.
- Splitting the code into the reusable `mazegen` package and the main script made the architecture clean.
- BFS for pathfinding guaranteed shortest paths without extra complexity.

What could be improved:

- The imperfect maze strategy (breaking extra walls every 3 cells) is naive; a smarter approach would give more varied results.
- The terminal renderer is limited by column width — very wide mazes clip on small terminals.
- No automated test suite was included (tests were manual).

### Tools Used

- **Python 3.10+**: primary language.
- **flake8**: style linting.
- **mypy**: static type checking.
- **pytest** (manual runs): functional verification.
- **pip / build**: packaging and installation.
- **Claude Code / GPT-5**: documentation drafting, README review, Makefile review, and configuration parsing assistance.

## Resources

- Deep-First Search Algorithm: https://www.geeksforgeeks.org/dsa/depth-first-search-or-dfs-for-a-graph/
- Breadth-First Search Algorithm: https://medium.com/@prajun_t/breadth-first-search-bfs-db7ffb384da7
- Python documentation: https://www.w3schools.com/python/default.asp

AI assistance (GPT-5 and Claude) was used for:

- Drafting the initial README
- Reviewing Makefile
- configuration parsing
- Improving documentation clarity and consistency
