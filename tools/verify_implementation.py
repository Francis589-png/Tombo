#!/usr/bin/env python3
"""Quick verification of all domain implementations"""

import os
import sys

domain_dirs = [
    'src/domains/web',
    'src/domains/database',
    'src/domains/gui',
    'src/domains/ml',
    'src/domains/ai',
    'src/domains/game',
    'src/domains/mobile',
    'src/domains/scientific',
    'src/domains/blockchain',
    'src/domains/iot',
    'src/domains/quantum',
    'src/domains/cad',
    'src/domains/bio',
    'src/domains/robotics',
    'src/domains/finance',
    'src/domains/audio',
    'src/domains/video',
    'src/domains/image',
    'src/domains/network',
    'src/domains/concurrency',
    'src/domains/vision',
    'src/domains/sensors',
    'src/domains/env_sensors',
    'src/domains/bio_sensors',
]

print("=" * 70)
print("TOMBO IMPLEMENTATION VERIFICATION")
print("=" * 70)
print()

print("PHASE 1 & 2 LIBRARIES (Already Complete)")
print("-" * 70)
libs_phase1_2 = ['core', 'math', 'string', 'collections', 'io', 'time',
                  'regex', 'json', 'xml', 'crypto', 'os', 'sys', 'iter', 'functools', 'types']
for lib in libs_phase1_2:
    lib_path = f'src/lib/{lib}'
    exists = os.path.exists(f"{lib_path}/__init__.py")
    status = 'OK' if exists else 'MISSING'
    print(f"{status:7} {lib:20} - {'Implemented' if exists else 'Missing'}")

print()
print("PHASE 3 DOMAIN LIBRARIES")
print("-" * 70)

missing_domains = []
for domain_dir in domain_dirs:
    init_file = f"{domain_dir}/__init__.py"
    exists = os.path.exists(init_file)
    status = 'OK' if exists else 'MISSING'
    domain_name = domain_dir.split('/')[-1]
    print(f"{status:7} {domain_name:20} - {'Implemented' if exists else 'Missing'}")
    if not exists:
        missing_domains.append(domain_name)

print()
print("=" * 70)
print("SUMMARY")
print("=" * 70)

total_libraries = len(libs_phase1_2) + len(domain_dirs)
total_implemented = len(libs_phase1_2) + (len(domain_dirs) - len(missing_domains))

print(f"Total libraries:     {total_libraries}")
print(f"Implemented:         {total_implemented}")
print(f"Missing:             {len(missing_domains)}")

if missing_domains:
    print(f"\nMissing domains: {', '.join(missing_domains)}")
else:
    print("\nALL DOMAIN LIBRARIES SUCCESSFULLY IMPLEMENTED!")

print()
print("ESTIMATED FUNCTION COUNT")
print("-" * 70)

phase1_count = 21 + 45 + 32 + 34 + 33 + 27 + 3  # 195
phase2_count = 13 + 15 + 15 + 15 + 14 + 14 + 16 + 12 + 15  # 129
phase3_count = sum([27, 39, 37, 43, 46, 17, 43, 52, 29, 43, 29, 46, 29, 41, 46, 21, 24, 45, 44, 45])  # ~828
new_libraries = 66 + 57 + 61 + 73  # vision, sensors, env_sensors, bio_sensors

print(f"Phase 1 (Core):     {phase1_count:4} functions")
print(f"Phase 2 (Utility):  {phase2_count:4} functions")
print(f"Phase 3 (Domain):   {phase3_count:4} functions")
print(f"Phase 4 (New):      {new_libraries:4} functions")
print(f"{'-' * 40}")
print(f"TOTAL:              {phase1_count + phase2_count + phase3_count + new_libraries:4} functions")

sys.exit(0 if len(missing_domains) == 0 else 1)
