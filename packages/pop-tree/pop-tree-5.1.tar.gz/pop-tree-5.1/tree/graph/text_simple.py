from collections import namedtuple
from typing import Any, Dict, List

__virtualname__ = "simple"

Plugin = namedtuple("Plugin", ("functions", "variables"))


def __virtual__(hub):
    return (
        hasattr(hub, "output"),
        "'rend' needs to be installed in the python environment to use this plugin",
    )


def _keys(d: Dict[str, Any]) -> List[str]:
    return [k for k in d.keys()]


def process_mod(
    hub,
    ref: str,
    doc: str,
    file: str,
    attributes: List[str],
    functions: Dict[str, Dict[str, Any]],
    variables: Dict[str, Dict[str, Any]],
    classes: Dict[str, Dict[str, Any]],
):
    return Plugin(functions=_keys(functions), variables=_keys(variables))


def show(hub, tree: Dict[str, Any]):
    simple_tree = hub.graph.init.recurse(tree)

    outputter = getattr(hub, f"output.{hub.OPT.rend.output}.display")
    rendered = outputter(simple_tree)
    print(rendered)
