# SAGA Architecture (v2.0.4)

Reference doc for the SAGA framework's core abstractions. Everything below
is taken from `saga/src/saga/__init__.py` (the entire core lives in this
single file) and the scheduler base classes.

This document covers SAGA v2.0.4. Note: earlier versions (≤1.x) used a
different API (`saga.data.Task`, `Processor`, `Link`, per-(task,proc) cost
matrices). Anything in the project's older docs referring to those types
is out of date.

---

## 1. Module layout

```
saga/src/saga/
├── __init__.py            ← all core types: Network, TaskGraph, Schedule,
│                            Scheduler, ScheduledTask, NetworkNode,
│                            NetworkEdge, TaskGraphNode, TaskGraphEdge
├── schedulers/
│   ├── __init__.py        ← re-exports the 23 concrete schedulers
│   ├── heft.py            ← HeftScheduler
│   ├── cpop.py            ← CpopScheduler + upward_rank, downward_rank
│   ├── … (21 others)
│   ├── parametric/        ← parametrised schedulers (per-(task,proc)
│   │                        cost matrices, advanced cost models)
│   └── stochastic/        ← scheduling under uncertainty
├── pisa/                  ← Problem-Instance-Sampling Adversary;
│                            generates hard task graphs
└── utils/
    ├── duplication.py     ← should_duplicate() helper
    └── draw.py            ← matplotlib visualisations (Gantt, graph)
```

---

## 2. Data model

### 2.1 NetworkNode

```python
class NetworkNode(BaseModel):
    name: str
    speed: float
```

A compute node. `speed` is a scalar — a node's execution rate.
Execution time of a task on a node is `task.cost / node.speed`. This is the
*uniform machines* model: every node runs every task; the only difference
is a constant speed factor.

### 2.2 NetworkEdge

```python
class NetworkEdge(BaseModel):
    source: str   # name of source node
    target: str   # name of target node
    speed: float  # bandwidth
```

A communication link. Communication time of a dependency `(t1 -> t2)` over
edge `(n1, n2)` is `dependency.size / edge.speed`.

**Self-loops (`source == target`)**: SAGA auto-fills these with `speed = inf`,
meaning intra-node communication is free. So when a task's parent and the
task itself land on the same node, comm cost is zero. When they land on
different nodes, comm cost is `data_size / link_speed`.

**Default edge speed for missing pairs**: `Network.create` fills in any
missing inter-node edges with `speed = 0.0`. **Watch out**: 0.0 means a
divide-by-zero risk in scheduler code. If you build networks by hand,
ensure every pair of nodes has an explicit edge.

### 2.3 Network

```python
class Network(BaseModel):
    nodes: FrozenSet[NetworkNode]
    edges: FrozenSet[NetworkEdge]
```

Frozen — once built, the structure is immutable. `model_config = {"frozen": True}`.

Construction:
- `Network.create(nodes=[...], edges=[...])` — accepts either typed objects
  or `(name, speed)` and `(src, tgt, speed)` tuples.
- `Network.from_nx(nx_graph)` — convert a `networkx.Graph` where each node
  has a `weight` attribute (used as speed) and each edge has a `weight`
  attribute (used as link speed).

Useful methods:
- `get_node(name)`, `get_edge(src, tgt)`
- `network.graph` — cached `nx.Graph` view of the network.
- `scale_to_ccr(task_graph, target_ccr)` — rescales link speeds so the
  network's communication-to-computation ratio matches a target. Critical
  for benchmarking across CCR sweeps in Phase 2.

### 2.4 TaskGraphNode

```python
class TaskGraphNode(BaseModel):
    name: str
    cost: float
```

A task with **one** computation cost. No per-processor heterogeneity in
this scalar — heterogeneity comes from the network's per-node `speed`.
For non-uniform models (different cost on each processor), use the
`schedulers.parametric` submodule.

### 2.5 TaskGraphEdge

```python
class TaskGraphEdge(BaseModel):
    source: str
    target: str
    size: float
```

A data dependency. `size` is the amount of data passed from `source` to
`target`. Combined with an edge in the network, gives a comm time.

### 2.6 TaskGraph

```python
class TaskGraph(BaseModel):
    tasks: FrozenSet[TaskGraphNode]
    dependencies: FrozenSet[TaskGraphEdge]
```

Frozen.

