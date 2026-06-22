"""
MAZE PARSER

This file handles the parsing of config.txt by
reading the data inside in a specific format of
'FIELD=DATA'

Comments are allowed and must begin with '#' per line
"""

from typing import Dict, Tuple, Any
from maze_gen.validator import ConfigError


def extract_config_data(filepath: str) -> Dict[str, Any]:

    """
    Uses all helper functions in this file and extracts data in config file
    as a dictionary.

    Default dictionary is created beforehand. Data read from the
    config file replaces the dictionary's respective field data.
    """

    with open(filepath, "r") as f:
        config = {
            "WIDTH": None,
            "HEIGHT": None,
            "ENTRY": None,
            "EXIT": None,
            "PERFECT": None,
            "OUTPUT_FILE": None,
            "SEED": None
        }
        dup_checker = {
            "WIDTH": None,
            "HEIGHT": None,
            "ENTRY": None,
            "EXIT": None,
            "PERFECT": None,
            "OUTPUT_FILE": None,
            "SEED": None
        }
        filedata_lines = f.readlines()
        for line in filedata_lines:
            split_line = line.strip("\n").split("=", 1)

            if len(split_line) == 2:
                key, value = extract_one_key_value_pair(split_line)

                if validate_key(key):
                    if dup_checker[key] == None:
                        config[key] = parse_raw_value(key, value)
                        dup_checker[key] = 1
                    else:
                        raise ConfigError("Duplicate Key field detected")
                else:
                    raise ConfigError("Invalid Key field detected")
        return config


def parse_raw_value(key: str, value: Any) -> Any:

    """
    Extracts the value data and tries convert the datatype based
    on the field it was in.
    """

    try:
        if key in ['WIDTH', 'HEIGHT']:
            return int(value)
        elif key in ['ENTRY', 'EXIT']:
            x, y = value.split(",")
            return (int(x), int(y))
        elif key in ['PERFECT']:
            if value == "True":
                return True
            elif value == "False":
                return False
            return None
        else:
            if value == '':
                return None
            return value
    except ValueError:
        return None


def validate_key(key: str) -> bool:

    """
    Checks if the field / key in the config file matches
    a list of allowed fields. Everything else is rejected.
    """

    valid_key_list = ['WIDTH', 'HEIGHT', 'ENTRY', 'EXIT',
                      'OUTPUT_FILE', 'PERFECT', 'SEED']

    if key not in valid_key_list:
        return False
    return True


def extract_one_key_value_pair(split_line: list[str]) -> Tuple[str, str]:

    """
    Takes in a list of strings from a single line and
    filters out comment data. and tries to build it
    into a Tuple of raw strings in (KEY, VALUE) format.
    """

    if "#" in split_line[1]:
        seperated_values = split_line[1].partition("#")
        ph_value = ""

        for s in seperated_values:
            if "#" not in s:
                ph_value += s
            else:
                break
        return (split_line[0], ph_value.strip())
    else:
        return (split_line[0], split_line[1].strip())
