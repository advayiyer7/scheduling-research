# Project Summary

## Overview

**Project**: Scheduling Algorithms Research for Distributed Computing  
**Advisor**: Professor Bhaskar Krishnamachari, USC ANRG  
**Student**: Advay  
**Started**: January 2026

---

## What We Built

### Environment Setup ✅
- Conda environment `scheduling-research` with Python 3.11
- SAGA framework v2.0.2 installed and working
- All 23 schedulers available and tested
- Dependencies: pydantic, networkx, numpy, matplotlib, torch

### Project Structure
```
scheduling-research/
├── docs/                    # Documentation and annotations
│   ├── heft_annotations.md
│   ├── heft_code_annotations.md
│   ├── heft_study_guide.md
│   ├── progress_log.md
│   ├── reading_list.md
│   └── schedulers_overview.md
├── notebooks/               # Jupyter experiments
│   ├── 01_saga_exploration.ipynb
│   └── 02_scheduler_experiments.ipynb
├── scripts/                 # Runnable scripts
│   ├── benchmark.py
│   ├── compare_schedulers.py
│   ├── explore_saga.py
│   ├── run_heft_example.py
│   └── verify_setup.py
├── src/                     # Custom implementations
│   ├── models/              # GNN models (TODO)
│   └── schedulers/          # Custom schedulers (TODO)
├── saga/                    # SAGA framework (cloned)
├── CHEATSHEET.md
├── NOTES.md
├── README.md
├── TODO.md
├── requirements.txt
└── setup.sh
```

---

## Available Schedulers (23 Total)

| Category | Schedulers |
|----------|------------|
| Classic Heuristics | HEFT, CPoP, FCP, DPS, ETF, FLB, GDL, Hbmct, Msbc, WBA, BIL, Duplex, FastestNode, MST |
| List-Based | MinMin, MaxMin, MCT, MET, OLB, Sufferage |
| Optimal | BruteForce, SMT |
| Hybrid | Hybrid |

---

## Scripts Ready to Run

| Script | Purpose | Command |
|--------|---------|---------|
| `verify_setup.py` | Check SAGA installation | `python scripts/verify_setup.py` |
| `explore_saga.py` | List all schedulers | `python scripts/explore_saga.py` |
| `run_heft_example.py` | Run HEFT on sample graph | `python scripts/run_heft_example.py` |
| `compare_schedulers.py` | Compare 6 schedulers | `python scripts/compare_schedulers.py` |

---

## Key Resources

### Papers to Read
1. **HEFT/CPoP** - Topcuoglu et al., IEEE TPDS 2002
2. **SAGA/PISA** - arXiv:2403.07120
3. **Parametric Scheduler** - arXiv:2403.07112
4. **GCN Scheduler** - ANRG paper

### Code to Study
- `saga/src/saga/schedulers/heft.py` - HEFT implementation
- `saga/src/saga/schedulers/cpop.py` - CPoP implementation
- `saga/src/saga/data/` - TaskGraph, Network data structures

---

## What's Next

### Immediate Tasks
1. Run example scripts to see schedulers in action
2. Annotate HEFT implementation (map code to paper)
3. Annotate CPoP implementation

### Research Tasks
1. Benchmark all 23 schedulers on standard problems
2. Analyze which schedulers work best for which graph types
3. Implement GNN-based scheduler predictor
4. Generate results and visualizations

---

## GitHub

Repository is set up and ready for commits.

```bash
git add .
git commit -m "message"
git push origin main
```
