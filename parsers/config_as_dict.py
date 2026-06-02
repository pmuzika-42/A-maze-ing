from typing import Any
import sys


def store_config(filename: str) -> dict[str, str]:
    """Read the config doc and return its content as a dict"""
    config = {}
    try:
        with open(filename) as f:
            for x in f:
                if x.lstrip()[0] != "#" and "=" in x:
                    line = x.split("=")
                    config.update({line[0]: line[1].rstrip()})
    except Exception as e:
        print(f"{e}: Bad format in config file")
        sys.exit()
    finally:
        return config


def convert_values(config: dict[str, Any]) -> dict[str, Any]:
    """Take config values as str and convert them to useful data types"""
    size_keys = ["WIDTH", "HEIGHT"]
    coord_keys = ["ENTRY", "EXIT"]
    for key in size_keys:
        try:
            config.update({key: int(config[key])})
        except Exception as e:
            print(f"Error in {key} value: {e}")
            sys.exit()
    for key in coord_keys:
        try:
            coord = tuple(map(int, config[key].split(",")))
            if len(coord) != 2:
                sys.exit(f"Error: Bad format in '{key}' value")
            x = int(coord[0])
            y = int(coord[1])
            config.update({key: (x, y)})
        except Exception as e:
            print(f"Error in {key} value: {e}")
            sys.exit()
    if config["PERFECT"] == "True":
        config.update({"PERFECT": True})
    elif config["PERFECT"] == "False":
        config.update({"PERFECT": False})
    else:
        sys.exit("Error: Bad format in 'PERFECT' value")
    return config
