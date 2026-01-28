# HEFT Implementation Study Guide

## Your Task

Open `saga/src/saga/schedulers/heft.py` in VS Code and add detailed comments explaining each section.

## How to Open the File

In VS Code, press `Ctrl+P` and type:
```
saga/src/saga/schedulers/heft.py
```

## What to Look For

### 1. Class Structure
- Find the `HeftScheduler` class
- Identify the main `schedule()` method
- Find helper methods for rank calculation

### 2. Upward Rank Calculation
Look for code that computes priority. The formula is:
```
rank_u(task) = avg_cost(task) + max{comm_cost + rank_u(successor)}
```

Questions to answer:
- How does SAGA calculate average computation cost?
- How are successors traversed (BFS, DFS, recursion)?
- How is communication cost computed?

### 3. Task Ordering
Look for code that sorts tasks by rank:
```python
# Something like:
sorted_tasks = sorted(tasks, key=lambda t: rank[t], reverse=True)
```

### 4. Processor Selection (EFT)
Look for the loop that assigns tasks to processors:
```python
# Something like:
for task in sorted_tasks:
    best_processor = None
    best_eft = infinity
    for processor in processors:
        eft = calculate_eft(task, processor)
        if eft < best_eft:
            best_eft = eft
            best_processor = processor
    assign(task, best_processor)
```

### 5. EST Calculation
Earliest Start Time depends on:
- When the processor is free
- When all predecessor data arrives

Look for:
```python
est = max(processor_available, max(predecessor_finish + comm_cost))
```

---

## Annotation Template

Create a new file `docs/heft_code_annotations.md` with your findings:

```markdown
# HEFT Code Annotations

## File: saga/src/saga/schedulers/heft.py

### Line XX-YY: Rank Calculation

```python
# paste code here
```

**Explanation**: This section computes the upward rank by...

### Line XX-YY: Task Sorting

```python
# paste code here
```

**Explanation**: Tasks are sorted in decreasing rank order because...

### Line XX-YY: Processor Selection

```python
# paste code here  
```

**Explanation**: For each task, we iterate through processors to find...

## Key Observations

1. ...
2. ...

## Differences from Paper

1. ...
```

---

## Questions to Answer in Your Annotations

1. **Data Structures**: What structures hold the schedule? (dict, list, custom class?)

2. **Insertion Policy**: Does SAGA use insertion-based scheduling (filling gaps)?

3. **Tie Breaking**: When two processors have the same EFT, which is chosen?

4. **Communication**: How is comm cost handled when tasks are on same processor?

5. **Complexity**: What's the time complexity? (Should be O(n²p) where n=tasks, p=processors)

---

## After Annotating HEFT

Do the same for CPoP:
```
saga/src/saga/schedulers/cpop.py
```

CPoP differences from HEFT:
- Uses both upward AND downward rank
- Identifies critical path
- Assigns critical path tasks to single "critical path processor"