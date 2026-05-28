"""
docs/heft_annotated.py
======================

Annotated copy of `saga/src/saga/schedulers/heft.py` (SAGA v2.0.4).
Source paper: Topcuoglu, Hariri, Wu — "Performance-effective and low-complexity
task scheduling for heterogeneous computing" IEEE TPDS 2002.
DOI: https://dx.doi.org/10.1109/71.993206

HEFT in one sentence:
    Order tasks by an upward-rank priority (longest-path-to-exit estimate),
    then greedily assign each task to whatever node gives it the earliest
    finish time (EFT), allowing insertion into idle gaps.

HEFT in two phases:
    Phase 1 — Task prioritising:
        Compute `rank_u` for every task (recursive, bottom-up).
        Sort tasks by rank_u descending.
    Phase 2 — Processor selection:
        Walk tasks in that order. For each task, try every node, compute
        the earliest start time honouring (a) data-arrival constraints from
        already-scheduled parents and (b) current node occupancy (insertion
        scheduling). Pick the node with the minimum finish time. Schedule it.

Why upward rank works as a priority:
    rank_u(t) = (avg compute cost of t) + max over successors s of
                ( avg comm cost t->s + rank_u(s) )
    It approximates the length of the longest path from t to the exit task,
    in average-case execution time. Tasks with larger rank_u dominate the
    makespan, so we want them placed early when more options are open.

How SAGA's v2 model differs from the original HEFT paper:
    HEFT'02 assumes per-task per-processor compute costs w_{i,j} (an MxN
    matrix). SAGA v2 collapses this to: each task has a single `cost`, each
    node has a `speed`, and exec_time(t, n) = t.cost / n.speed. So the
    heterogeneity model is "uniform machines" (machines differ by a single
    speed scalar), not "unrelated machines" (arbitrary matrix). Network
    edges also have `speed`, so comm_time(edge, link) = edge.size / link.speed.
    For the original HEFT'02 generality, see PISA / parametric schedulers.
"""

from queue import PriorityQueue
import pathlib
from typing import Any, List, Optional
import numpy as np


from saga import Schedule, Scheduler, ScheduledTask, TaskGraph, Network
# `upward_rank` is defined in cpop.py — both HEFT and CPoP use it, so SAGA
# centralises it there (and caches it via @lru_cache for repeated calls on
# the same (network, task_graph) pair).
from saga.schedulers.cpop import upward_rank
# Optional optimisation: HEFT can duplicate a task on multiple nodes when
# communication clearly dominates computation. `should_duplicate` returns
# True when avg outgoing comm time exceeds avg compute time. By default
# duplication_factor=1 disables this.
from saga.utils.duplication import should_duplicate


thisdir = pathlib.Path(__file__).resolve().parent


def heft_rank_sort(network: Network, task_graph: TaskGraph) -> List[str]:
    """Phase 1 of HEFT: produce the ordered list of task names to schedule.

    Primary key: upward rank (descending — larger rank goes first).
    Tie-breaker: reverse topological position (later tasks first when ranks
    tie). This is a SAGA-specific choice; the HEFT paper is silent on ties.

    Why a tie-breaker matters:
        Two parallel branches of equal critical length get the same upward
        rank. Without a deterministic tie-break, different runs would
        produce different schedules. SAGA picks reverse-topological so
        leafier tasks dispatch first, which tends to free up downstream
        scheduling decisions.
    """
    # rank_u(task_name) -> float, computed bottom-up. See cpop.upward_rank
    # for the recursion; effectively dynamic programming over a reverse
    # topological walk.
    urank = upward_rank(network, task_graph)

    # Build a secondary ordering on tasks. `topological_sort()` gives
    # parents before children; we reverse, then index, so that a task
    # appearing later in topo order gets a LARGER number. That number is
    # used only to break ties on `urank` (larger wins because we sort
    # reverse=True below).
    topological_sort = {
        node.name: i for i, node in enumerate(reversed(task_graph.topological_sort()))
    }

    # Composite key: (urank, topo_position). Sort descending on the tuple.
    rank = {node: (urank[node], topological_sort[node]) for node in urank}
    order = sorted(list(rank.keys()), key=lambda x: rank.get(x, 0.0), reverse=True)
    return order


