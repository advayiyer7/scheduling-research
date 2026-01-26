# Scheduling Algorithms Research

Research project exploring scheduling algorithms for distributed computing systems under Professor Bhaskar Krishnamachari at USC ANRG.

## Project Goals

- Understand HEFT and CPoP scheduling heuristics
- Explore the SAGA framework for task graph scheduling
- Implement GNN-based scheduler prediction models
- Design and benchmark novel scheduling algorithms

## Setup

```bash
bash setup.sh
```

## Quick Start

```bash
# After setup, explore SAGA
conda activate scheduling-research
python scripts/explore_saga.py

# Run SAGA tests
pytest saga/tests -k "HeftScheduler" --timeout=60

# Run benchmarks
python scripts/benchmark.py
```

## Project Structure

```
├── src/
│   ├── schedulers/      # Custom scheduler implementations
│   └── models/          # GNN/ML models
├── scripts/             # Utility scripts
├── notebooks/           # Jupyter exploration
├── docs/                # Paper notes
└── saga/                # SAGA framework (cloned)
```

## Key Papers

| Paper | Link |
|-------|------|
| SAGA & PISA | [arXiv:2403.07120](https://arxiv.org/pdf/2403.07120) |
| HEFT/CPoP | [IEEE](https://ieeexplore.ieee.org/document/765092) |
| Parametric Scheduler | [arXiv:2403.07112](https://arxiv.org/pdf/2403.07112) |
| GCN Scheduler | [ANRG](https://anrg.usc.edu/www/papers/Mehrdad_GCNScheduler_GNNet.pdf) |

## Progress

- [ ] Set up SAGA framework
- [ ] Annotate HEFT/CPoP implementations  
- [ ] Survey additional schedulers
- [ ] Implement custom scheduler
- [ ] Build GNN prediction model