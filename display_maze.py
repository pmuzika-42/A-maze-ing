def display_maze_terminal() -> None:
    with open("maze.txt") as f:
        for _ in range(len(f.readline()) - 1):
            print(" __", end="")
        print()
        for _ in range(len(f.readline()) - 1):
            print("|__", end="")


if __name__ == "__main__":
    display_maze_terminal()
