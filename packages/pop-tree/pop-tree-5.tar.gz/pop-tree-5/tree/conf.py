CLI_CONFIG = {
    "output": {
        "source": "rend",
        "default": None,
    },
    "add_sub": {"nargs": "*"},
    "sub": {
        "positional": True,
        "nargs": "?",
    },
    "recurse": {
        "action": "store_true",
    },
    "graph": {},
}

# TODO only print the named refs I.E pop.config.load or pop.config
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
    "recurse": {
        "help": "Load the named sub onto the hub recursively",
        "default": False,
    },
    "graph": {
        "help": "Plugin to use for generating a graph, (I.E. 'simple', 'details', 'json')",
        "default": None,
    },
}

DYNE = {
    "graph": ["graph"],
    "tree": ["tree"],
}
