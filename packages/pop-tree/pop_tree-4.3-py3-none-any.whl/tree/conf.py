CLI_CONFIG = {
    "format_plugin": {"options": ["-p"]},
    "output": {
        "source": "rend",
        "default": None,
    },
    "add_sub": {"nargs": "*"},
    "sub": {
        "positional": True,
        "nargs": "?",
    },
    "details": {
        "action": "store_true",
    },
    "recurse": {
        "action": "store_true",
    },
}
CONFIG = {
    "add_sub": {
        "help": "Add a sub to the hub",
        "default": [],
    },
    "sub": {
        "type": str,
        "help": "The sub on the hub to parse",
        "default": None,
    },
    "details": {
        "help": "Include details of each element in the tree",
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
