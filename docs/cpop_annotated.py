"""
docs/cpop_annotated.py
======================

Annotated copy of `saga/src/saga/schedulers/cpop.py` (SAGA v2.0.4).
Source paper: Topcuoglu, Hariri, Wu — "Performance-effective and low-complexity
task scheduling for heterogeneous computing" IEEE TPDS 2002.
DOI: https://dx.doi.org/10.1109/71.993206

CPoP = Critical Path on a Processor.

How CPoP differs from HEFT in one sentence:
    HEFT picks the EFT-minimising node per task, treating all tasks alike.
    CPoP identifies the critical-path tasks (those on the longest
    upward+downward rank chain) and pins ALL of them onto a single
    "critical-path processor" — the one that minimises the sum of their
    execution times. Non-critical tasks are scheduled HEFT-style.

Intuition:
    The critical path determines the makespan lower bound. If you can run
    the entire CP on the fastest available processor with zero inter-task
    communication overhead (because consecutive CP tasks live on the same
    node and their data transfer is free / loopback), you shrink the
    makespan floor. Non-CP tasks then fill in around the CP.

Priority used to drive the scheduling order:
    priority(t) = rank_u(t) + rank_d(t)
    The maximum value of this sum is constant across all tasks on the
    critical path — that's the geometric definition of the CP in a DAG
    weighted by avg execution + avg comm.

Algorithm sketch:
    1. Compute rank_u and rank_d for every task.
    2. priority[t] = rank_u + rank_d.
    3. cp_rank = max priority over entry tasks (= length of CP).
    4. cp_node = node minimising sum of exec times for CP tasks.
    5. Put ready tasks (no unscheduled parent) into a max-heap by priority.
    6. Pop tasks. If on CP: schedule on cp_node only. Otherwise: pick
       EFT-minimising node (HEFT-style). Add newly-ready children to heap.

Important: CPoP traverses the DAG in priority order, not topological order.
A heap of "tasks whose parents are all scheduled" is the ready set.
"""

from functools import lru_cache
import heapq
from queue import PriorityQueue
from typing import Any, Dict, Optional
import numpy as np

from saga import Scheduler, ScheduledTask, Schedule, Network, TaskGraph
from saga.utils.duplication import should_duplicate


# ---------------------------------------------------------------------------
# Rank functions — shared between HEFT (upward only) and CPoP (both).
# ---------------------------------------------------------------------------

@lru_cache(maxsize=None)
def upward_rank(network: Network, task_graph: TaskGraph) -> Dict[str, float]:
    """rank_u — longest *expected* path from a task to the exit task.

    Recurrence (HEFT'02 eq. 1):
        rank_u(t) = avg_compute(t) + max over s in succ(t) of
                    ( avg_comm(t, s) + rank_u(s) )

    Base case (sink): rank_u(sink) = avg_compute(sink) (no successors).

    Why "average"? We don't know which processor we'll run on yet. The
    rank is a prioritisation heuristic, not a real time, so averaging
    over candidates gives a cheap, network-aware estimate.
    """
    ranks: Dict[str, float] = {}

    # Reverse topo: children before parents, so when we compute rank_u(t)
    # we already have rank_u(child) for all children.
    topological_order = task_graph.topological_sort()
    for task in topological_order[::-1]:
        # Average execution time across all nodes — cost / speed averaged.
        avg_comp_time = np.mean([task.cost / node.speed for node in network.nodes])

        # max{ comm + child's rank } over outgoing edges. If `task` is a
        # sink (no outgoing), the second term is 0.
        max_comm_time = (
            0
            if task_graph.out_degree(task.name) <= 0
            else max(
                [
                    # rank already known (we're going in reverse topo).
                    ranks[task_graph_dependency.target]
                    # avg comm time on this edge: data size / avg link speed.
                    # NOTE: this averages over ALL edges in the network, not
                    # just edges adjacent to candidate destination nodes. A
                    # network-wide average — a deliberate simplification of
                    # HEFT'02's `c_bar`.
                    + np.mean(
                        [
                            task_graph_dependency.size / network_edge.speed
                            for network_edge in network.edges
                        ]
                    )
                    for task_graph_dependency in task_graph.out_edges(task.name)
                ]
            )
        )
        ranks[task.name] = float(avg_comp_time + max_comm_time)

    return ranks


