"""Quick Phase 8 import and smoke tests"""
import sys
sys.path.insert(0, 'src')

print('Validating Phase 8 libraries...')

try:
    from lib.mapreduce import MapReduce
    print('✓ MapReduce imported')
except Exception as e:
    print('✗ MapReduce import failed:', e)

try:
    from lib.aggregations import mean, median, group_by
    print('✓ Aggregations imported')
except Exception as e:
    print('✗ Aggregations import failed:', e)

try:
    from lib.analytics import describe, moving_average
    print('✓ Analytics imported')
except Exception as e:
    print('✗ Analytics import failed:', e)

try:
    from lib.pipelines import DataPipeline
    print('✓ Pipelines imported')
except Exception as e:
    print('✗ Pipelines import failed:', e)

try:
    from lib.datalake import DataLake
    print('✓ DataLake imported')
except Exception as e:
    print('✗ DataLake import failed:', e)

try:
    from lib.query import Query
    print('✓ Query imported')
except Exception as e:
    print('✗ Query import failed:', e)

print('\nPhase 8 skeletons created. Run full Phase 8 tests next.')
