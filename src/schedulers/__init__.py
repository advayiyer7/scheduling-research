"""
Custom Scheduling Algorithms

Usage:
    from src.schedulers import RandomScheduler, GreedyLoadBalancer
"""

import random
import networkx as nx
from typing import Dict, Any, Optional

# Check if SAGA is available
try:
    from saga.schedulers import Scheduler
    SAGA_AVAILABLE = True
except ImportError:
    SAGA_AVAILABLE = False
    Scheduler = object


class RandomScheduler:
    """Baseline: Random task-to-processor assignment."""
    
    def __init__(self, seed: Optional[int] = None):
        self.seed = seed
    
    def schedule(self, network, task_graph) -> Dict[Any, Any]:
        if self.seed is not None:
            random.seed(self.seed)
        
        processors = list(network.nodes())
        topo_order = list(nx.topological_sort(task_graph))
        
        assignments = {}
        for task in topo_order:
            assignments[task] = random.choice(processors)
        
        return assignments


class GreedyLoadBalancer:
    """Assign each task to least-loaded processor."""
    
    def schedule(self, network, task_graph) -> Dict[Any, Any]:
        processors = list(network.nodes())
        topo_order = list(nx.topological_sort(task_graph))
        
        processor_load = {p: 0.0 for p in processors}
        assignments = {}
        
        for task in topo_order:
            # Get task cost
            cost = task_graph.nodes[task].get('cost', 1.0)
            if isinstance(cost, dict):
                cost = sum(cost.values()) / len(cost) if cost else 1.0
            
            # Assign to least loaded
            min_proc = min(processors, key=lambda p: processor_load[p])
            assignments[task] = min_proc
            processor_load[min_proc] += float(cost)
        
        return assignments


class MyCustomScheduler:
    """TODO: Implement your own scheduler."""
    
    def __init__(self, **params):
        self.params = params
    
    def schedule(self, network, task_graph):
        raise NotImplementedError("Implement your scheduler!")