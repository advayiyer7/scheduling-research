# Progress Log

## January 2026

### Day 1 - Project Setup ✅
- Created conda environment `scheduling-research` with Python 3.11
- Cloned and installed SAGA framework v2.0.2
- Installed dependencies: pydantic, networkx, numpy, matplotlib
- Verified SAGA installation - all 23 schedulers available
- Created initial project structure and documentation

### Day 2 - Exploration (In Progress)
- [ ] Run HEFT example: `python scripts/run_heft_example.py`
- [ ] Compare schedulers: `python scripts/compare_schedulers.py`
- [ ] Start reading HEFT paper
- [ ] Begin code annotations

---

## Next Actions

### Immediate (Today)
1. Run `python scripts/run_heft_example.py`
2. Run `python scripts/compare_schedulers.py`
3. Open `saga/src/saga/schedulers/heft.py` in VS Code
4. Start annotating (follow `docs/heft_study_guide.md`)

### This Week
1. Finish HEFT annotations
2. Read HEFT/CPoP paper sections 3-4
3. Annotate CPoP implementation
4. Run experiments in Jupyter notebook

### Next Week
1. Survey other schedulers (MinMin, MaxMin, etc.)
2. Start designing custom scheduler
3. Read GCN scheduler paper

---

## Reading Progress

| Paper | Status | Notes |
|-------|--------|-------|
| HEFT/CPoP (Topcuoglu 2002) | Not Started | Priority #1 |
| SAGA/PISA (arXiv:2403.07120) | Not Started | Framework overview |
| Parametric Scheduler | Not Started | |
| GCN Scheduler | Not Started | For later |

---

## Code Understanding

### HEFT Algorithm
- [ ] Understand upward rank calculation
- [ ] Understand EFT calculation
- [ ] Understand processor selection
- [ ] Document data structures used

### SAGA Framework
- [x] TaskGraph creation
- [x] Network creation
- [x] Running schedulers
- [ ] Schedule visualization
- [ ] Problem generation (PISA)

---


## Experiment Ideas

1. **Communication ratio impact**: How does CCR (communication-to-computation ratio) affect scheduler performance?

2. **Scalability**: How do schedulers scale with number of tasks? Processors?

3. **Graph structure**: Do certain schedulers work better on specific DAG shapes (chains, forks, diamonds)?

4. **Heterogeneity**: Impact of processor speed variation on scheduler choice?