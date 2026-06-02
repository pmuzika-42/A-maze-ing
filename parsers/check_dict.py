from typing import Any


def check_config_keys(config: dict[str, str]) -> bool:
    """Check if all the mandatory keys are in config file"""
    mandatory_keys = [
        "WIDTH",
        "HEIGHT",
        "ENTRY",
        "EXIT",
        "OUTPUT_FILE",
        "PERFECT"
    ]
    for key in mandatory_keys:
        if key not in config.keys():
            print(f"Config file is missing '{key}' key")
            return False
    return True


def check_config_values(config: dict[str, Any]) -> bool:
    """Check width, height, entry and exit values"""
    width = config["WIDTH"]
    height = config["HEIGHT"]
    entry = config["ENTRY"]
    exit = config["EXIT"]
    if all([(width > 0 and height > 0), (width > 1 or height > 1),
            (entry[0] >= 0 and entry[0] <= width - 1),
            (entry[1] >= 0 and entry[1] <= height - 1),
            (exit[0] >= 0 and exit[0] <= width - 1),
            (exit[1] >= 0 and exit[1] <= height - 1),
            (entry != exit)]):
        return True
    else:
        return False
