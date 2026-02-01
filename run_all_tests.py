#!/usr/bin/env python
"""
Tombo Language - Complete Test Suite Guide
Run all verification tests to ensure system readiness
"""

import subprocess
import sys
from pathlib import Path

def run_test(name, script_path):
    """Run a test script and return results"""
    print(f"\n{'='*70}")
    print(f"Running: {name}")
    print(f"Script: {script_path}")
    print(f"{'='*70}\n")
    
    try:
        result = subprocess.run(
            [sys.executable, script_path],
            cwd=Path(__file__).parent,
            capture_output=False
        )
        return result.returncode == 0
    except Exception as e:
        print(f"Error running test: {e}")
        return False

def main():
    print("\n" + "="*70)
    print("TOMBO LANGUAGE - COMPLETE TEST SUITE")
    print("="*70)
    
    tests = [
        ("Library Verification", "tools/verify_implementation.py"),
        ("Build & Test Report", "tools/build_test_report.py"),
        ("Hardware Integration Test", "tools/hardware_integration_test.py"),
    ]
    
    results = {}
    
    for test_name, script in tests:
        results[test_name] = run_test(test_name, script)
    
    print("\n" + "="*70)
    print("TEST SUITE RESULTS")
    print("="*70)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, passed_test in results.items():
        status = "✅ PASSED" if passed_test else "❌ FAILED"
        print(f"{test_name:.<45} {status}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✅✅✅ ALL TESTS PASSED - SYSTEM READY FOR PUBLISHING ✅✅✅\n")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed - Please review errors above\n")
        return 1

if __name__ == '__main__':
    sys.exit(main())
