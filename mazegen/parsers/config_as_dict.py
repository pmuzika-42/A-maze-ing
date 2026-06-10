from typing import Any
from . import check_keys


def store_config(filename: str) -> dict[str, str]:
    """Read the config doc and return its content as a dict"""
    config = {}
    try:
        with open(filename) as f:
            for x in f:
                line = x.strip()
                if not line or line[0] == "#":
                    continue
                if "=" not in line:
                    raise ValueError(f"Invalid config line: '{line}'")
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip()
                if key in config:
                    raise ValueError(f"{key} key is duplicate")
                config[key] = value
    except FileNotFoundError:
        raise FileNotFoundError("File config.txt not found")
    return config


def convert_values(config: dict[str, Any]) -> dict[str, Any]:
    """Take config values as str and convert them to useful data types"""
    if not check_keys(config):
        raise ValueError("Invalid config file. Try again")
    size_keys = ["WIDTH", "HEIGHT"]
    coord_keys = ["ENTRY", "EXIT"]
    for key in size_keys:
        try:
            config.update({key: int(config[key])})
        except ValueError as e:
            raise ValueError(f"Error in {key} value") from e
    for key in coord_keys:
        try:
            coord = tuple(map(int, config[key].split(",")))
            if len(coord) != 2:
                raise ValueError(f"Bad format in '{key}' value")
            x = int(coord[0])
            y = int(coord[1])
            config.update({key: (x, y)})
        except Exception as e:
            raise ValueError(f"Error in {key} value") from e
    if config["PERFECT"] == "True":
        config.update({"PERFECT": True})
    elif config["PERFECT"] == "False":
        config.update({"PERFECT": False})
    else:
        raise ValueError("Bad format in 'PERFECT' value")
    if "SEED" in config:
        try:
            config["SEED"] = int(config["SEED"].strip())
        except ValueError:
            raise ValueError("SEED must be an integer")
    return config
