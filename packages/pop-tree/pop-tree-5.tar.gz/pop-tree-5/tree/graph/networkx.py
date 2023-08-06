from enum import Enum, IntEnum
from typing import Any, Dict, List

try:
    import networkx as nx
    import matplotlib.pyplot as plt

    HAS_LIBS = (True,)
except ImportError as e:
    HAS_LIBS = False, str(e)


def __virtual__(hub):
    return HAS_LIBS


def __init__(hub):
    # A collection of nodes (vertices) along with identified pairs of nodes (called edges, links, etc).
    hub.graph.networkx.GRAPH = nx.Graph(name="hub")


class NodeType(IntEnum):
    hub = 0
    sub = 1
    plugin = 2
    function = 3
    contract = 6
    variable = 4
    cls = 5
    unknown = 7


def add_node(hub, ref: str, node_type: NodeType = NodeType.unknown, **attrs):
    builder = []
    for name in ref.split("."):
        parent = ".".join(builder)
        cur_ref = ".".join(builder + [name])
        if cur_ref not in hub.graph.networkx.GRAPH.nodes:
            hub.graph.networkx.GRAPH.add_node(
                cur_ref, name=name, node_type=NodeType.sub
            )
        hub.graph.networkx.GRAPH.add_edge(parent, cur_ref)
        builder.append(name)

    # The last thing in the list gets all the attrs
    if attrs:
        hub.graph.networkx.GRAPH.add_node(
            cur_ref, name=name, node_type=node_type, **attrs
        )


def add_edge(
    hub, ref1: str, ref2: str, node_type: NodeType = NodeType.unknown, **ref2_attrs
):
    hub.graph.networkx.add_node(ref1)
    hub.graph.networkx.add_node(ref2, node_type=node_type, **ref2_attrs)
    hub.graph.networkx.GRAPH.add_edge(ref1, ref2)


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
    hub.graph.networkx.add_node(ref, doc=doc, file=file, attributes=attributes)

    for name, function in functions.items():
        if any(function["contracts"].get(c) for c in ("pre", "call", "post")):
            previous = None
            for c in (
                function["contracts"]["pre"]
                + function["contracts"]["call"]
                + [function["ref"]]
                + function["contracts"]["post"]
            ):
                if c == function["ref"]:
                    node_type = NodeType.function
                else:
                    node_type = NodeType.contract
                hub.graph.networkx.GRAPH.add_node(
                    c, name=c.split(".")[-1], node_type=node_type
                )
                if previous is None:
                    hub.graph.networkx.GRAPH.add_edge(ref, c, doc=doc)
                else:
                    hub.graph.networkx.GRAPH.add_edge(previous, c)
                previous = c
        else:
            hub.graph.networkx.add_edge(
                ref, function["ref"], doc=doc, node_type=NodeType.function
            )

    for name, variable in variables.items():
        hub.graph.networkx.add_edge(
            ref,
            variable["ref"],
            type=variable["type"],
            value=variable["value"],
            node_type=NodeType.variable,
        )

    for name, cls in classes.items():
        hub.graph.networkx.add_edge(ref, cls["ref"], node_type=NodeType.cls)


def show(hub, tree: Dict[str, Any]):
    hub.graph.init.recurse(tree)
    hub.graph.networkx.GRAPH.add_node("", name="hub", node_type=NodeType.hub)

    # All nodes should point to themselves down the line
    graph: nx.GRAPH = hub.graph.networkx.GRAPH
    # from pprint import pprint
    # print(dict(graph.adjacency()))

    plt.figure()
    pos_nodes = nx.spring_layout(graph)
    nx.draw(
        graph,
        pos_nodes,
        node_color=[
            v.value for v in nx.get_node_attributes(graph, "node_type").values()
        ],
        cmap=plt.cm.get_cmap("Set2"),
    )
    names = nx.get_node_attributes(graph, "name")
    nx.draw_networkx_labels(graph, pos_nodes, labels=names)
    plt.show()
