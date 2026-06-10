from typing import Any


def check_config_keys(config: dict[str, Any]) -> bool:
    """Check if mandatory and optional keys are in config file"""
    mandatory_keys = [
        "WIDTH",
        "HEIGHT",
        "ENTRY",
        "EXIT",
        "OUTPUT_FILE",
        "PERFECT"
    ]
    for key in mandatory_keys:
        if key not in config:
            print(f"Config file is missing '{key}' key")
            return False
    allowed_keys = set(mandatory_keys)
    allowed_keys.add("SEED")
    for key in config:
        if key not in allowed_keys:
            print(f"{key} not expected as key")
            return False
    return True


def check_max_size(width: int, height: int) -> bool:
    """Check if size <= max size allowed"""
    MAX_WIDTH = 42
    MAX_HEIGHT = 300
    MAX_CELLS = 9000
    if width > MAX_WIDTH:
        print("Width exceeds terminal size. Max width is 42")
        return False
    if height > MAX_HEIGHT:
        print("Height too big. Max height is 300")
        return False
    if MAX_CELLS < width * height:
        print("Maze size not supported by program. Max cell number is 9000")
        return False
    return True


def check_size_values(width: int, height: int) -> bool:
    """Check if width and height given values allow to draw a maze"""
    if all([(width > 0 and height > 0), (width > 1 or height > 1)]):
        return True
    else:
        return False


def check_diff_entry_exit(ent: tuple[int, int], ex: tuple[int, int]) -> bool:
    """Check entry and exit are different"""
    if ent == ex:
        return False
    return True


def check_coord(coord: tuple[int, int], width: int, height: int) -> bool:
    """Check if coordinates are inside the map"""
    if not all([(coord[0] >= 0 and coord[0] <= width - 1),
                (coord[1] >= 0 and coord[1] <= height - 1)]):
        return False
    return True


def check_config_values(config: dict[str, Any]) -> bool:
    """Check width, height, entry and exit values"""
    width = config["WIDTH"]
    height = config["HEIGHT"]
    entry = config["ENTRY"]
    exit = config["EXIT"]
    if not check_size_values(width, height):
        print("Incorrect maze size")
        return False
    if not check_max_size(width, height):
        return False
    if not check_coord(entry, width, height):
        print("Entry not inside the maze")
        return False
    if not check_coord(exit, width, height):
        print("Exit not inside the maze")
        return False
    if not check_diff_entry_exit(entry, exit):
        print("Entry and Exit have equal coordinates")
        return False
    return True
