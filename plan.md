# Research Execution Plan

## Instructions for Claude Code

This document outlines a comprehensive plan to complete the scheduling algorithms research project. Execute tasks in order, committing progress after each major milestone.

---

## Phase 1: Code Understanding & Annotations (Days 1-2)

### Task 1.1: Analyze HEFT Implementation
```bash
# Open and analyze this file
cat saga/src/saga/schedulers/heft.py
```

**Deliverable**: Create `docs/heft_annotated.py` - a copy of heft.py with detailed inline comments explaining:
- How upward rank is calculated
- How tasks are sorted
- How EFT (Earliest Finish Time) is computed
- How processor selection works
- Data structures used

### Task 1.2: Analyze CPoP Implementation
```bash
cat saga/src/saga/schedulers/cpop.py
```

**Deliverable**: Create `docs/cpop_annotated.py` with same level of detail.

### Task 1.3: Analyze Base Classes
```bash
cat saga/src/saga/schedulers/base.py
cat saga/src/saga/data/task_graph.py
cat saga/src/saga/data/network.py
```

**Deliverable**: Create `docs/saga_architecture.md` explaining:
- Scheduler base class interface
- TaskGraph structure and methods
- Network structure and methods
- How schedules are represented

---

## Phase 2: Comprehensive Benchmarking (Days 3-5)

### Task 2.1: Create Benchmark Suite
**Deliverable**: Create `experiments/benchmark_suite.py`

```python
"""
Benchmark all 23 SAGA schedulers on multiple problem instances.
Vary: graph size, graph shape, CCR (communication-to-computation ratio), processor count
Output: CSV files with results
"""
```

Requirements:
- Test all 23 schedulers
- Problem sizes: 10, 20, 50, 100, 200 tasks
- Graph types: chain, diamond, fork-join, random DAG
- CCR values: 0.1, 0.5, 1.0, 2.0, 5.0
- Processor counts: 2, 4, 8, 16
- Measure: makespan, runtime, schedule length ratio (SLR)
- Save results to `experiments/results/benchmark_results.csv`

### Task 2.2: Create Problem Generators
**Deliverable**: Create `src/generators/task_graphs.py`

```python
"""
Generate various task graph structures for benchmarking.
"""
def generate_chain(n_tasks, heterogeneity=0.5): ...
def generate_diamond(n_tasks): ...
def generate_fork_join(n_tasks, width): ...
def generate_random_dag(n_tasks, edge_prob, ccr): ...
def generate_stg(n_tasks):  # Standard Task Graph format
```

### Task 2.3: Run Full Benchmark
```bash
python experiments/benchmark_suite.py --all
```

**Deliverable**: `experiments/results/benchmark_results.csv` with columns:
- scheduler, graph_type, n_tasks, n_processors, ccr, makespan, runtime_ms, slr

---

## Phase 3: Analysis & Visualization (Days 6-7)

### Task 3.1: Create Analysis Script
**Deliverable**: Create `experiments/analyze_results.py`

Generate these visualizations:
1. **Heatmap**: Scheduler × Graph Type → Average SLR
2. **Line plot**: Makespan vs. Number of Tasks (per scheduler)
3. **Box plot**: Makespan distribution per scheduler
4. **Bar chart**: Average runtime per scheduler
5. **Scatter**: CCR vs. Best Scheduler

Save all plots to `experiments/figures/`

### Task 3.2: Create Summary Report
**Deliverable**: Create `experiments/results/benchmark_report.md`

Include:
- Executive summary of findings
- Best scheduler for each scenario
- Statistical analysis (mean, std, p-values)
- Embedded figures
- Recommendations

---

## Phase 4: Custom Scheduler Implementation (Days 8-10)

### Task 4.1: Implement Hybrid Scheduler
**Deliverable**: Create `src/schedulers/hybrid_heft.py`

Implement a scheduler that:
- Uses HEFT ranking
- Applies lookahead for processor selection
- Considers insertion-based scheduling
- Must pass SAGA's test suite

### Task 4.2: Implement Learned Heuristic Selector
**Deliverable**: Create `src/schedulers/meta_scheduler.py`

A meta-scheduler that:
- Analyzes task graph features (size, CCR, critical path ratio, parallelism)
- Selects best scheduler from portfolio based on features
- Uses simple decision tree or rules learned from benchmark data

### Task 4.3: Test Custom Schedulers
```bash
pytest tests/test_custom_schedulers.py
```

**Deliverable**: Create `tests/test_custom_schedulers.py`

---

## Phase 5: GNN Scheduler Predictor (Days 11-15)