Construction:
- `TaskGraph.create(tasks=[...], dependencies=[...])`
- `TaskGraph.from_nx(nx_digraph)` — uses `weight` attr for cost (nodes) and
  data size (edges).

**Auto-injection of super-source / super-sink**: If the DAG has more than
one source (in-degree-zero task), `TaskGraph.create` automatically adds a
synthetic `__super_source__` task with cost 0, with 0-size edges to all
real sources. Same for sinks → `__super_sink__`. This means every SAGA
DAG effectively has a single entry and single exit, which lets schedulers
assume that. (HEFT and CPoP rely on this.)

Useful methods:
- `get_task(name)`, `get_dependency(src, tgt)`
- `in_edges(task)` / `out_edges(task)` → `List[TaskGraphEdge]`
- `in_degree(task)` / `out_degree(task)` → int
- `topological_sort()` → `List[TaskGraphNode]` in dependency order.
- `all_topological_sorts()` — generator, useful for exhaustive search
  (BruteForce scheduler).
- `task_graph.graph` — cached `nx.DiGraph` view.

---

## 3. Schedule

### 3.1 ScheduledTask

```python
class ScheduledTask(BaseModel):
    node: str
    name: str
    start: float
    end: float
```

A single placement: task `name` runs on node `node` over interval
`[start, end]`. Duration must equal `task.cost / node.speed` (the
scheduler is responsible for computing this consistently).

### 3.2 Schedule

```python
class Schedule(BaseModel):
    task_graph: TaskGraph
    network: Network
    mapping: Dict[str, List[ScheduledTask]]
    _task_map: Dict[str, List[ScheduledTask]]  # private, keyed by task name
```

Two indices over the same set of placements:
- `mapping[node_name]` → list of tasks on that node, **sorted by start
  time**. `add_task` uses `bisect` to maintain the order, and checks that
  consecutive tasks don't overlap (within `EPS = 1e-9`).
- `_task_map[task_name]` → list of `ScheduledTask` for that task (multiple
  entries when a task is duplicated across nodes).

Key methods:

- `schedule.makespan` — `max(tasks[-1].end for tasks in mapping.values())`.
  Returns 0.0 for empty schedules.

- `schedule.get_earliest_start_time(task, node, append_only=False)` —
  **This is the workhorse**. Computes when `task` could start on `node`
  given the current state of the schedule.

  Two constraints are applied:
  1. **Data arrival**: for each parent `p` of `task`, find the earliest
     time the data arrives at `node`. If `p` is duplicated, use the
     duplicate that delivers earliest. Take the max across all parents.
  2. **Node occupancy**: with `append_only=True`, just put the task at
     the end of the node's queue (after `mapping[node][-1].end`). With
     `append_only=False` (the default — used by HEFT, CPoP, etc.), scan
     existing gaps and return the earliest gap that fits the task.
     This is HEFT's "insertion-based policy".

- `schedule.add_task(scheduled_task)` — bisect-insert into the right
  node's list, raise `ValueError` on overlap with the following task.

- `schedule.is_scheduled(task_name)` — True if any node holds it.

- `schedule.get_scheduled_task(task_name)` — returns the list of
  placements (may be >1 with duplication).

- `schedule.remove_task(task_name)` — symmetric to `add_task`.

---

## 4. Scheduler (the base class)

```python
class Scheduler(ABC, BaseModel):
    @abstractmethod
    def schedule(self, network: Network, task_graph: TaskGraph) -> Schedule:
        ...

    @property
    def name(self) -> str:
        return self.__class__.__name__
```

Minimal interface. Concrete schedulers extend it.

Conventions concrete schedulers follow (not enforced by the ABC):
- Accept extra kwargs `schedule: Optional[Schedule] = None` (initial
  partial schedule — composability) and `min_start_time: float = 0.0`.
- Return a fresh `Schedule` object covering every task in the task graph.
- Are deterministic given the same `(network, task_graph)`.

The 23 concrete schedulers (re-exported from `saga.schedulers`):

