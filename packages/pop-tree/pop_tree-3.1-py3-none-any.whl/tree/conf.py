CLI_CONFIG = {
    "format_plugin": {"options": ["-p"]},
    "output": {"source": "rend", "default": None,},
    "add_sub": {"nargs": "*"},
    "sub": {"positional": True, "nargs": "?",},
    "doc": {"action": "store_true",},
    "file": {"action": "store_true",},
    "recurse": {"action": "store_true", },
}
CONFIG = {
    "add_sub": {"help": "Add a sub to the hub", "default": [],},
    "sub": {"type": str, "help": "The sub on the hub to parse", "default": None,},
    "doc": {
        "help": "Show the available docstrings of all functions",
        "default": False,
    },
    "file": {
        "help": "Show the file locations of available functions",
        "default": False,
    },
    "recurse": {
        "help": "Load the named sub onto the hub recursively",
        "default": False,
    },
}
SUBCOMMANDS = {}
DYNE = {
    "tree": ["tree"],
}