### Task 5.1: Data Preparation
**Deliverable**: Create `src/models/data_prep.py`

- Convert task graphs to PyTorch Geometric format
- Extract node features: computation cost, in-degree, out-degree, rank
- Extract edge features: communication cost, data size
- Extract graph-level features: size, CCR, width, depth
- Create train/val/test splits

### Task 5.2: GNN Model Architecture
**Deliverable**: Create `src/models/gnn_scheduler.py`

```python
"""
Graph Neural Network that predicts:
Option A: Best scheduler for a given problem (classification)
Option B: Task priorities directly (regression)
Option C: Task-to-processor assignment (node classification)
"""

class SchedulerGNN(torch.nn.Module):
    def __init__(self):
        # Graph convolution layers
        # Global pooling
        # MLP head
```

Use:
- PyTorch Geometric
- GCN or GAT layers
- Global mean/max pooling
- Classification head for scheduler selection

### Task 5.3: Training Pipeline
**Deliverable**: Create `src/models/train.py`

- Training loop with validation
- Early stopping
- Model checkpointing
- Logging (tensorboard or wandb)
- Hyperparameter config

### Task 5.4: Evaluation
**Deliverable**: Create `src/models/evaluate.py`

- Test set accuracy
- Comparison: GNN selection vs. always-HEFT vs. oracle
- Makespan improvement statistics
- Confusion matrix for scheduler selection

---

## Phase 6: Results & Paper-Ready Figures (Days 16-18)

### Task 6.1: Generate Publication Figures
**Deliverable**: Create `experiments/generate_paper_figures.py`

Generate high-quality figures:
- Figure 1: Scheduler comparison across problem sizes
- Figure 2: Impact of CCR on scheduler performance
- Figure 3: GNN prediction accuracy
- Figure 4: Makespan improvement with GNN selector
- Figure 5: Runtime comparison

Settings:
- Use matplotlib with publication style
- Font size 12+
- PDF/SVG output
- Color-blind friendly palette

### Task 6.2: Create Results Tables
**Deliverable**: Create `experiments/results/tables.md`

LaTeX-ready tables:
- Table 1: Benchmark summary statistics
- Table 2: Best scheduler per scenario
- Table 3: GNN model performance
- Table 4: Comparison with baselines

### Task 6.3: Final Report
**Deliverable**: Create `docs/final_report.md`

Sections:
1. Introduction & Motivation
2. Background (HEFT, CPoP, scheduling theory)
3. Methodology (benchmarking, GNN approach)
4. Experimental Setup
5. Results & Analysis
6. Conclusions
7. Future Work

---

## File Structure After Completion

```
scheduling-research/
├── docs/
│   ├── heft_annotated.py
│   ├── cpop_annotated.py
│   ├── saga_architecture.md
│   └── final_report.md
├── experiments/
│   ├── benchmark_suite.py
│   ├── analyze_results.py
│   ├── generate_paper_figures.py
│   ├── results/
│   │   ├── benchmark_results.csv
│   │   ├── benchmark_report.md
│   │   └── tables.md
│   └── figures/
│       ├── scheduler_comparison.pdf
│       ├── ccr_impact.pdf
│       └── gnn_accuracy.pdf
├── src/
│   ├── generators/
│   │   └── task_graphs.py
│   ├── schedulers/
│   │   ├── hybrid_heft.py
│   │   └── meta_scheduler.py
│   └── models/
│       ├── data_prep.py
│       ├── gnn_scheduler.py
│       ├── train.py
│       └── evaluate.py
├── tests/
│   └── test_custom_schedulers.py
└── checkpoints/
    └── gnn_model.pt
```

---

## Quick Commands

```bash
# Run benchmarks
python experiments/benchmark_suite.py --all

# Analyze results
python experiments/analyze_results.py

# Train GNN
python src/models/train.py --epochs 100 --lr 0.001

# Evaluate
python src/models/evaluate.py --checkpoint checkpoints/best.pt

# Generate figures
python experiments/generate_paper_figures.py
```

---

## Success Criteria

1. ✅ All 23 schedulers benchmarked on 100+ problem instances
2. ✅ Clear analysis of which schedulers work best when
3. ✅ At least one custom scheduler implemented and tested
4. ✅ GNN model trained with >70% accuracy on scheduler selection
5. ✅ Publication-ready figures and tables
6. ✅ Comprehensive final report

---

## Notes for Claude Code

- Commit after each major task
- Run tests frequently
- Save intermediate results
- Use error handling for long-running experiments
- Create checkpoints for GNN training
- Document any issues or deviations from plan