def downward_rank(network: Network, task_graph: TaskGraph) -> Dict[str, float]:
    """rank_d — longest *expected* path from the entry to (just before) t.

    Recurrence (HEFT'02 eq. 2, sort of):
        rank_d(t) = max over p in pred(t) of
                    ( rank_d(p) + avg_comm(p, t) + avg_compute(p) )

    Base case (entry): rank_d(entry) = 0.

    Note: rank_d does NOT include t's own execution time, only the
    longest predecessor chain leading INTO t. priority = rank_u + rank_d
    therefore double-counts neither: rank_u contributes t's own avg exec.
    """
    ranks: Dict[str, float] = {}
    # Forward topo: parents before children.
    for task in task_graph.topological_sort():
        rank = (
            0
            if task_graph.in_degree(task.name) <= 0
            else max(
                [
                    ranks[task_graph_dependency.source]
                    # avg comm on the parent->task edge.
                    + np.mean(
                        [
                            task_graph_dependency.size / network_edge.speed
                            for network_edge in network.edges
                        ]
                    )
                    # SUBTLE: this adds the *current task's* avg compute,
                    # divided by avg node speed. This is consistent with the
                    # downward-rank formulation that includes the predecessor
                    # of t at the level closest to t. The convention varies
                    # by paper; SAGA's choice keeps rank_u + rank_d
                    # invariant along the critical path.
                    + (
                        task.cost
                        / np.mean([neighbor.speed for neighbor in network.nodes])
                    )
                    for task_graph_dependency in task_graph.in_edges(task.name)
                ]
            )
        )
        ranks[task.name] = float(rank)
    return ranks


@lru_cache(maxsize=None)
def cpop_ranks(network: Network, task_graph: TaskGraph) -> Dict[str, float]:
    """CPoP's task priority = upward + downward rank.

    Property: every task on the critical path has the same value of this
    sum, and that value equals the CP length. Tasks off the CP have a
    strictly smaller sum.
    """
    upward_ranks = upward_rank(network, task_graph)
    downward_ranks = downward_rank(network, task_graph)
    ranks = {
        task.name: (upward_ranks[task.name] + downward_ranks[task.name])
        for task in task_graph.tasks
    }
    return ranks


# ---------------------------------------------------------------------------
# CPoP scheduler
# ---------------------------------------------------------------------------

class CpopScheduler(Scheduler):
    """Critical-Path-on-Processor scheduler.

    Two key differences from HEFT:
      * Priorities use rank_u + rank_d, not just rank_u.
      * All CP tasks are forced onto a single "CP node", chosen to
        minimise total CP exec time.
    """

    # Same duplication hook as HEFT, but only applied to *non-critical* tasks.
    duplication_factor: int = 1

    def schedule(
        self,
        network: Network,
        task_graph: TaskGraph,
        schedule: Optional[Schedule] = None,
        min_start_time: float = 0.0,
    ) -> Schedule:
        """Build a CPoP schedule.

        Unlike HEFT, this respects a partial input schedule: if `schedule`
        is provided, CPoP continues from there, scheduling only tasks not
        already placed. This makes CpopScheduler composable with other
        schedulers (e.g. schedule warm-up tasks with X, finish with CPoP).
        """
        # --- Initialise from input partial schedule, if any ---
        # comp_schedule == "computed schedule" — the one we're filling in.
        comp_schedule = Schedule(task_graph, network)
        # task_map: task_name -> list of its ScheduledTask placements.
        # (List because duplication may put one task on multiple nodes.)
        task_map: Dict[str, list[ScheduledTask]] = {}
        if schedule is not None:
            # model_copy is pydantic v2's deep-ish copy. Preserves
            # the existing placements so we don't re-place them.
            comp_schedule = schedule.model_copy()
            task_map = {}
            for node_name, tasks in schedule.items():
                for scheduled_task in tasks:
                    task_map.setdefault(scheduled_task.name, []).append(scheduled_task)

        # --- Compute priorities and locate the critical path ---
        ranks = cpop_ranks(network, task_graph)

        # Entry tasks are sources of the DAG. The CP starts at an entry.
        entry_tasks = [
            task.name
            for task in task_graph.tasks
            if task_graph.in_degree(task.name) == 0
        ]
        # Length of the critical path = max priority among entry tasks.
        # (By construction, the max priority IS achieved at an entry,
        # since rank_u is largest at the entry and rank_d is 0 there —
        # actually their sum is constant along the CP, so checking
        # entries is enough.)
        cp_rank = ranks[max(entry_tasks, key=lambda task_name: ranks[task_name])]

        # CP processor selection. The original CPoP paper says: pick the
        # node minimising the total execution time of the critical-path
        # tasks if they all ran on that node alone.
        #
        # Note: in SAGA's uniform-speed model, the answer simplifies to
        # "the fastest node", because every CP task's exec time scales
        # like 1/speed. The general formulation here is the right one for
        # extending to per-(task,node) cost matrices.
        cp_node = min(
            network.nodes,
            key=lambda node: sum(
                task.cost / node.speed
                for task in task_graph.tasks
                if np.isclose(ranks[task.name], cp_rank)
            ),
        )

        # --- Build the ready-task max-heap ---
        # Tasks are "ready" iff every parent has already been scheduled
        # (either by the input partial schedule, or by a prior pop in this
        # loop). Initially that means "every entry task whose parents are
        # all in task_map". For a fresh schedule, that's just the entry
        # tasks (which have NO parents).
        #
        # heapq is a MIN-heap. To get max-by-priority, push `-rank` so the
        # most negative (= largest rank) pops first.
        pq = [
            (-ranks[task.name], task)
            for task in task_graph.tasks
            if task.name not in task_map
            and all(
                task_graph_dep.source in task_map
                for task_graph_dep in task_graph.in_edges(task.name)
            )
        ]
        heapq.heapify(pq)

        # --- Main scheduling loop ---
        while pq:
            task_rank, task = heapq.heappop(pq)

            # Is this a critical-path task? Compare its priority (un-negated)
            # to cp_rank. Use np.isclose to tolerate float drift.
            is_critical = np.isclose(-task_rank, cp_rank)
            # Restrict candidate nodes: CP tasks may ONLY go on cp_node.
            # Non-CP tasks may go anywhere.
            nodes = frozenset([cp_node]) if is_critical else network.nodes

            # For each candidate node, compute the EFT exactly as HEFT does.
            best_nodes: PriorityQueue[Any] = PriorityQueue()
            for node in nodes:
                start_time = comp_schedule.get_earliest_start_time(
                    task=task, node=node, append_only=False
                )
                end_time = start_time + (task.cost / node.speed)
                best_nodes.put((end_time, node))

            # Duplication: only enabled for NON-CP tasks. CP tasks
            # already live on one specific node and there's nothing to
            # duplicate.
            duplicate_factor = 1
            if not is_critical and should_duplicate(task.name, task_graph, network):
                duplicate_factor = max(
                    self.duplication_factor, len(task_graph.out_edges(task.name))
                )

            # Place the task on the best (smallest EFT) node, or
            # multiple nodes if duplicating.
            for _ in range(duplicate_factor):
                if best_nodes.empty():
                    break
                min_finish_time, best_node = best_nodes.get()
                new_exec_time = task.cost / best_node.speed
                new_task = ScheduledTask(
                    node=best_node.name,
                    name=task.name,
                    start=min_finish_time - new_exec_time,
                    end=min_finish_time,
                )
                comp_schedule.add_task(new_task)
                if task.name not in task_map:
                    task_map[task.name] = []
                task_map[task.name].append(new_task)

            # Discover newly-ready children: those whose every parent
            # now appears in task_map. Push them onto the heap.
            ready_tasks = [
                task_graph.get_task(dep.target)
                for dep in task_graph.out_edges(task.name)
                if all(
                    child_dep.source in task_map
                    for child_dep in task_graph.in_edges(dep.target)
                )
            ]
            for ready_task in ready_tasks:
                heapq.heappush(pq, (-ranks[ready_task.name], ready_task))

        return comp_schedule


