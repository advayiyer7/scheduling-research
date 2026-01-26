# HEFT Algorithm Annotations

## Paper Reference
**Title**: Performance-effective and low-complexity task scheduling for heterogeneous computing  
**Authors**: Topcuoglu, Hariri, Wu (IEEE TPDS 2002)

## Algorithm Overview

### Phase 1: Task Prioritization
Compute upward rank for each task:
```
rank_u(exit) = avg_cost(exit)
rank_u(task) = avg_cost(task) + max{comm(task,child) + rank_u(child)}
```

### Phase 2: Processor Selection
For each task (sorted by rank):
1. Compute EST on each processor
2. EFT = EST + execution_cost
3. Assign to processor with minimum EFT

## Code Location
`saga/src/saga/schedulers/heft.py`

## Your Annotations
<!-- Add line-by-line comments as you read the code -->

## Questions
1. How does SAGA handle insertion-based scheduling?
2. How are ties broken?
3. How are entry/exit tasks handled?