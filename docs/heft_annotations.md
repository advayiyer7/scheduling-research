# HEFT Algorithm Annotations

## Paper Reference
**Title**: Performance-effective and low-complexity task scheduling for heterogeneous computing  
**Authors**: Topcuoglu, Hariri, Wu  
**Published**: IEEE TPDS 2002  
**Link**: https://ieeexplore.ieee.org/document/765092

## Algorithm Summary

HEFT is a list-based scheduling heuristic with two phases:

### Phase 1: Task Prioritization

Compute **upward rank** (rank_u) for each task, starting from exit task:

```
rank_u(n_exit) = w̄(n_exit)

rank_u(n_i) = w̄(n_i) + max{c̄(i,j) + rank_u(n_j)} for all successors n_j
```

Where:
- `w̄(n_i)` = average computation cost of task n_i across all processors
- `c̄(i,j)` = average communication cost from task i to task j

Tasks are sorted by **decreasing rank_u** (highest priority first).

### Phase 2: Processor Selection

For each task in priority order:
1. For each processor p, calculate **Earliest Finish Time (EFT)**:
   ```
   EFT(n_i, p_j) = EST(n_i, p_j) + w(n_i, p_j)
   ```
2. Assign task to processor with **minimum EFT**

**Earliest Start Time (EST)**:
```
EST(n_entry, p_j) = 0

EST(n_i, p_j) = max{avail(p_j), max{AFT(n_m) + c(m,i)} for all predecessors n_m}
```

Where:
- `avail(p_j)` = when processor p_j becomes available
- `AFT(n_m)` = actual finish time of predecessor task
- `c(m,i)` = communication cost (0 if same processor)

---

## SAGA Implementation

**File**: `saga/src/saga/schedulers/heft.py`

### Key Functions to Annotate

#### 1. Rank Calculation
```python
# TODO: Copy the _compute_rank or similar function
# Add comments explaining each line
```

#### 2. Processor Selection  
```python
# TODO: Copy the scheduling loop
# Explain EFT calculation
```

#### 3. Schedule Construction
```python
# TODO: Document how the final schedule is built
```

---

## My Annotations

<!-- 
Add your line-by-line annotations below.
Format:
```python
# Line of code from heft.py
# ^ My explanation of what this does
```
-->

### _compute_upward_rank function

```python
# TODO: Add annotated code here
```

### schedule method

```python
# TODO: Add annotated code here
```

---

## Questions

- [ ] How does SAGA handle the insertion-based scheduling policy?
- [ ] How are ties broken when multiple processors have same EFT?
- [ ] How is communication cost calculated when tasks are on same processor?
- [ ] What data structures are used for efficiency?

## Differences from Paper

<!-- Note any differences between SAGA implementation and paper description -->

---

## References

- Original paper: Topcuoglu et al., IEEE TPDS 2002
- SAGA implementation: `saga/src/saga/schedulers/heft.py`