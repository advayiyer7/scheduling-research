"""
Basic HEFT Example

Runs HEFT on a diamond-shaped task graph over a 3-node heterogeneous network.

Run: python src/scripts/run_heft_example.py
"""

import networkx as nx

from saga import Network, TaskGraph
from saga.schedulers import HeftScheduler


def build_diamond_task_graph() -> TaskGraph:
    r"""
    Diamond DAG:

        T0
       /  \
      T1   T2
       \  /
        T3

    In SAGA v2, a task has a single `cost`. Per-processor heterogeneity
    comes from differing node speeds in the network (exec_time = cost / speed).
    """
    g = nx.DiGraph()
    g.add_node("T0", weight=14)
    g.add_node("T1", weight=13)
    g.add_node("T2", weight=11)
    g.add_node("T3", weight=13)

    g.add_edge("T0", "T1", weight=18)
    g.add_edge("T0", "T2", weight=12)
    g.add_edge("T1", "T3", weight=9)
    g.add_edge("T2", "T3", weight=15)

    return TaskGraph.from_nx(g)


def build_heterogeneous_network() -> Network:
    """
    3-node fully-connected network with different node speeds (heterogeneous)
    and uniform link speeds.
    """
    g = nx.Graph()
    g.add_node("P0", weight=1.0)
    g.add_node("P1", weight=1.5)
    g.add_node("P2", weight=2.0)

    g.add_edge("P0", "P1", weight=1.0)
    g.add_edge("P0", "P2", weight=1.0)
    g.add_edge("P1", "P2", weight=1.0)

    return Network.from_nx(g)


def print_task_graph(task_graph: TaskGraph) -> None:
    print("\n=== Task Graph ===")
    tasks = sorted(task_graph.tasks, key=lambda t: t.name)
    print(f"Tasks ({len(tasks)}): " + ", ".join(f"{t.name}(cost={t.cost})" for t in tasks))
    deps = sorted(task_graph.dependencies, key=lambda d: (d.source, d.target))
    print(f"Dependencies ({len(deps)}):")
    for d in deps:
        print(f"  {d.source} -> {d.target}  (data size = {d.size})")


def print_network(network: Network) -> None:
    print("\n=== Network ===")
    nodes = sorted(network.nodes, key=lambda n: n.name)
    print(f"Nodes ({len(nodes)}): " + ", ".join(f"{n.name}(speed={n.speed})" for n in nodes))


def print_schedule(schedule) -> None:
    print("\n=== Schedule ===")
    print(f"Makespan: {schedule.makespan:.2f}")
    print("Assignments (by node):")
    for node_name in sorted(schedule.mapping.keys()):
        tasks = schedule.mapping[node_name]
        if not tasks:
            print(f"  {node_name}: (idle)")
            continue
        parts = [f"{t.name} [{t.start:.2f}, {t.end:.2f}]" for t in tasks]
        print(f"  {node_name}: " + ", ".join(parts))


def main() -> None:
    print("=" * 50)
    print("HEFT Scheduling Example (SAGA v2 API)")
    print("=" * 50)

    task_graph = build_diamond_task_graph()
    print_task_graph(task_graph)

    network = build_heterogeneous_network()
    print_network(network)

    print("\nRunning HEFT...")
    schedule = HeftScheduler().schedule(network, task_graph)
    print_schedule(schedule)


if __name__ == "__main__":
    main()
