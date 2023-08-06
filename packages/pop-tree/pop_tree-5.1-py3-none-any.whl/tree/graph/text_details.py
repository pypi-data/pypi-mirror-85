from typing import Any, Dict, List

__virtualname__ = "details"


def __virtual__(hub):
    return (
        hasattr(hub, "output"),
        "'rend' needs to be installed in the python environment to use this plugin",
    )


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
    ...


def show(hub, tree: Dict[str, Any]):
    outputter = getattr(hub, f"output.{hub.OPT.rend.output}.display")
    rendered = outputter(tree)
    print(rendered)
