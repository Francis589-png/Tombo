"""
Phase 8 Library Tests - MapReduce, Aggregations, Analytics, Pipelines, DataLake, Query
"""
import sys
import os
# Avoid importing the top-level `src` package which has side-effects.
# Insert the `src` directory on sys.path and import libraries directly from `lib`.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from lib.mapreduce import MapReduce
from lib.aggregations import mean, median, group_by
from lib.analytics import describe, moving_average, correlation
from lib.pipelines import DataPipeline
from lib.datalake import DataLake
from lib.query import Query


def test_mapreduce_wordcount():
    records = ["apple banana apple", "banana orange", "apple"]

    def map_fn(line):
        for w in line.split():
            yield (w, 1)

    def reduce_fn(key, values):
        return (key, sum(values))

    result = dict(MapReduce.execute(records, map_fn, reduce_fn))
    assert result['apple'] == 3
    assert result['banana'] == 2
    assert result['orange'] == 1
    print('✓ MapReduce wordcount')


def test_aggregations_basic():
    vals = [1, 2, 3, 4, 5]
    assert mean(vals) == 3
    assert median(vals) == 3
    groups = group_by([{'k':1,'v':10},{'k':2,'v':20},{'k':1,'v':30}], lambda r: r['k'])
    assert len(groups[1]) == 2
    print('✓ Aggregations basic')


def test_analytics_describe_and_ma():
    vals = [1,2,3,4,5]
    desc = describe(vals)
    assert desc['count'] == 5
    ma = moving_average(vals, window=3)
    assert len(ma) == 5
    c = correlation([1,2,3], [1,2,3])
    assert abs(c - 1.0) < 1e-9
    print('✓ Analytics describe/moving_average/correlation')


def test_pipelines_map_filter_batch():
    data = range(10)
    pipeline = DataPipeline().map(lambda x: x*2).filter(lambda x: x%4==0).batch(3)
    out = pipeline.run(data)
    # flattened output -> batches of numbers divisible by 4 after doubling
    flattened = [y for batch in out for y in batch]
    assert all(x%4==0 for x in flattened)
    print('✓ Pipelines map/filter/batch')


def test_datalake_save_load(tmp_path=None):
    base = 'tests_datalake'
    dl = DataLake(base_path=base)
    records = [{'id':1,'n':'a'},{'id':2,'n':'b'}]
    path = dl.save('small', records)
    loaded = list(dl.load('small'))
    assert loaded[0]['id'] == 1
    # cleanup
    try:
        import shutil
        shutil.rmtree(base)
    except Exception:
        pass
    print('✓ DataLake save/load')


def test_query_filter_select_sort_limit():
    recs = [{'id':1,'v':3},{'id':2,'v':1},{'id':3,'v':2}]
    q = Query(recs).filter(lambda r: r['v']>1).select(['id']).sort_by(lambda r: r['id'], reverse=True).limit(1)
    out = q.all()
    assert len(out) == 1 and 'id' in out[0]
    print('✓ Query filter/select/sort/limit')


def run_all_phase8_tests():
    print('\n' + '='*40)
    print('PHASE 8: DATA PROCESSING - TEST SUITE')
    print('='*40)
    try:
        test_mapreduce_wordcount()
        test_aggregations_basic()
        test_analytics_describe_and_ma()
        test_pipelines_map_filter_batch()
        test_datalake_save_load()
        test_query_filter_select_sort_limit()
        print('\n✓ ALL PHASE 8 TESTS PASSED')
        return True
    except AssertionError as e:
        print('\n✗ TEST FAILED:', e)
        return False

if __name__ == '__main__':
    success = run_all_phase8_tests()
    sys.exit(0 if success else 1)
