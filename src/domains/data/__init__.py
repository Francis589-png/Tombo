"""
TOMBO Data Domain - MapReduce, Aggregations, Analytics, Pipelines, DataLake, Query
Domain grouping for Phase 8 data-processing libraries
"""
from tombo.lib.mapreduce import MapReduce
from tombo.lib.aggregations import sum_values, mean, median, variance, stddev, group_by
from tombo.lib.analytics import describe, moving_average, correlation
from tombo.lib.pipelines import DataPipeline
from tombo.lib.datalake import DataLake
from tombo.lib.query import Query

__all__ = [
    'MapReduce', 'sum_values', 'mean', 'median', 'variance', 'stddev', 'group_by',
    'describe', 'moving_average', 'correlation', 'DataPipeline', 'DataLake', 'Query'
]

DOMAIN_NAME = 'data'
DOMAIN_LIBRARIES = ['mapreduce', 'aggregations', 'analytics', 'pipelines', 'datalake', 'query']
DOMAIN_VERSION = '8.0.0'
