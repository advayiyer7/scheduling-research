"""
Scheduler Benchmarking Script

Compare multiple schedulers on the same task graphs.
Usage: python scripts/benchmark.py
"""

import time
from typing import Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class BenchmarkResult:
    """Results from running a scheduler on a problem instance."""
    scheduler_name: str
    makespan: float
    runtime_seconds: float
    task_graph_name: str
    network_name: str


def benchmark_scheduler(scheduler, network, task_graph, name: str) -> BenchmarkResult:
    """Run a single scheduler and measure performance."""
    start = time.perf_counter()
    schedule = scheduler.schedule(network, task_graph)
    runtime = time.perf_counter() - start
    
    # Get makespan from schedule
    makespan = getattr(schedule, 'makespan', -1)
    
    return BenchmarkResult(
        scheduler_name=name,
        makespan=makespan,
        runtime_seconds=runtime,
        task_graph_name=getattr(task_graph, 'name', 'unknown'),
        network_name=getattr(network, 'name', 'unknown')
    )


def run_benchmark():
    """Run benchmark comparing SAGA schedulers."""
    try:
        from saga.schedulers import HeftScheduler, CpopScheduler
        from saga.data import TaskGraph, Network
    except ImportError:
        print("Install SAGA first: cd saga && pip install -e .")
        return
    
    print("=== Scheduler Benchmark ===\n")
    
    # Define schedulers to compare
    schedulers = [
        ('HEFT', HeftScheduler()),
        ('CPoP', CpopScheduler()),
    ]
    
    # TODO: Load or generate task graphs
    # You can use SAGA's problem generators or create your own
    
    print("To run actual benchmarks:")
    print("1. Generate task graphs using PISA or SAGA utilities")
    print("2. Load benchmark networks")
    print("3. Iterate through (scheduler, problem) pairs")
    print("\nSee saga/scripts/examples/ for reference implementations")


def compare_results(results: List[BenchmarkResult]):
    """Print comparison table of results."""
    print("\n=== Results ===")
    print(f"{'Scheduler':<20} {'Makespan':<12} {'Runtime (s)':<12}")
    print("-" * 44)
    
    for r in sorted(results, key=lambda x: x.makespan):
        print(f"{r.scheduler_name:<20} {r.makespan:<12.2f} {r.runtime_seconds:<12.4f}")


if __name__ == "__main__":
    run_benchmark()