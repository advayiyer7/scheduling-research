# HEFT Code Annotations

**File analyzed**: `saga/src/saga/schedulers/heft.py`  
**Date**: [Fill in]  
**Author**: Advay

---

## Overview

The HEFT scheduler is implemented in approximately [X] lines of code. The main class is `HeftScheduler` which inherits from [parent class].

---

## Class Structure

```python
class HeftScheduler:
    # TODO: Document the class structure
    pass
```

**Notes**: 

---

## 1. Upward Rank Calculation

### Code (Lines XX-YY)

```python
# TODO: Paste the rank calculation code here
```

### Explanation

The upward rank is calculated by...

### Mapping to Paper

Paper equation (Section 3.1):
```
rank_u(n_i) = w̄_i + max_{n_j ∈ succ(n_i)} (c̄_{i,j} + rank_u(n_j))
```

In the code:
- `w̄_i` (average computation) is computed by...
- `c̄_{i,j}` (average communication) is computed by...
- The max over successors is done using...

---

## 2. Task Prioritization

### Code (Lines XX-YY)

```python
# TODO: Paste the task sorting code here
```

### Explanation

Tasks are sorted by...

---

## 3. Processor Selection (EFT)

### Code (Lines XX-YY)

```python
# TODO: Paste the EFT calculation code here
```

### Explanation

For each task, the Earliest Finish Time on each processor is calculated as...

### EST Calculation

```python
# TODO: Paste EST calculation
```

EST = max(processor_available_time, max(data_arrival_times))

---

## 4. Schedule Construction

### Code (Lines XX-YY)

```python
# TODO: Paste schedule building code
```

### Explanation

The final schedule is stored in...

---

## Key Data Structures

| Variable | Type | Purpose |
|----------|------|---------|
| | | |
| | | |
| | | |

---

## Answers to Key Questions

### 1. Does SAGA use insertion-based scheduling?

[Your answer]

### 2. How are ties broken?

[Your answer]

### 3. How is communication cost handled for same-processor tasks?

[Your answer]

### 4. What is the time complexity?

[Your answer]

---

## Differences from Paper

1. [Any differences you noticed]

---

## Things I Learned

1. 
2. 
3. 

---

## Questions for Professor

1. 
2.