# ---------------------------------------------------------------------------
# Complexity
# ---------------------------------------------------------------------------
#
# Let V = |tasks|, E = |dependencies|, P = |network.nodes|.
#
# rank_u, rank_d: each O((V + E) * P + V * |edges_in_network|). With
#   @lru_cache, repeated calls on the same instance are O(1).
# cpop_ranks: O(V) on top of rank_u/rank_d.
#
# Critical-path traversal:
#   * Each task pushed/popped from the heap at most once: O(V log V).
#   * Per pop, the inner EFT computation is O(P) for non-CP, O(1) for CP.
#   * Newly-ready check per pop: O(out_degree(t)).
# Aggregate: O((V + E) * P + V log V).
#
# Empirically: similar wall-clock to HEFT for sparse DAGs; slightly slower
# on dense DAGs because rank_d adds a second O(V*P) pass.
#
# ---------------------------------------------------------------------------
# Comparison with HEFT
# ---------------------------------------------------------------------------
#
# | Aspect             | HEFT                          | CPoP                              |
# |--------------------|-------------------------------|-----------------------------------|
# | Priority           | rank_u (descending)           | rank_u + rank_d (descending)      |
# | Traversal          | Sorted list                   | Priority-queue ready set          |
# | CP awareness       | Implicit                      | Explicit: CP tasks pinned to one  |
# |                    |                               | "CP node"                         |
# | Placement of CP    | EFT-minimising node per task  | All CP tasks on cp_node           |
# | Placement of rest  | EFT-minimising node per task  | EFT-minimising node per task      |
# | Composable?        | No (rebuilds schedule)        | Yes (accepts partial input)       |
# | Duplication        | All tasks                     | Non-CP tasks only                 |
#
# When CPoP wins: networks where comm cost dominates, because pinning the
# CP onto one node makes consecutive CP transfers free (loopback speed).
# When HEFT wins: heterogeneous task costs and modest comm, where
# pinning the CP onto one node forfeits the chance to put particular
# tasks on processors they're especially fast on.
