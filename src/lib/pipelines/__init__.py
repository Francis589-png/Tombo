"""
Pipelines library - composable data processing pipelines
"""
from typing import Callable, Iterable, List, Any


class DataPipeline:
    """Chainable pipeline for transforming iterable data."""

    def __init__(self):
        self.steps: List[Callable[[Iterable[Any]], Iterable[Any]]] = []

    def add_step(self, fn: Callable[[Iterable[Any]], Iterable[Any]]):
        self.steps.append(fn)
        return self

    def run(self, data: Iterable[Any]):
        current = data
        for step in self.steps:
            current = step(current)
        return list(current)

    def map(self, fn: Callable[[Any], Any]):
        def step(it):
            for x in it:
                yield fn(x)
        return self.add_step(step)

    def filter(self, predicate: Callable[[Any], bool]):
        def step(it):
            for x in it:
                if predicate(x):
                    yield x
        return self.add_step(step)

    def batch(self, size: int):
        def step(it):
            batch = []
            for x in it:
                batch.append(x)
                if len(batch) >= size:
                    yield batch
                    batch = []
            if batch:
                yield batch
        return self.add_step(step)
