# Scheduling Algorithms Research

Research project exploring scheduling algorithms for distributed computing systems, with focus on HEFT-based scheduling theory and deep learning/GNN approaches for algorithm recommendation.

## Project Goals

1. **Understand HEFT and CPoP** - Study classic scheduling heuristics and reconcile paper descriptions with SAGA implementations
2. **Explore Scheduling Landscape** - Review various scheduling algorithms (brute-force, SMT-based, heuristics)
3. **Implement GNN-based Scheduling** - Build neural network models to predict optimal schedulers
4. **Design Novel Algorithms** - Extend SAGA with new scheduling approaches

## Setup

### Prerequisites
- Python 3.11+
- Conda (recommended)
- Git

### Installation

```bash
# Create and activate environment
conda create -n scheduling-research python=3.11
conda activate scheduling-research

# Install Graphviz for visualization
conda install -c conda-forge graphviz python-graphviz

# Clone and install SAGA
git clone https://github.com/ANRGUSC/saga.git
cd saga
pip install -e .
cd ..

# Install additional dependencies
pip install -r requirements.txt
```

## Project Structure

```
scheduling-research/
├── src/                    # Custom scheduler implementations
│   ├── schedulers/         # New scheduling algorithms
│   └── models/             # GNN/ML models for scheduler prediction
├── notebooks/              # Jupyter notebooks for exploration
├── experiments/            # Experiment scripts and results
├── data/                   # Task graphs, networks, benchmark data
├── docs/                   # Notes, paper summaries
└── saga/                   # SAGA framework (submodule)
```

## Key Resources

### Papers
- [SAGA and PISA Paper](https://arxiv.org/pdf/2403.07120) - Framework introduction
- [HEFT/CPoP Paper](https://ieeexplore.ieee.org/document/765092) - Original scheduling algorithms
- [Parametric Scheduler](https://arxiv.org/pdf/2403.07112) - Parametric approach
- [GCN Scheduler](https://anrg.usc.edu/www/papers/Mehrdad_GCNScheduler_GNNet.pdf) - Graph neural network approach

### Code
- [SAGA Repository](https://github.com/ANRGUSC/saga)
- Key directories in SAGA:
  - `saga/src/saga/schedulers/` - Scheduler implementations
  - `tests/test_schedulers.py` - Test suite

## Research Tasks

### Phase 1: Setup & Exploration
- [ ] Set up SAGA framework and run example scripts
- [ ] Read SAGA/PISA paper
- [ ] Familiarize with codebase structure

### Phase 2: Understand HEFT/CPoP
- [ ] Read original HEFT/CPoP paper
- [ ] Review `saga/src/saga/schedulers/heft.py` and `cpop.py`
- [ ] Add detailed comments mapping algorithm to implementation

### Phase 3: Explore Additional Schedulers
- [ ] Survey other schedulers in SAGA
- [ ] Document differences and tradeoffs

### Phase 4: Extend the System
- [ ] Design or implement a new scheduling algorithm
- [ ] Ensure compatibility with SAGA framework
- [ ] Pass `tests/test_schedulers.py`

## Author

Advay - USC Computer Science