| Category           | Schedulers                                                                            |
|--------------------|---------------------------------------------------------------------------------------|
| Classic list-based | HeftScheduler, CpopScheduler, FCPScheduler, DPSScheduler, ETFScheduler, GDLScheduler  |
| Greedy heuristics  | MinMinScheduler, MaxMinScheduler, MCTScheduler, METScheduler, OLBScheduler, SufferageScheduler |
| Other              | FLBScheduler, HbmctScheduler, MsbcScheduler, WBAScheduler, BILScheduler, DuplexScheduler, FastestNodeScheduler, MSTScheduler |
| Optimal (slow)     | BruteForceScheduler, SMTScheduler                                                     |
| Composite          | HybridScheduler                                                                       |

---

## 5. Common patterns

### Building an instance

```python
import networkx as nx
from saga import Network, TaskGraph

# Network: undirected graph; node weight = speed, edge weight = bandwidth.
net_g = nx.Graph()
net_g.add_node("P0", weight=1.0)
net_g.add_node("P1", weight=2.0)
net_g.add_edge("P0", "P1", weight=1.0)
network = Network.from_nx(net_g)

# Task graph: DAG; node weight = compute cost, edge weight = data size.
tg = nx.DiGraph()
tg.add_node("T0", weight=10.0)
tg.add_node("T1", weight=5.0)
tg.add_edge("T0", "T1", weight=3.0)
task_graph = TaskGraph.from_nx(tg)
```

### Running a scheduler

```python
from saga.schedulers import HeftScheduler
sched = HeftScheduler().schedule(network, task_graph)
print(sched.makespan)
for node_name, tasks in sched.mapping.items():
    for t in tasks:
        print(f"{node_name}: {t.name} [{t.start:.2f}, {t.end:.2f}]")
```

### Sweeping CCR

```python
for ccr in [0.1, 0.5, 1.0, 2.0, 5.0]:
    scaled = network.scale_to_ccr(task_graph, ccr)
    sched = HeftScheduler().schedule(scaled, task_graph)
    print(f"CCR {ccr}: makespan {sched.makespan:.2f}")
```

---

## 6. Gotchas

1. **Pydantic v2, not v1.** `TaskGraph`/`Network` are pydantic models.
   They're hashable (cached `computed_hash`) and frozen, so they work as
   `@lru_cache` keys (which is how `upward_rank` and `cpop_ranks` cache).

2. **`FrozenSet` order is not deterministic across runs.** Don't rely on
   `for node in network.nodes: ...` returning nodes in the same order in
   different Python sessions. Schedulers that sort internally (HEFT, CPoP)
   are fine; schedulers that don't sort can produce non-reproducible
   schedules. If reproducibility matters, sort by `node.name` first.

3. **Self-loop edges**: `Network.create` auto-adds self-loops with
   `speed = inf`. So `network.get_edge("P0", "P0").speed == inf`. This
   makes `data_size / speed == 0` for intra-node comms, which is what
   you want.

4. **`scale_to_ccr` clobbers self-loops** (verified by direct test).
   Before scaling, self-loops have `speed = inf` so intra-node parent→child
   comm is free. After `scale_to_ccr(target_ccr)`, every edge is rewritten
   to the same scaled `link_speed`, **including self-loops**. So
   `data_size / link_speed > 0` for same-node comm post-scaling.

   Consequence for Phase 2 benchmarking: schedulers that pin
   parent+child onto the same node (CPoP for the CP, FastestNode always)
   pay non-trivial intra-node comm after `scale_to_ccr`. To restore the
   free-loopback model, rebuild the scaled network with explicit self-loops
   at `inf`, e.g.:

   ```python
   from saga import Network, NetworkEdge
   scaled = network.scale_to_ccr(task_graph, target_ccr=ccr)
   fixed_edges = {
       NetworkEdge(source=e.source, target=e.target,
                   speed=math.inf if e.source == e.target else e.speed)
       for e in scaled.edges
   }
   scaled = Network(nodes=scaled.nodes, edges=frozenset(fixed_edges))
   ```

5. **The `EPS = 1e-9` tolerance in `add_task`** means schedules with
   sub-nanosecond gaps may be flagged as overlapping. If you write a
   custom scheduler that produces back-to-back placements, prefer to
   compute `start = previous_task.end` exactly rather than via floating
   point arithmetic that may introduce drift.

6. **Caching is per-process and unbounded.** `upward_rank` and
   `cpop_ranks` use `@lru_cache(maxsize=None)`. Long-running benchmark
   sweeps over many problem instances will accumulate cache entries.
   Call `upward_rank.cache_clear()` between unrelated sweeps if memory
   matters.
