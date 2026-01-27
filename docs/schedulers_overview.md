# SAGA Schedulers Overview

## Summary

SAGA includes 23 scheduling algorithms. This document categorizes them and provides brief descriptions.

## Categories

### 1. Classic Heuristics (Priority-Based)

| Scheduler | Full Name | Description |
|-----------|-----------|-------------|
| **HeftScheduler** | Heterogeneous Earliest Finish Time | Upward rank priority, EFT processor selection |
| **CpopScheduler** | Critical Path on Processor | Prioritizes critical path tasks |
| **FCPScheduler** | Fast Critical Path | Faster variant of critical path methods |
| **DPSScheduler** | Dynamic Priority Scheduling | Dynamic priority adjustment |
| **ETFScheduler** | Earliest Task First | Based on earliest start times |

### 2. List Scheduling

| Scheduler | Full Name | Description |
|-----------|-----------|-------------|
| **MinMinScheduler** | Minimum-Minimum | Assigns task with min completion time |
| **MaxMinScheduler** | Maximum-Minimum | Opposite of MinMin |
| **MCTScheduler** | Minimum Completion Time | Greedy completion time |
| **METScheduler** | Minimum Execution Time | Greedy execution time |
| **OLBScheduler** | Opportunistic Load Balancing | Random assignment |
| **SufferageScheduler** | Sufferage | Based on "sufferage" value |

### 3. Optimal/Exact

| Scheduler | Description |
|-----------|-------------|
| **BruteForceScheduler** | Tries all permutations (slow, optimal) |
| **SMTScheduler** | SAT/SMT solver (optimal for small problems) |

### 4. Other Heuristics

| Scheduler | Notes |
|-----------|-------|
| **FLBScheduler** | Fast Load Balancing |
| **GDLScheduler** | Guided by Deadline |
| **HbmctScheduler** | HEFT-based MCT |
| **MsbcScheduler** | Modified Score-Based Clustering |
| **WBAScheduler** | Workflow-Based Algorithm |
| **BILScheduler** | Best Imaginary Level |
| **DuplexScheduler** | Duplex scheduling |
| **FastestNodeScheduler** | Assigns to fastest node |
| **MSTScheduler** | Minimum Spanning Tree based |
| **HybridScheduler** | Combination approach |

## Priority for Study

1. **HeftScheduler** - Most cited, need to annotate
2. **CpopScheduler** - Same paper as HEFT, need to annotate
3. **MinMinScheduler** - Simple baseline
4. **BruteForceScheduler** - Optimal reference
5. Others as needed

## Code Locations

All schedulers in: `saga/src/saga/schedulers/`

Key files:
- `heft.py` - HEFT implementation
- `cpop.py` - CPoP implementation
- `base.py` - Base scheduler class