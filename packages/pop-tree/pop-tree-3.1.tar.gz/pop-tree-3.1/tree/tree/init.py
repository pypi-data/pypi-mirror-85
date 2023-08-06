from collections import namedtuple

import pop.hub

__func_alias__ = {"format_": "format"}

from dict_tools import data as data_
from typing import Any, Dict, List, NamedTuple
import pop.loader

Plugin = namedtuple("Plugin", ("functions", "variables"))


def __init__(hub):
    hub.pop.sub.add(dyne_name="rend")
    hub.pop.sub.load_subdirs(hub.tree)


def cli(hub: pop.hub.Hub):
    hub.pop.config.load(["tree", "rend"], cli="tree")

    print_opt = str(hub.OPT.tree.sub).upper() == "OPT"
    if hub.OPT.tree.sub:
        if print_opt:
            hub.pop.config.load(
                ["tree", "rend"] + list(hub.OPT.tree.add_sub), cli="tree"
            )
        else:
            hub.pop.sub.add(dyne_name=hub.OPT.tree.sub)
            if hub.OPT.tree.recurse:
                hub.pop.sub.load_subdirs(getattr(hub, hub.OPT.tree.sub), recurse=True)

    for dyne in hub.OPT.tree.add_sub:
        hub.pop.sub.add(dyne_name=dyne)

    if print_opt:
        result = hub.OPT
    else:
        result = hub.tree.init.traverse()
        if hub.OPT.tree.sub:
            result = {hub.OPT.tree.sub: result[hub.OPT.tree.sub]}

    outputter = getattr(hub, f"output.{hub.OPT.rend.output}.display")
    rendered = outputter({"hub": result})

    print(rendered)


def funcs(hub: pop.hub.Hub, mod: pop.loader.LoadedMod) -> List[str]:
    """
    Find all of the loaded functions in a pop plugin. I.E:
        pprint(hub.pop.tree.funcs(hub.pop.tree))
    :param hub: The redistributed pop central hub
    :param mod: A plugin that has been loaded onto a sub
    :return: A Dictionary of loaded modules names mapped to a list of their functions
    """
    return sorted(mod._funcs.keys())


def data(hub: pop.hub.Hub, mod: pop.loader.LoadedMod) -> List[str]:
    """
    Find all of the loaded data in a pop plugin. I.E:
        pprint(hub.pop.tree.data(hub.pop.tree))
    :param hub: The redistributed pop central hub
    :param mod: A plugin that has been loaded onto a sub
    """
    return sorted(x for x in mod._vars if x.isupper() and not x.startswith("_"))


def recurse(hub: pop.hub.Hub, sub: pop.hub.Sub, top: bool = True) -> Dict[str, Any]:
    """
    Find all of the loaded subs in a Sub. I.E:
        pprint(hub.pop.tree.recurse(hub.pop))
    :param hub: The redistributed pop central hub
    :param sub: The pop object that contains the loaded module data
    """
    ret = data_.NamespaceDict()
    for loaded in sub._subs:
        loaded_sub = getattr(sub, loaded)
        recursed_sub = hub.tree.init.recurse(loaded_sub, top=False)

        for mod in loaded_sub._loaded:
            loaded_mod = getattr(loaded_sub, mod)
            recursed_sub[mod] = hub.tree.init.parse_mod(loaded_mod)

        if recursed_sub:
            ret[loaded] = recursed_sub

    return ret


def parse_mod(hub, mod):
    ret = {}

    if hub.OPT.tree.file:
        ret["file"] = mod.__file__

    mod_doc = (mod._attrs["__doc__"] or "").strip()
    if mod_doc and hub.OPT.tree.doc:
        ret["doc"] = mod_doc

    ret["functions"] = hub.tree.init.funcs(mod)
    ret["variables"] = hub.tree.init.data(mod)
    if hub.OPT.tree.file or hub.OPT.tree.doc:
        return ret
    else:
        return Plugin(functions=ret["functions"], variables=ret["variables"])


def traverse(hub) -> Dict[str, Any]:
    """
    :param hub: The redistributed pop central hub
    :return: A dictionary representation of all the subs on the hub. I.E:
        pprint(hub.pop.tree.traverse())
    """
    root = data_.NamespaceDict()
    for sub in hub._subs:
        loaded_sub = getattr(hub, sub)
        root[sub] = hub.tree.init.recurse(loaded_sub)

        for mod in loaded_sub._loaded:
            loaded_mod = getattr(loaded_sub, mod)
            root[sub][mod] = hub.tree.init.parse_mod(loaded_mod)
    return root
