"""
DomainManager: loads pluggable domains on demand.
Simple singleton manager for now; domains are Python modules under `src/domains/<name>/`.
Each domain module should implement `register(env)` to register functions/values into the environment.
"""
import importlib
import os

class DomainManager:
    _instance = None

    def __init__(self):
        self.domains = {}

    @classmethod
    def get(cls):
        if cls._instance is None:
            cls._instance = DomainManager()
        return cls._instance

    def load_domain(self, name):
        if name in self.domains:
            return self.domains[name]
        # try to import src.domains.<name>
        module_name = f"src.domains.{name}"
        try:
            mod = importlib.import_module(module_name)
        except ModuleNotFoundError:
            return None
        # module should expose `register(env)`
        self.domains[name] = mod
        return mod

    def provides(self, capability):
        for dom in self.domains.values():
            if hasattr(dom, 'provides') and capability in getattr(dom, 'provides'):
                return True
        return False
