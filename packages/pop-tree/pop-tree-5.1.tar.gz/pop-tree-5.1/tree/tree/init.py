from pop.hub import Hub, Sub
from dict_tools import data as data_
from typing import Any, Dict

__func_alias__ = {"format_": "format"}


def __init__(hub: Hub):
    hub.pop.sub.add(dyne_name="rend")
    hub.pop.sub.add(dyne_name="graph")
    hub.pop.sub.load_subdirs(hub.tree)


def cli(hub: Hub):
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

    if hub.OPT.tree.graph:
        hub.graph.GRAPH = hub.OPT.tree.graph
    else:
        # Find the first plugin that was loaded for graphing
        loaded_mods = hub.graph._loaded
        if "simple" in loaded_mods:
            hub.graph.GRAPH = "simple"
        else:
            iter_mods = iter(hub.graph._loaded)
            hub.graph.GRAPH = next(iter_mods)
            if hub.graph.GRAPH == "init":
                hub.graph.GRAPH = next(iter_mods)

    hub.graph.init.show(result)


def recurse(hub: Hub, sub: Sub, ref: str = None) -> Dict[str, Any]:
    """
    Find all of the loaded subs in a Sub. I.E:
        pprint(hub.pop.tree.recurse(hub.pop))
    :param hub: The redistributed pop central hub
    :param sub: The pop object that contains the loaded module data
    :param ref: The current reference on the hub
    """
    sub_name = sub._dyne_name
    if sub_name:
        if ref:
            ref = f"{ref}.{sub_name}"
        else:
            ref = sub_name
    ret = data_.NamespaceDict()
    for loaded in sorted(sub._subs):
        loaded_ref = f"{ref}.{loaded}"
        loaded_sub: Sub = getattr(sub, loaded)
        if not (loaded_sub._virtual and getattr(loaded_sub, "_sub_virtual", True)):
            # Bail early if the sub's virtual isn't True
            continue
        recursed_sub = hub.tree.init.recurse(loaded_sub, ref=loaded_ref)

        for mod in sorted(loaded_sub._loaded):
            loaded_mod = getattr(loaded_sub, mod)
            recursed_sub[mod] = hub.tree.mod.parse(
                loaded_mod, ref=f"{ref}.{loaded}.{mod}"
            )

        if recursed_sub:
            ret[loaded] = recursed_sub

    return ret


def traverse(hub: Hub) -> Dict[str, Any]:
    """
    :param hub: The redistributed pop central hub
    :return: A dictionary representation of all the subs on the hub. I.E:
        pprint(hub.pop.tree.traverse())
    """
    root = data_.NamespaceDict()
    for sub in sorted(hub._subs):
        loaded_sub = getattr(hub, sub)
        root[sub] = hub.tree.init.recurse(loaded_sub)

        for mod in sorted(loaded_sub._loaded):
            loaded_mod = getattr(loaded_sub, mod)
            root[sub][mod] = hub.tree.mod.parse(loaded_mod, ref=f"{sub}.{mod}")
    return root
