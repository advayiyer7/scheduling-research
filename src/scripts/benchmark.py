"""
Scheduler Benchmarking

Usage: python scripts/benchmark.py
"""

import time
from typing import List, Tuple


def benchmark_scheduler(scheduler, network, task_graph, name: str) -> dict:
    """Run scheduler and measure performance."""
    start = time.perf_counter()
    schedule = scheduler.schedule(network, task_graph)
    runtime = time.perf_counter() - start
    
    makespan = getattr(schedule, 'makespan', -1)
    
    return {
        'name': name,
        'makespan': makespan,
        'runtime': runtime
    }


def run_benchmark():
    """Run benchmark comparing schedulers."""
    try:
        from saga.schedulers import HeftScheduler, CpopScheduler
        print("[OK] SAGA schedulers loaded")
    except ImportError:
        print("[X] Install SAGA first: cd saga && pip install -e .")
        return
    
    print("\n=== Scheduler Benchmark ===")
    
    schedulers = [
        ('HEFT', HeftScheduler()),
        ('CPoP', CpopScheduler()),
    ]
    
    print(f"Loaded {len(schedulers)} schedulers")
    print("\nTo run full benchmarks:")
    print("  1. Generate task graphs with PISA")
    print("  2. Create network topologies")
    print("  3. Run each scheduler and compare makespan")
    print("\nSee: saga/scripts/examples/")


def main():
    print("=" * 40)
    print("Scheduler Benchmark")
    print("=" * 40)
    run_benchmark()


if __name__ == "__main__":
    main()