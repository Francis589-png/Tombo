"""
TOMBO Domain Module System

Provides dynamic library loading, registration, and interop between domains.
Supports 14 domains with 63+ built-in libraries and 5000+ functions.
"""

import importlib
import sys
from typing import Dict, List, Callable, Any, Optional
from pathlib import Path


class DomainRegistry:
    """Central registry for domains, libraries, and their functions."""

    def __init__(self):
        self.domains: Dict[str, 'Domain'] = {}
        self.libraries: Dict[str, 'Library'] = {}
        self.global_functions: Dict[str, Callable] = {}
        self.global_constants: Dict[str, Any] = {}
        self._dependency_graph: Dict[str, List[str]] = {}
        self._loaded_libraries: set = set()

    def register_domain(self, name: str, description: str = "", version: str = "1.0.0"):
        """Register a new domain."""
        domain = Domain(name, description, version)
        self.domains[name] = domain
        self._dependency_graph[name] = []
        return domain

    def register_library(self, domain_name: str, library_name: str, module_path: str = None):
        """Register a library under a domain."""
        if domain_name not in self.domains:
            self.register_domain(domain_name)

        if module_path is None:
            module_path = f"src.lib.{domain_name}.{library_name}"

        lib = Library(library_name, domain_name, module_path)
        lib_key = f"{domain_name}.{library_name}"
        self.libraries[lib_key] = lib
        self.domains[domain_name].add_library(lib)
        return lib

    def load_library(self, domain_name: str, library_name: str, env=None) -> bool:
        """Dynamically load a library and register its functions."""
        lib_key = f"{domain_name}.{library_name}"

        if lib_key in self._loaded_libraries:
            return True

        if lib_key not in self.libraries:
            print(f"Warning: Library {lib_key} not registered")
            return False

        lib = self.libraries[lib_key]
        try:
            # Try to import the library module
            module = importlib.import_module(lib.module_path)

            # Call register function if it exists
            if hasattr(module, 'register') and env is not None:
                module.register(env)

            # Extract available functions
            lib.functions = {
                name: getattr(module, name)
                for name in dir(module)
                if not name.startswith('_') and callable(getattr(module, name))
            }

            self._loaded_libraries.add(lib_key)
            return True
        except ImportError as e:
            print(f"Warning: Could not load library {lib_key}: {e}")
            return False
        except Exception as e:
            print(f"Error loading library {lib_key}: {e}")
            return False

    def load_domain(self, domain_name: str, env=None) -> bool:
        """Load all libraries in a domain."""
        if domain_name not in self.domains:
            print(f"Warning: Domain {domain_name} not registered")
            return False

        domain = self.domains[domain_name]
        all_loaded = True

        for lib in domain.libraries:
            if not self.load_library(domain_name, lib.name, env):
                all_loaded = False

        return all_loaded

    def load_all(self, env=None) -> int:
        """Load all registered libraries. Returns count of successfully loaded libraries."""
        count = 0
        for lib_key in self.libraries:
            domain, lib_name = lib_key.split('.')
            if self.load_library(domain, lib_name, env):
                count += 1
        return count

    def get_library(self, domain_name: str, library_name: str) -> Optional['Library']:
        """Get a library by domain and name."""
        lib_key = f"{domain_name}.{library_name}"
        return self.libraries.get(lib_key)

    def get_domain(self, domain_name: str) -> Optional['Domain']:
        """Get a domain by name."""
        return self.domains.get(domain_name)

    def list_domains(self) -> List[str]:
        """List all registered domains."""
        return sorted(self.domains.keys())

    def list_libraries(self, domain_name: str = None) -> List[str]:
        """List libraries, optionally filtered by domain."""
        if domain_name:
            if domain_name in self.domains:
                return [lib.name for lib in self.domains[domain_name].libraries]
            return []
        return sorted(self.libraries.keys())

    def list_functions(self, domain_name: str = None, library_name: str = None) -> List[str]:
        """List all functions, optionally filtered by domain/library."""
        functions = []

        if domain_name and library_name:
            lib = self.get_library(domain_name, library_name)
            return list(lib.functions.keys()) if lib else []

        if domain_name:
            domain = self.get_domain(domain_name)
            if domain:
                for lib in domain.libraries:
                    functions.extend(lib.functions.keys())
            return sorted(set(functions))

        # All functions across all libraries
        for lib in self.libraries.values():
            functions.extend(lib.functions.keys())
        return sorted(set(functions))

    def describe(self) -> str:
        """Generate a description of registered domains and libraries."""
        lines = ["TOMBO Language Domain Registry"]
        lines.append("=" * 50)
        lines.append(f"\nDomains: {len(self.domains)}")
        lines.append(f"Libraries: {len(self.libraries)}")
        lines.append(f"Loaded: {len(self._loaded_libraries)}")
        lines.append("\nDomains:")

        for domain_name in sorted(self.domains.keys()):
            domain = self.domains[domain_name]
            lines.append(f"  {domain_name:20} - {domain.description or 'N/A'}")
            for lib in domain.libraries:
                status = "✓" if f"{domain_name}.{lib.name}" in self._loaded_libraries else " "
                lines.append(f"    [{status}] {lib.name}")

        return "\n".join(lines)


