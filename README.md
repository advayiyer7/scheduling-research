# Scheduling Algorithms Research

Research project exploring scheduling algorithms for distributed computing systems under Professor Bhaskar Krishnamachari at USC ANRG.

## Setup Status: ✅ Complete

- [x] Conda environment created
- [x] SAGA framework installed (v2.0.2)
- [x] Dependencies installed

## Available Schedulers (23 total)

| Heuristic | List-Based | Other |
|-----------|------------|-------|
| HeftScheduler | MinMinScheduler | BruteForceScheduler |
| CpopScheduler | MaxMinScheduler | SMTScheduler |
| FCPScheduler | MCTScheduler | HybridScheduler |
| DPSScheduler | METScheduler | |
| ETFScheduler | OLBScheduler | |
| FLBScheduler | SufferageScheduler | |
| GDLScheduler | | |
| HbmctScheduler | | |
| MsbcScheduler | | |
| WBAScheduler | | |
| BILScheduler | | |
| DuplexScheduler | | |
| FastestNodeScheduler | | |
| MSTScheduler | | |

## Quick Start

```bash
conda activate scheduling-research
python scripts/explore_saga.py
python saga/scripts/examples/basic_usage/main.py
```

## Research Progress

- [x] Set up SAGA framework
- [ ] Read SAGA/PISA paper
- [ ] Read HEFT/CPoP paper  
- [ ] Annotate HEFT implementation
- [ ] Annotate CPoP implementation
- [ ] Survey additional schedulers
- [ ] Implement custom scheduler
- [ ] Build GNN prediction model

## Key Papers

| Paper | Link | Status |
|-------|------|--------|
| SAGA & PISA | [arXiv:2403.07120](https://arxiv.org/pdf/2403.07120) | To Read |
| HEFT/CPoP | [IEEE](https://ieeexplore.ieee.org/document/765092) | To Read |
| Parametric Scheduler | [arXiv:2403.07112](https://arxiv.org/pdf/2403.07112) | To Read |
| GCN Scheduler | [ANRG](https://anrg.usc.edu/www/papers/Mehrdad_GCNScheduler_GNNet.pdf) | To Read |

## Author

Advay - USC Computer Science  