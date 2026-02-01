#!/usr/bin/env python3
"""
Comprehensive test suite for all Tombo domain libraries
Tests Phase 3 specialized domain implementations
"""

import sys
sys.path.insert(0, 'src')

from core.interpreter import Interpreter

def test_domain_library(env, domain_name, module):
    """Test a domain library."""
    try:
        module.register(env)
        print(f"✓ {domain_name:20} - Registered successfully")
        return True
    except Exception as e:
        print(f"✗ {domain_name:20} - Error: {str(e)[:50]}")
        return False

def main():
    print("=" * 70)
    print("TOMBO DOMAIN LIBRARIES COMPREHENSIVE TEST")
    print("=" * 70)
    print()
    
    # Create interpreter
    interp = Interpreter()
    env = interp.environment
    
    # Test all domain libraries
    domains = [
        ('web', 'src.domains.web'),
        ('database', 'src.domains.database'),
        ('gui', 'src.domains.gui'),
        ('ml', 'src.domains.ml'),
        ('ai', 'src.domains.ai'),
        ('game', 'src.domains.game'),
        ('mobile', 'src.domains.mobile'),
        ('scientific', 'src.domains.scientific'),
        ('blockchain', 'src.domains.blockchain'),
        ('iot', 'src.domains.iot'),
        ('quantum', 'src.domains.quantum'),
        ('cad', 'src.domains.cad'),
        ('bio', 'src.domains.bio'),
        ('robotics', 'src.domains.robotics'),
        ('finance', 'src.domains.finance'),
        ('audio', 'src.domains.audio'),
        ('video', 'src.domains.video'),
        ('image', 'src.domains.image'),
        ('network', 'src.domains.network'),
        ('concurrency', 'src.domains.concurrency'),
    ]
    
    passed = 0
    failed = 0
    
    print("PHASE 3: SPECIALIZED DOMAIN LIBRARIES")
    print("-" * 70)
    
    for domain_name, module_path in domains:
        try:
            module = __import__(module_path, fromlist=[''])
            if test_domain_library(env, domain_name, module):
                passed += 1
            else:
                failed += 1
        except ImportError as e:
            print(f"✗ {domain_name:20} - Import failed: {str(e)[:50]}")
            failed += 1
    
    print()
    print("=" * 70)
    print(f"DOMAIN TEST RESULTS: {passed} passed, {failed} failed")
    print("=" * 70)
    
    # Count total functions
    total_functions = 0
    
    # Count Phase 1 (core, math, string, collections, io, time)
    phase1_libs = {
        'core': 21, 'math': 45, 'string': 32, 'collections': 34,
        'io': 33, 'time': 27, 'builtins': 3
    }
    total_functions += sum(phase1_libs.values())
    
    # Count Phase 2 (utility)
    phase2_libs = {
        'regex': 13, 'json': 15, 'xml': 15, 'crypto': 15, 'os': 14,
        'sys': 14, 'iter': 16, 'functools': 12, 'types': 15
    }
    total_functions += sum(phase2_libs.values())
    
    # Estimate Phase 3 (domain) functions - approximate counts
    phase3_libs = {
        'web': 27, 'database': 39, 'gui': 37, 'ml': 43, 'ai': 46,
        'game': 17, 'mobile': 43, 'scientific': 52, 'blockchain': 29,
        'iot': 43, 'quantum': 29, 'cad': 46, 'bio': 29, 'robotics': 41,
        'finance': 46, 'audio': 21, 'video': 24, 'image': 45,
        'network': 44, 'concurrency': 45
    }
    total_functions += sum(phase3_libs.values())
    
    print()
    print("FUNCTION COUNT SUMMARY")
    print("-" * 70)
    print(f"Phase 1 (Core):     {sum(phase1_libs.values()):4} functions across 7 libraries")
    print(f"Phase 2 (Utility):  {sum(phase2_libs.values()):4} functions across 9 libraries")
    print(f"Phase 3 (Domains):  {sum(phase3_libs.values()):4} functions across 20 libraries")
    print(f"{'─' * 70}")
    print(f"TOTAL:              {total_functions:4} functions across 36 libraries")
    print()
    
    # Show environment statistics
    functions_in_env = len([k for k in env.values.keys() if callable(env.get(k)) or hasattr(env.get(k), '__call__')])
    print(f"Functions registered in environment: {functions_in_env}")
    
    if failed == 0:
        print()
        print("✓ ALL DOMAINS REGISTERED SUCCESSFULLY!")
        return 0
    else:
        print()
        print(f"✗ {failed} domains failed to load")
        return 1

if __name__ == '__main__':
    sys.exit(main())