class Domain:
    """Represents a major domain (Web, Database, ML, etc.)."""

    def __init__(self, name: str, description: str = "", version: str = "1.0.0"):
        self.name = name
        self.description = description
        self.version = version
        self.libraries: List['Library'] = []
        self.metadata: Dict[str, Any] = {}

    def add_library(self, library: 'Library'):
        """Add a library to this domain."""
        if library not in self.libraries:
            self.libraries.append(library)

    def __repr__(self):
        return f"Domain({self.name}, {len(self.libraries)} libraries)"


class Library:
    """Represents a library (e.g., 'http' under 'web' domain)."""

    def __init__(self, name: str, domain: str, module_path: str):
        self.name = name
        self.domain = domain
        self.module_path = module_path
        self.functions: Dict[str, Callable] = {}
        self.constants: Dict[str, Any] = {}
        self.dependencies: List[str] = []
        self.metadata: Dict[str, Any] = {}

    def __repr__(self):
        return f"Library({self.domain}.{self.name})"


def create_default_registry() -> DomainRegistry:
    """Create and populate the default TOMBO domain registry with all 14 domains."""
    registry = DomainRegistry()

    # Tier 1: Core & Critical
    registry.register_domain("io", "File I/O, console, input/output", "1.0.0")
    registry.register_domain("web", "Web APIs, HTTP, REST, WebSockets", "1.0.0")
    registry.register_domain("database", "SQL, NoSQL, ORM, migrations", "1.0.0")
    registry.register_domain("filesystem", "File operations, paths, streams", "1.0.0")

    # Tier 2: Data & Analysis
    registry.register_domain("ml", "Machine learning, neural networks, NLP", "1.0.0")
    registry.register_domain("scientific", "Scientific computing, stats, plotting", "1.0.0")
    registry.register_domain("datascience", "DataFrames, ETL, transformations", "1.0.0")
    registry.register_domain("collections", "Maps, sets, queues, trees", "1.0.0")

    # Tier 3: Systems & Dev
    registry.register_domain("blockchain", "Blockchain, crypto, smart contracts", "1.0.0")
    registry.register_domain("robotics", "Robot control, sensors, vision", "1.0.0")
    registry.register_domain("iot", "IoT devices, MQTT, edge computing", "1.0.0")
    registry.register_domain("devops", "Containers, orchestration, infra", "1.0.0")

    # Tier 4: Graphics & Specialized
    registry.register_domain("game", "Game engine, graphics, physics, audio", "1.0.0")
    registry.register_domain("gui", "Desktop GUI, widgets, theming", "1.0.0")

    # Additional Specialized
    registry.register_domain("mobile", "iOS/Android APIs", "1.0.0")
    registry.register_domain("quantum", "Quantum circuits, gates, simulation", "1.0.0")
    registry.register_domain("bioinformatics", "Sequence analysis, genomics", "1.0.0")
    registry.register_domain("finance", "Trading, portfolio, pricing models", "1.0.0")
    registry.register_domain("cad", "3D modeling, transformations, exports", "1.0.0")

    # Utility/System Domains
    registry.register_domain("system", "OS interactions, system info, args", "1.0.0")
    registry.register_domain("utils", "Utility functions, helpers", "1.0.0")
    registry.register_domain("testing", "Unit tests, assertions, mocking", "1.0.0")
    registry.register_domain("debug", "Debugging, profiling, tracing", "1.0.0")

    # === Register Core Libraries (Always Available) ===
    registry.register_library("io", "core", "src.lib.core")
    registry.register_library("io", "io", "src.lib.io")
    registry.register_library("io", "math", "src.lib.math")
    registry.register_library("io", "string", "src.lib.string")
    registry.register_library("io", "collections", "src.lib.collections")
    registry.register_library("io", "time", "src.lib.time")
    registry.register_library("io", "regex", "src.lib.regex")
    registry.register_library("io", "json", "src.lib.json")
    registry.register_library("io", "xml", "src.lib.xml")
    registry.register_library("io", "crypto", "src.lib.crypto")
    registry.register_library("io", "os", "src.lib.os")
    registry.register_library("io", "sys", "src.lib.sys")
    registry.register_library("io", "iter", "src.lib.iter")
    registry.register_library("io", "functools", "src.lib.functools")
    registry.register_library("io", "types", "src.lib.types")

    # === Register Libraries ===

    # Core/IO domain libraries
    registry.register_library("io", "print_module", "src.lib.io")
    registry.register_library("io", "input_module", "src.lib.io")
    registry.register_library("io", "file", "src.lib.io.file")
    registry.register_library("io", "path", "src.lib.io.path")
    registry.register_library("io", "stream", "src.lib.io.stream")

    # Web domain libraries (Phase 5-6)
    registry.register_library("web", "web", "src.lib.web")
    registry.register_library("web", "http", "src.lib.http")
    registry.register_library("web", "rest", "src.lib.rest")
    registry.register_library("web", "graphql", "src.lib.graphql")
    registry.register_library("web", "websocket", "src.lib.websocket")
    registry.register_library("web", "auth", "src.lib.auth")

    # Database domain libraries (Phase 5)
    registry.register_library("database", "database", "src.lib.database")
    registry.register_library("database", "orm", "src.lib.orm")
    registry.register_library("database", "cache", "src.lib.cache")

    # Data domain libraries (Phase 6)
    registry.register_library("datascience", "etl", "src.lib.etl")
    registry.register_library("datascience", "streaming", "src.lib.streaming")
    
    # NLP domain libraries (Phase 6)
    registry.register_library("ml", "nlp", "src.lib.nlp")

    # Filesystem domain
    registry.register_library("filesystem", "operations", "src.lib.filesystem")
    registry.register_library("filesystem", "watcher", "src.lib.filesystem.watcher")
    registry.register_library("filesystem", "compression", "src.lib.filesystem.compression")

    # Collections domain (core)
    registry.register_library("collections", "list", "src.lib.collections")
    registry.register_library("collections", "dict", "src.lib.collections")
    registry.register_library("collections", "set", "src.lib.collections")
    registry.register_library("collections", "queue", "src.lib.collections")

    # ML domain libraries (8 total)
    registry.register_library("ml", "models", "src.lib.ml.models")
    registry.register_library("ml", "neural", "src.lib.ml.neural")
    registry.register_library("ml", "data", "src.lib.ml.data")
    registry.register_library("ml", "nlp", "src.lib.ml.nlp")
    registry.register_library("ml", "vision", "src.lib.ml.vision")
    registry.register_library("ml", "metrics", "src.lib.ml.metrics")
    registry.register_library("ml", "tune", "src.lib.ml.tune")
    registry.register_library("ml", "inference", "src.lib.ml.inference")

    # Scientific domain libraries (5 total)
    registry.register_library("scientific", "core", "src.lib.scientific")
    registry.register_library("scientific", "scipy", "src.lib.scientific.scipy")
    registry.register_library("scientific", "numpy", "src.lib.scientific.numpy")
    registry.register_library("scientific", "stats", "src.lib.scientific.stats")
    registry.register_library("scientific", "plotting", "src.lib.scientific.plotting")
    registry.register_library("scientific", "signal", "src.lib.scientific.signal")

    # DataScience domain
    registry.register_library("datascience", "pandas", "src.lib.datascience.pandas")
    registry.register_library("datascience", "polars", "src.lib.datascience.polars")
    registry.register_library("datascience", "etl", "src.lib.datascience.etl")
    registry.register_library("datascience", "transform", "src.lib.datascience.transform")

    # Blockchain domain
    registry.register_library("blockchain", "blockchain", "src.lib.blockchain")
    registry.register_library("blockchain", "crypto", "src.lib.blockchain.crypto")
    registry.register_library("blockchain", "smart_contracts", "src.lib.blockchain.smart_contracts")
    registry.register_library("blockchain", "web3", "src.lib.blockchain.web3")

    # Robotics domain
    registry.register_library("robotics", "control", "src.lib.robotics.control")
    registry.register_library("robotics", "sensors", "src.lib.robotics.sensors")
    registry.register_library("robotics", "vision", "src.lib.robotics.vision")
    registry.register_library("robotics", "planning", "src.lib.robotics.planning")

    # IoT domain
    registry.register_library("iot", "devices", "src.lib.iot.devices")
    registry.register_library("iot", "mqtt", "src.lib.iot.mqtt")
    registry.register_library("iot", "protocol", "src.lib.iot.protocol")
    registry.register_library("iot", "edge", "src.lib.iot.edge")

    # Game domain
    registry.register_library("game", "graphics", "src.lib.game.graphics")
    registry.register_library("game", "physics", "src.lib.game.physics")
    registry.register_library("game", "audio", "src.lib.game.audio")
    registry.register_library("game", "input", "src.lib.game.input")
    registry.register_library("game", "ui", "src.lib.game.ui")

    # GUI domain
    registry.register_library("gui", "window", "src.lib.gui")
    registry.register_library("gui", "widgets", "src.lib.gui.widgets")
    registry.register_library("gui", "theme", "src.lib.gui.theme")

    # Image Processing domain
    registry.register_library("image", "core", "src.lib.image")
    registry.register_library("image", "filters", "src.lib.image.filters")
    registry.register_library("image", "analysis", "src.lib.image.analysis")

    # Audio Processing domain
    registry.register_library("audio", "core", "src.lib.audio")
    registry.register_library("audio", "synthesis", "src.lib.audio.synthesis")
    registry.register_library("audio", "analysis", "src.lib.audio.analysis")

    # Network domain
    registry.register_library("network", "sockets", "src.lib.network")
    registry.register_library("network", "protocols", "src.lib.network.protocols")
    registry.register_library("network", "tools", "src.lib.network.tools")

    # Concurrency domain
    registry.register_library("concurrency", "threading", "src.lib.concurrency")
    registry.register_library("concurrency", "async", "src.lib.concurrency.async")
    registry.register_library("concurrency", "multiprocessing", "src.lib.concurrency.multiprocessing")

    # Specialized domains (remaining)
    registry.register_library("cad", "cad", "src.lib.cad")
    registry.register_library("mobile", "mobile", "src.lib.mobile")
    registry.register_library("quantum", "quantum", "src.lib.quantum")
    registry.register_library("bioinformatics", "bioinformatics", "src.lib.bioinformatics")
    registry.register_library("finance", "finance", "src.lib.finance")

    # System/Utility domains
    registry.register_library("system", "os", "src.lib.system")
    registry.register_library("system", "sys", "src.lib.system")
    registry.register_library("utils", "json", "src.lib.utils.json")
    registry.register_library("utils", "time", "src.lib.utils.time")
    registry.register_library("utils", "random", "src.lib.utils.random")
    registry.register_library("utils", "hash", "src.lib.utils.hash")
    registry.register_library("utils", "serialization", "src.lib.utils.serialization")
    registry.register_library("utils", "logging", "src.lib.utils.logging")
    registry.register_library("utils", "config", "src.lib.utils.config")
    registry.register_library("testing", "core", "src.lib.testing")
    registry.register_library("testing", "fixtures", "src.lib.testing")
    registry.register_library("testing", "mocks", "src.lib.testing")
    registry.register_library("debug", "core", "src.lib.debug")
    registry.register_library("debug", "profiler", "src.lib.debug")
    registry.register_library("datascience", "core", "src.lib.datascience")
    registry.register_library("datascience", "analysis", "src.lib.datascience")
    registry.register_library("datascience", "visualization", "src.lib.datascience")
    registry.register_library("game", "core", "src.lib.game")
    registry.register_library("game", "engine", "src.lib.game")
    registry.register_library("mobile", "ui", "src.lib.mobile")
    registry.register_library("mobile", "sensors", "src.lib.mobile")
    registry.register_library("mobile", "notifications", "src.lib.mobile")
    registry.register_library("mobile", "storage", "src.lib.mobile")

    return registry


# Global registry instance
_global_registry: Optional[DomainRegistry] = None


def get_registry() -> DomainRegistry:
    """Get the global domain registry, creating it if necessary."""
    global _global_registry
    if _global_registry is None:
        _global_registry = create_default_registry()
    return _global_registry


def reset_registry():
    """Reset the global registry (useful for testing)."""
    global _global_registry
    _global_registry = None
