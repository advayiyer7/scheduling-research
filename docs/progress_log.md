# Progress Log

## January 2026

### Day 1 - Project Setup
- Created conda environment `scheduling-research` with Python 3.11
- Cloned and installed SAGA framework v2.0.2
- Installed dependencies: pydantic, networkx, numpy, matplotlib
- Verified SAGA installation - all 23 schedulers available

**Schedulers discovered:**
- Classic heuristics: HEFT, CPoP, FCP, DPS, ETF
- List scheduling: MinMin, MaxMin, MCT, MET, OLB, Sufferage
- Other: BruteForce, SMT (optimal but slow), Hybrid

**Next steps:**
1. Run basic SAGA examples
2. Read HEFT/CPoP paper
3. Start annotating heft.py

---

## Notes

### HEFT Algorithm Overview
- Two phases: task prioritization + processor selection
- Uses "upward rank" for priority
- Selects processor with Earliest Finish Time (EFT)
- O(n²p) complexity where n=tasks, p=processors

### Questions to Answer
- How does SAGA represent task graphs?
- How does SAGA represent networks?
- What's the difference between HEFT and CPoP?
- Which schedulers are optimal vs heuristic?