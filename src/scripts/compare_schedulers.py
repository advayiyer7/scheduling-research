"""
Compare Schedulers

Runs multiple SAGA schedulers on the same problem instance and prints a
comparison of makespan and wall-clock runtime.

Run: python src/scripts/compare_schedulers.py
"""

import time
from typing import List, Tuple

import networkx as nx

from saga import Network, TaskGraph, Scheduler
from saga.schedulers import (
    HeftScheduler,
    CpopScheduler,
    MinMinScheduler,
    MaxMinScheduler,
    MCTScheduler,
    SufferageScheduler,
    FastestNodeScheduler,
)


def build_instance() -> Tuple[Network, TaskGraph]:
    r"""
    A small DAG used as a shared benchmark instance:

        T0
       / | \
      T1 T2 T3
      |  X  |     (T1->T4, T2->T4, T2->T5, T3->T5)
      T4   T5
       \   /
        T6
    """
    tg = nx.DiGraph()
    for name, w in [("T0", 10), ("T1", 8), ("T2", 14), ("T3", 7),
                    ("T4", 11), ("T5", 9), ("T6", 6)]:
        tg.add_node(name, weight=w)
    for src, tgt, w in [
        ("T0", "T1", 4), ("T0", "T2", 6), ("T0", "T3", 5),
        ("T1", "T4", 3), ("T2", "T4", 7), ("T2", "T5", 4),
        ("T3", "T5", 5), ("T4", "T6", 2), ("T5", "T6", 3),
    ]:
        tg.add_edge(src, tgt, weight=w)

    net = nx.Graph()
    for name, speed in [("P0", 1.0), ("P1", 1.5), ("P2", 2.0), ("P3", 1.25)]:
        net.add_node(name, weight=speed)
    nodes = ["P0", "P1", "P2", "P3"]
    for i, u in enumerate(nodes):
        for v in nodes[i + 1:]:
            net.add_edge(u, v, weight=1.0)

    return Network.from_nx(net), TaskGraph.from_nx(tg)


def benchmark(scheduler: Scheduler, network: Network, task_graph: TaskGraph) -> dict:
    name = scheduler.name
    t0 = time.perf_counter()
    try:
        schedule = scheduler.schedule(network, task_graph)
        runtime_ms = (time.perf_counter() - t0) * 1000.0
        return {
            "scheduler": name,
            "makespan": schedule.makespan,
            "runtime_ms": runtime_ms,
            "error": None,
        }
    except Exception as e:
        return {
            "scheduler": name,
            "makespan": float("nan"),
            "runtime_ms": (time.perf_counter() - t0) * 1000.0,
            "error": f"{type(e).__name__}: {e}",
        }


def print_table(rows: List[dict]) -> None:
    rows_sorted = sorted(rows, key=lambda r: (r["error"] is not None, r["makespan"]))
    print(f"\n{'Scheduler':<22} {'Makespan':>10} {'Runtime (ms)':>14}  {'Notes'}")
    print("-" * 70)
    for r in rows_sorted:
        ms = "ERR" if r["error"] else f"{r['makespan']:.2f}"
        notes = r["error"] if r["error"] else ""
        print(f"{r['scheduler']:<22} {ms:>10} {r['runtime_ms']:>14.2f}  {notes}")


def main() -> None:
    print("=" * 50)
    print("Scheduler Comparison (SAGA v2 API)")
    print("=" * 50)

    network, task_graph = build_instance()
    print(f"\nInstance: {len(task_graph.tasks)} tasks, "
          f"{len(task_graph.dependencies)} deps, "
          f"{len(network.nodes)} nodes")

    schedulers: List[Scheduler] = [
        HeftScheduler(),
        CpopScheduler(),
        MinMinScheduler(),
        MaxMinScheduler(),
        MCTScheduler(),
        SufferageScheduler(),
        FastestNodeScheduler(),
    ]

    results = [benchmark(s, network, task_graph) for s in schedulers]
    print_table(results)

    successes = [r for r in results if r["error"] is None]
    if successes:
        best = min(successes, key=lambda r: r["makespan"])
        print(f"\nBest makespan: {best['scheduler']} = {best['makespan']:.2f}")


if __name__ == "__main__":
    main()
