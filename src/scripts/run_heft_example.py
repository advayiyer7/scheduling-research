"""
Basic HEFT Example

This script demonstrates running HEFT on a simple task graph.
Run: python scripts/run_heft_example.py
"""

import networkx as nx
from saga.schedulers import HeftScheduler
from saga.data import TaskGraph, Network, Task, Data, Processor, Link


def create_diamond_task_graph():
    """
    Create a diamond-shaped task graph:
    
        T0 (entry)
       /  \
      T1   T2
       \  /
        T3 (exit)
    
    This is a classic example from scheduling literature.
    """
    task_graph = TaskGraph()
    
    # Define computation costs: {processor_name: execution_time}
    # Different processors have different speeds
    task_graph.add_task(Task(name="T0", comp_costs={"P0": 14, "P1": 16, "P2": 9}))
    task_graph.add_task(Task(name="T1", comp_costs={"P0": 13, "P1": 19, "P2": 18}))
    task_graph.add_task(Task(name="T2", comp_costs={"P0": 11, "P1": 13, "P2": 19}))
    task_graph.add_task(Task(name="T3", comp_costs={"P0": 13, "P1": 8, "P2": 17}))
    
    # Define data dependencies (edges)
    # Data(name, size) - size affects communication cost
    task_graph.add_data(Data(name="D0_1", size=18), "T0", "T1")
    task_graph.add_data(Data(name="D0_2", size=12), "T0", "T2")
    task_graph.add_data(Data(name="D1_3", size=9), "T1", "T3")
    task_graph.add_data(Data(name="D2_3", size=15), "T2", "T3")
    
    return task_graph


def create_simple_network():
    """
    Create a 3-processor network.
    
    P0 --- P1
     \    /
      \  /
       P2
    
    All links have the same bandwidth for simplicity.
    """
    network = Network()
    
    # Add processors (compute nodes)
    network.add_processor(Processor(name="P0", speed=1.0))
    network.add_processor(Processor(name="P1", speed=1.0))
    network.add_processor(Processor(name="P2", speed=1.0))
    
    # Add links (communication channels)
    # Link bandwidth determines communication time = data_size / bandwidth
    network.add_link(Link(name="L01", source="P0", dest="P1", bandwidth=1.0))
    network.add_link(Link(name="L10", source="P1", dest="P0", bandwidth=1.0))
    network.add_link(Link(name="L02", source="P0", dest="P2", bandwidth=1.0))
    network.add_link(Link(name="L20", source="P2", dest="P0", bandwidth=1.0))
    network.add_link(Link(name="L12", source="P1", dest="P2", bandwidth=1.0))
    network.add_link(Link(name="L21", source="P2", dest="P1", bandwidth=1.0))
    
    return network


def print_task_graph_info(task_graph):
    """Print task graph details."""
    print("\n=== Task Graph ===")
    print(f"Tasks: {[t.name for t in task_graph.tasks]}")
    print(f"Dependencies: {len(list(task_graph.data))} edges")
    print("\nComputation costs:")
    for task in task_graph.tasks:
        print(f"  {task.name}: {task.comp_costs}")


def print_schedule(schedule):
    """Print schedule details."""
    print("\n=== Schedule ===")
    print(f"Makespan: {schedule.makespan:.2f}")
    print("\nTask assignments:")
    for task_name, processor_name in schedule.task_to_processor.items():
        start = schedule.task_to_start_time.get(task_name, 0)
        end = schedule.task_to_end_time.get(task_name, 0)
        print(f"  {task_name} -> {processor_name} (start: {start:.1f}, end: {end:.1f})")


def main():
    print("=" * 50)
    print("HEFT Scheduling Example")
    print("=" * 50)
    
    # Create problem instance
    print("\n[1] Creating task graph...")
    task_graph = create_diamond_task_graph()
    print_task_graph_info(task_graph)
    
    print("\n[2] Creating network...")
    network = create_simple_network()
    print(f"Processors: {[p.name for p in network.processors]}")
    
    # Run HEFT
    print("\n[3] Running HEFT scheduler...")
    scheduler = HeftScheduler()
    schedule = scheduler.schedule(network, task_graph)
    
    # Print results
    print_schedule(schedule)
    
    print("\n" + "=" * 50)
    print("Done! Try modifying task costs or network to see how schedule changes.")
    print("=" * 50)


if __name__ == "__main__":
    main()