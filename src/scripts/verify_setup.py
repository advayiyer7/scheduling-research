"""
Verify SAGA Setup

Run: python scripts/verify_setup.py
"""

def main():
    print("=" * 50)
    print("SAGA Setup Verification")
    print("=" * 50)
    
    errors = []
    
    # Test 1: Import SAGA
    print("\n[1] Importing SAGA...", end=" ")
    try:
        import saga
        print("OK")
    except ImportError as e:
        print(f"FAILED: {e}")
        errors.append("SAGA import")
    
    # Test 2: Import schedulers
    print("[2] Importing schedulers...", end=" ")
    try:
        from saga.schedulers import HeftScheduler, CpopScheduler
        print("OK")
    except ImportError as e:
        print(f"FAILED: {e}")
        errors.append("Schedulers import")
    
    # Test 3: Import data classes
    print("[3] Importing data classes...", end=" ")
    try:
        from saga.data import TaskGraph, Network
        print("OK")
    except ImportError as e:
        print(f"FAILED: {e}")
        errors.append("Data classes import")
    
    # Test 4: Count schedulers
    print("[4] Counting schedulers...", end=" ")
    try:
        from saga import schedulers
        names = [n for n in dir(schedulers) if n.endswith('Scheduler') and not n.startswith('_')]
        print(f"OK ({len(names)} found)")
    except Exception as e:
        print(f"FAILED: {e}")
        errors.append("Scheduler count")
    
    # Test 5: Create scheduler instance
    print("[5] Creating HEFT instance...", end=" ")
    try:
        heft = HeftScheduler()
        print("OK")
    except Exception as e:
        print(f"FAILED: {e}")
        errors.append("HEFT instantiation")
    
    # Summary
    print("\n" + "=" * 50)
    if errors:
        print(f"FAILED: {len(errors)} error(s)")
        for e in errors:
            print(f"  - {e}")
    else:
        print("ALL TESTS PASSED")
        print("\nYou're ready to start!")
        print("Next: python saga/scripts/examples/basic_usage/main.py")
    print("=" * 50)


if __name__ == "__main__":
    main()