class HeftScheduler(Scheduler):
    """Heterogeneous Earliest Finish Time (HEFT) scheduler.

    Implements Algorithm 1 from Topcuoglu et al. 2002, adapted to SAGA v2's
    uniform-machines data model.

    Attributes:
        duplication_factor: Maximum number of nodes a single task may be
            duplicated onto. Default 1 = no duplication (standard HEFT).
            Higher values enable an extension that helps when comm cost
            dominates compute cost. Vanilla HEFT'02 does NOT include
            duplication; this is a SAGA add-on.
    """

    duplication_factor: int = 1

    def schedule(
        self,
        network: Network,
        task_graph: TaskGraph,
        schedule: Optional[Schedule] = None,
        min_start_time: float = 0.0,
    ) -> Schedule:
        """Produce a schedule for `task_graph` on `network`.

        Args:
            network: The compute fabric (nodes + links).
            task_graph: The DAG of tasks to place.
            schedule: Currently unused by HEFT (CPoP supports this — for
                composing with another scheduler that placed some tasks
                already). Ignored here; a fresh Schedule is built.
            min_start_time: Floor for task start times (useful when this
                scheduler is invoked as a sub-routine after time t).

        Returns:
            A complete Schedule covering every task in task_graph.
        """
        # ---- Phase 1: priority order ----
        schedule_order = heft_rank_sort(network, task_graph)

        # Schedule starts empty. Each node maps to an (initially empty) list
        # of ScheduledTask. The `min_start_time` argument is honoured per
        # task below, not stored on the Schedule object itself.
        schedule = Schedule(task_graph, network)

        # ---- Phase 2: place each task on its EFT-minimising node ----
        for task_name in schedule_order:
            task = task_graph.get_task(task_name)

            # If duplication placed this task earlier in an earlier loop
            # iteration, skip. (Happens only when duplication_factor > 1.)
            if schedule.is_scheduled(task_name):
                continue

            # Decide whether to duplicate this task. Off by default
            # (factor=1). The duplication count is bounded by the number of
            # out-edges — duplicating beyond the number of children buys
            # nothing because there's no consumer waiting on the extra copy.
            duplicate_factor = 1
            if should_duplicate(task_name, task_graph, network):
                duplicate_factor = min(
                    self.duplication_factor, len(task_graph.out_edges(task_name))
                )

            # For each candidate node, compute the finish time we'd achieve
            # if we placed this task there. Stash (finish_time, node) in a
            # PriorityQueue so the smallest finish time pops first.
            min_finish_time = np.inf
            best_nodes: PriorityQueue[Any] = PriorityQueue()
            for node in network.nodes:
                # `get_earliest_start_time` (in saga/__init__.py) does the
                # real work of HEFT's "insertion-based scheduling":
                #   - It looks at every parent's scheduled finish + comm
                #     time, takes the max (when can the data arrive?).
                #   - With append_only=False it also scans the existing
                #     gaps on this node and returns the earliest slot the
                #     task fits into. This is the "insertion policy" from
                #     the HEFT paper, not pure append-only.
                start_time = schedule.get_earliest_start_time(
                    task=task, node=node, append_only=False
                )
                # Respect the caller's floor.
                start_time = max(start_time, min_start_time)
                # SAGA v2 exec time model: cost / speed. (HEFT'02 instead
                # has a per-(task,proc) matrix w_{i,j}; SAGA collapses that
                # to one scalar per task and one per node.)
                runtime = (
                    task_graph.get_task(task_name).cost / network.get_node(node).speed
                )
                finish_time = start_time + runtime
                # Smallest finish_time = best node in standard HEFT.
                best_nodes.put((finish_time, node))

            # Pop the best (lowest-EFT) node(s) and place the task there.
            # With duplicate_factor==1 this places once; with >1 it places
            # on the next-best nodes too, creating duplicate copies that
            # the parent feeds in parallel.
            for _ in range(duplicate_factor):
                if best_nodes.empty():
                    break
                min_finish_time, best_node = best_nodes.get()

                # Recover start from end so the placed interval is
                # consistent with the EFT we computed for this node. We
                # must recompute exec time using *this* node's speed
                # (since each duplicate goes on a different node).
                new_task = ScheduledTask(
                    node=best_node.name,
                    name=task_name,
                    start=min_finish_time
                    - (
                        task_graph.get_task(task_name).cost
                        / best_node.speed
                    ),
                    end=min_finish_time,
                )
                schedule.add_task(new_task)

        return schedule


# ---------------------------------------------------------------------------
# Complexity
# ---------------------------------------------------------------------------
#
# Let V = |tasks|, E = |dependencies|, P = |network.nodes|.
#
# Phase 1 — upward_rank (in cpop.py):
#   * topological_sort: O(V + E)
#   * For each task: O(avg compute over P nodes) = O(P)
#                    O(max over successors, each averaged over |network.edges|)
#                    Worst case O(V * P^2) for dense networks; typically
#                    O((V + E) * P) for sparse ones.
#   The result is cached by @lru_cache so subsequent calls on the same
#   (network, task_graph) cost O(1) lookup.
#
# Phase 2 — heft_rank_sort + scheduling loop:
#   * Sort: O(V log V).
#   * For each task: O(P) nodes considered, each calling
#     get_earliest_start_time which is O(|in_edges(task)| + |tasks on node|).
#   Aggregate: O(V * P * (E/V + V/P)) = O(V*E*P/V + V*V) ≈ O(P*E + V^2).
#
# Practical observation: P (procs) is small (4-32), V (tasks) is the driver.
# HEFT runs in ms for V up to ~10k.
#
# ---------------------------------------------------------------------------
# Things this implementation does NOT do (compared to literature variants)
# ---------------------------------------------------------------------------
#
# * Lookahead-HEFT: pick the node that minimises EFT of the CURRENT task
#   AND the EFTs of its already-rank-prioritised children. Not implemented.
# * HEFT with task replication for fault tolerance: different from the
#   `duplication_factor` add-on here.
# * Stochastic / robust HEFT (tasks with cost distributions): see
#   saga/schedulers/stochastic/.
# * Heterogeneous link speeds are honoured, but the rank computation uses
#   the MEAN link speed (np.mean over network.edges), so very heterogeneous
#   networks can mis-rank tasks. Parametric / per-pair-aware variants exist
#   in saga/schedulers/parametric/.
