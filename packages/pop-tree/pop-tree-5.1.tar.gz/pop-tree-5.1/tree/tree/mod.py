import inspect
import textwrap
from pop.contract import Contracted as Contract
from pop.hub import Hub
from pop.loader import LoadedMod
from collections import OrderedDict
from typing import Any, Dict, List

UNKNOWN_REF = "< unknown ref >"


def get_ref(hub: Hub, mod: LoadedMod) -> str:
    """
    Try to find a reference on the hub for the given mod
    """
    try:
        sister_func: Contract = next(iter(mod._funcs.values()))
        return sister_func.ref
    except StopIteration:
        return "asdf"


def serialize_signature(hub: Hub, signature: inspect.Signature):
    ret = OrderedDict()
    for p in signature.parameters:
        param: inspect.Parameter = signature.parameters[p]
        ret[param.name] = {}
        if param.default is not inspect._empty:
            ret[param.name]["default"] = param.default
        if param.annotation is not inspect._empty:
            ret[param.name]["annotation"] = str(param.annotation)

    final_ret = {"parameters": ret}
    if signature.return_annotation is not inspect._empty:
        final_ret["return_annotation"] = signature.return_annotation
    return final_ret


def funcs(hub: Hub, mod: LoadedMod, ref: str) -> List[str] or Dict[str, str]:
    """
    Find all of the loaded functions in a pop plugin. I.E:
        pprint(hub.pop.tree.funcs(hub.pop.tree))
    :param hub: The redistributed pop central hub
    :param mod: A plugin that has been loaded onto a sub
    :param ref: The current reference on the hub
    :return: A Dictionary of loaded modules names mapped to a list of their functions
    """
    funcs = sorted(mod._funcs.keys())
    ret = {}
    for f in funcs:
        contract: Contract = mod._funcs[f]
        func_info = {
            "ref": f"{ref}.{f}",
            "doc": textwrap.dedent(str(contract.func.__doc__ or "")).strip("\n"),
            "contracts": {
                contract_type: [f"{c.ref}.{c.func.__name__}" for c in contracts]
                for contract_type, contracts in contract.contract_functions.items()
            },
        }
        func_info.update(
            hub.tree.mod.serialize_signature(contract.signature),
        )
        ret[f] = func_info
    return ret


def data(hub: Hub, mod: LoadedMod, ref: str) -> List[str] or Dict[str, str]:
    """
    Find all of the loaded data in a pop plugin. I.E:
        pprint(hub.pop.tree.data(hub.pop.tree))
    :param hub: The redistributed pop central hub
    :param mod: A plugin that has been loaded onto a sub
    :param ref: The current reference on the hub
    """
    datas = sorted(x for x in mod._vars if x.isupper() and not x.startswith("_"))
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


def types(hub: Hub, mod: LoadedMod, ref: str) -> List[str] or Dict[str, str]:
    """
    Find all of the loaded types in a pop plugin. I.E:
        pprint(hub.pop.tree.types(hub.pop.tree))
    :param hub: The redistributed pop central hub
    :param mod: A plugin that has been loaded onto a sub
    :param ref: The current reference on the hub
    """
    classes = sorted(x for x in mod._classes if not x.startswith("_"))
    ret = {}
    for class_name in classes:
        c = mod._classes[class_name]
        signature = inspect.signature(c.__init__)
        class_info = {
            "ref": f"{ref}.{class_name}",
            "doc": textwrap.dedent((c.__doc__ or "")).strip("\n"),
            "signature": f"{hub.tree.mod.serialize_signature(signature)}",
        }
        ret[class_name] = class_info
    return ret


def parse(hub: Hub, mod: LoadedMod, ref: str) -> Dict[str, Any]:
    """
    Parse a loaded mod object

    :param hub: The redistributed pop central hub
    :param mod: A plugin that has been loaded onto a sub
    :param ref: The current reference on the hub
    """
    mod_functions = hub.tree.mod.funcs(mod, ref)
    mod_variables = hub.tree.mod.data(mod, ref)
    ret = {
        "ref": ref,
        "doc": (mod._attrs["__doc__"] or "").strip(),
        "file": mod.__file__,
        "attributes": sorted(
            [a for a in mod._attrs if not (a.startswith("__") and a.endswith("__"))]
        ),
        "classes": hub.tree.mod.types(mod, ref),
        "functions": mod_functions,
        "variables": mod_variables,
    }
    return ret
