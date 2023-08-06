import collections
import inspect
import pop.contract
import pop.hub
import pop.loader
import textwrap
from collections import namedtuple
from dict_tools import data as data_
from typing import Any, Dict, List

__func_alias__ = {"format_": "format"}

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


def serialize_signature(hub, signature: inspect.Signature):
    ret = collections.OrderedDict()
    for p in signature.parameters:
        param: inspect.Parameter = signature.parameters[p]
        ret[param.name] = {}
        if param.default is not inspect._empty:
            ret[param.name]["default"] = param.default
        if param.annotation is not inspect._empty:
            ret[param.name]["annotation"] = str(param.annotation)
    return {"parameters": ret, "return_annotation": signature.return_annotation}


def funcs(
    hub: pop.hub.Hub, mod: pop.loader.LoadedMod, ref: str
) -> List[str] or Dict[str, str]:
    """
    Find all of the loaded functions in a pop plugin. I.E:
        pprint(hub.pop.tree.funcs(hub.pop.tree))
    :param hub: The redistributed pop central hub
    :param mod: A plugin that has been loaded onto a sub
    :return: A Dictionary of loaded modules names mapped to a list of their functions
    """
    funcs = sorted(mod._funcs.keys())
    if hub.OPT.tree.details:
        ret = {}
        for f in funcs:
            contract: pop.contract.Contracted = mod._funcs[f]
            func_info = {
                "ref": f"{ref}.{f}",
                "doc": textwrap.dedent(str(contract.func.__doc__ or "")).strip("\n"),
                "contracts": {
                    contract_type: [
                        f"{ref}.{c.ref}.{c.func.__name__}" for c in contracts
                    ]
                    for contract_type, contracts in contract.contract_functions.items()
                },
            }
            func_info.update(
                hub.tree.init.serialize_signature(contract.signature),
            )
            ret[f] = func_info
        return ret
    else:
        return funcs


def data(
    hub: pop.hub.Hub, mod: pop.loader.LoadedMod, ref: str
) -> List[str] or Dict[str, str]:
    """
    Find all of the loaded data in a pop plugin. I.E:
        pprint(hub.pop.tree.data(hub.pop.tree))
    :param hub: The redistributed pop central hub
    :param mod: A plugin that has been loaded onto a sub
    """
    datas = sorted(x for x in mod._vars if x.isupper() and not x.startswith("_"))
    if hub.OPT.tree.details:
        ret = {}
        for d_name in datas:
            d = mod._vars[d_name]
            data_info = {
                "ref": f"{ref}.{d_name}",
                "type": d.__class__.__name__,
                "value": d,
            }
            ret[d_name] = data_info
        return ret
    else:
        return datas


def types(
    hub: pop.hub.Hub, mod: pop.loader.LoadedMod, ref: str
) -> List[str] or Dict[str, str]:
    """
    Find all of the loaded types in a pop plugin. I.E:
        pprint(hub.pop.tree.types(hub.pop.tree))
    :param hub: The redistributed pop central hub
    :param mod: A plugin that has been loaded onto a sub
    """
    classes = sorted(x for x in mod._classes if not x.startswith("_"))
    if hub.OPT.tree.details:
        ret = {}
        for class_name in classes:
            c = mod._classes[class_name]
            signature = inspect.signature(c.__init__)
            class_info = {
                "ref": f"{ref}.{class_name}",
                "doc": textwrap.dedent((c.__doc__ or "")).strip("\n"),
                "signature": f"{hub.tree.init.serialize_signature(signature)}",
            }
            ret[class_name] = class_info
        return ret
    else:
        return classes


UNKNOWN_REF = "< unknown ref >"


def get_ref(hub: pop.hub.Hub, mod: pop.loader.LoadedMod) -> str:
    """
    Try to find a reference on the hub for the given mod
    """
    try:
        sister_func: pop.contract.Contracted = next(iter(mod._funcs.values()))
        return sister_func.ref
    except StopIteration:
        return UNKNOWN_REF


def recurse(hub: pop.hub.Hub, sub: pop.hub.Sub, ref: str = None) -> Dict[str, Any]:
    """
    Find all of the loaded subs in a Sub. I.E:
        pprint(hub.pop.tree.recurse(hub.pop))
    :param hub: The redistributed pop central hub
    :param sub: The pop object that contains the loaded module data
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
        loaded_sub: pop.hub.Sub = getattr(sub, loaded)
        recursed_sub = hub.tree.init.recurse(loaded_sub, loaded_ref)

        for mod in sorted(loaded_sub._loaded):
            loaded_mod = getattr(loaded_sub, mod)
            recursed_sub[mod] = hub.tree.init.parse_mod(loaded_mod, ref=f"{ref}")

        if recursed_sub:
            ret[loaded] = recursed_sub

    return ret


def parse_mod(hub, mod, ref: str = None) -> Dict[str, Any] or Plugin:
    if hub.OPT.tree.details:
        ref_builder = []
        if ref:
            ref_builder.append(ref)
        ref_builder.append(hub.tree.init.get_ref(mod))
        ref = ".".join(ref_builder)
    mod_functions = hub.tree.init.funcs(mod, ref)
    mod_variables = hub.tree.init.data(mod, ref)
    if hub.OPT.tree.details:
        ret = {
            "ref": ref,
            "doc": (mod._attrs["__doc__"] or "").strip(),
            "file": mod.__file__,
            "attributes": sorted(
                [a for a in mod._attrs if not a.startswith("__") and a.endswith("__")]
            ),
            "classes": hub.tree.init.types(mod, ref),
            "functions": mod_functions,
            "variables": mod_variables,
        }

        return ret
    else:
        return Plugin(functions=mod_functions, variables=mod_variables)


def traverse(hub) -> Dict[str, Any]:
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
            root[sub][mod] = hub.tree.init.parse_mod(loaded_mod)
    return root
