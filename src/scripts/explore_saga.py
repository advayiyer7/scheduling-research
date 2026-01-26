"""
SAGA Framework Exploration

Usage: python scripts/explore_saga.py
"""

import sys


def check_saga():
    """Check if SAGA is installed."""
    try:
        import saga
        print("[OK] SAGA imported successfully")
        return True
    except ImportError:
        print("[X] SAGA not found")
        print("    Run: git clone https://github.com/ANRGUSC/saga.git")
        print("    Then: cd saga && pip install -e .")
        return False


def list_schedulers():
    """List available SAGA schedulers."""
    try:
        from saga import schedulers
        print("\n=== Available Schedulers ===")
        
        names = [n for n in dir(schedulers) if n.endswith('Scheduler') and not n.startswith('_')]
        for name in sorted(names):
            print(f"  - {name}")
        
        return names
    except Exception as e:
        print(f"Error listing schedulers: {e}")
        return []


def run_simple_example():
    """Run a simple HEFT example."""
    try:
        from saga.schedulers import HeftScheduler
        print("\n=== HEFT Scheduler ===")
        print(f"Loaded: {HeftScheduler}")
        print("Ready to use!")
    except Exception as e:
        print(f"Could not load HEFT: {e}")


def main():
    print("=" * 40)
    print("SAGA Framework Exploration")
    print("=" * 40)
    
    if not check_saga():
        sys.exit(1)
    
    list_schedulers()
    run_simple_example()
    
    print("\n=== Next Steps ===")
    print("1. Run examples: python saga/scripts/examples/basic_usage/main.py")
    print("2. Run tests: pytest saga/tests -k HeftScheduler --timeout=60")
    print("3. Read code: saga/src/saga/schedulers/heft.py")


if __name__ == "__main__":
    main()