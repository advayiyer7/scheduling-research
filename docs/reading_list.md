# Reading List & Paper Notes

## Priority Papers (Start Here)

### 1. SAGA and PISA Framework
**Paper**: [arXiv:2403.07120](https://arxiv.org/pdf/2403.07120)
- **What**: Introduces SAGA framework and PISA adversarial problem generator
- **Why Read**: Foundation for all work - understand the codebase you'll be using
- **Key Concepts**:
  - Task graph representation
  - Network modeling
  - Scheduler interface
  - PISA: generates hard scheduling problems to benchmark algorithms

### 2. HEFT and CPoP (Original Algorithms)
**Paper**: [IEEE - Task Scheduling for Heterogeneous Processors](https://ieeexplore.ieee.org/document/765092)
- **What**: Heterogeneous Earliest Finish Time (HEFT) and Critical Path on Processor (CPoP)
- **Why Read**: Classic algorithms, your task is to annotate the implementations
- **Key Concepts**:
  - Upward rank (ranku) - priority calculation
  - Earliest Finish Time (EFT) processor selection
  - Critical path identification
  - Task prioritization heuristics

### 3. Parametric Scheduler
**Paper**: [arXiv:2403.07112](https://arxiv.org/pdf/2403.07112)
- **What**: Parameterized scheduling approach
- **Why Read**: Shows how to generalize scheduling decisions
- **Key Concepts**: TBD after reading

### 4. GCN Scheduler (Graph Neural Networks)
**Paper**: [GCNScheduler](https://anrg.usc.edu/www/papers/Mehrdad_GCNScheduler_GNNet.pdf)
- **What**: Using Graph Convolutional Networks for scheduling
- **Why Read**: Core to your GNN implementation goal
- **Key Concepts**:
  - Graph neural network architecture
  - Learning task graph representations
  - Scheduler prediction/recommendation

---

## Notes Template

### Paper: [Title]
**Citation**: 
**Date Read**: 

#### Summary (2-3 sentences)


#### Key Contributions


#### Algorithm/Method


#### Relevance to Project


#### Questions/Ideas

---

## HEFT Algorithm Notes

### Algorithm Overview (from paper)

1. **Compute ranku for all tasks** (upward rank)
   - ranku(exit_task) = w_exit (average computation cost)
   - ranku(task) = w_task + max(c_edge + ranku(successor)) for all successors
   
2. **Sort tasks by decreasing ranku** (priority list)

3. **For each task in priority order**:
   - For each processor:
     - Calculate Earliest Start Time (EST)
     - Calculate Earliest Finish Time (EFT) = EST + execution_cost
   - Assign task to processor with minimum EFT

### Code Location in SAGA
- `saga/src/saga/schedulers/heft.py`

### My Annotations
<!-- Add your line-by-line comments here after reviewing the code -->

