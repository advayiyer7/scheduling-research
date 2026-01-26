"""
SAGA Framework Exploration Script

Run this after installing SAGA to understand the framework.
Usage: python scripts/explore_saga.py
"""

import sys

def check_saga_installation():
    """Verify SAGA is installed correctly."""
    try:
        import saga
        print("✓ SAGA imported successfully")
        return True
    except ImportError:
        print("✗ SAGA not found. Install with:")
        print("  git clone https://github.com/ANRGUSC/saga.git")
        print("  cd saga && pip install -e .")
        return False


def explore_schedulers():
    """List available schedulers in SAGA."""
    from saga import schedulers
    
    print("\n=== Available Schedulers ===")
    scheduler_classes = [
        name for name in dir(schedulers) 
        if name.endswith('Scheduler') and not name.startswith('_')
    ]
    
    for name in sorted(scheduler_classes):
        cls = getattr(schedulers, name)
        doc = cls.__doc__.split('\n')[0] if cls.__doc__ else "No description"
        print(f"  • {name}: {doc}")
    
    return scheduler_classes


def create_simple_task_graph():
    """Create a diamond-shaped task graph for testing."""
    import networkx as nx
    
    # Diamond: entry -> (A, B) -> exit
    #     0
    #    / \
    #   1   2
    #    \ /
    #     3
    
    G = nx.DiGraph()
    
    # Add nodes with computation costs
    # costs[processor] = time to execute on that processor
    G.add_node(0, cost={'p0': 10, 'p1': 12, 'p2': 8})   # Entry
    G.add_node(1, cost={'p0': 8, 'p1': 10, 'p2': 12})   # Task A
    G.add_node(2, cost={'p0': 12, 'p1': 8, 'p2': 10})   # Task B  
    G.add_node(3, cost={'p0': 6, 'p1': 8, 'p2': 10})    # Exit
    
    # Add edges with communication costs
    G.add_edge(0, 1, weight=2)  # 0 -> 1
    G.add_edge(0, 2, weight=3)  # 0 -> 2
    G.add_edge(1, 3, weight=2)  # 1 -> 3
    G.add_edge(2, 3, weight=2)  # 2 -> 3
    
    print("\n=== Task Graph (Diamond) ===")
    print(f"  Nodes: {list(G.nodes())}")
    print(f"  Edges: {list(G.edges())}")
    
    return G


def create_simple_network():
    """Create a simple 3-processor network."""
    import networkx as nx
    
    # Fully connected network of 3 processors
    N = nx.complete_graph(3)
    N = nx.DiGraph(N)  # Convert to directed for SAGA
    
    # Rename nodes
    mapping = {0: 'p0', 1: 'p1', 2: 'p2'}
    N = nx.relabel_nodes(N, mapping)
    
    # Add bandwidth on edges (communication rate)
    for u, v in N.edges():
        N[u][v]['weight'] = 1.0  # Unit bandwidth
    
    print("\n=== Network (3 Processors) ===")
    print(f"  Processors: {list(N.nodes())}")
    print(f"  Links: {N.number_of_edges()}")
    
    return N


def run_heft_example():
    """Run HEFT on a simple example."""
    from saga.schedulers import HeftScheduler
    from saga.data import TaskGraph, Network
    
    print("\n=== Running HEFT Scheduler ===")
    
    # Note: SAGA has its own TaskGraph and Network classes
    # This is a simplified example - check SAGA docs for exact API
    
    try:
        # Try to run one of SAGA's built-in examples
        import subprocess
        result = subprocess.run(
            ['python', '-c', '''
from saga.schedulers import HeftScheduler
print("HEFT Scheduler loaded successfully!")
print(f"HEFT docstring: {HeftScheduler.__doc__[:200]}...")
'''],
            capture_output=True, text=True
        )
        print(result.stdout)
        if result.stderr:
            print(f"Note: {result.stderr}")
    except Exception as e:
        print(f"Could not run HEFT example: {e}")
        print("Try running SAGA's examples directly:")
        print("  python saga/scripts/examples/basic_usage/main.py")


def main():
    print("=" * 50)
    print("SAGA Framework Exploration")
    print("=" * 50)
    
    if not check_saga_installation():
        sys.exit(1)
    
    explore_schedulers()
    create_simple_task_graph()
    create_simple_network()
    run_heft_example()
    
    print("\n=== Next Steps ===")
    print("1. Run SAGA examples: python saga/scripts/examples/basic_usage/main.py")
    print("2. Run tests: pytest saga/tests -k 'HeftScheduler' --timeout=60")
    print("3. Read HEFT code: saga/src/saga/schedulers/heft.py")
    print("4. Read the papers in docs/reading_list.md")


if __name__ == "__main__":
    main()