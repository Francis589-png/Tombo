"""
Testing Framework Library for TOMBO Language
Professional unit testing, test fixtures, and test runners
"""

from typing import Callable, List, Dict, Any, Optional, Tuple
from collections import defaultdict
import time
import traceback


class TestCase:
    """Base class for test cases"""
    
    def __init__(self, name: str = "TestCase"):
        """Initialize test case"""
        self.name = name
        self.test_methods: List[str] = []
        self.setup_method: Optional[Callable] = None
        self.teardown_method: Optional[Callable] = None
    
    def setUp(self) -> None:
        """Run before each test"""
        pass
    
    def tearDown(self) -> None:
        """Run after each test"""
        pass
    
    def get_test_methods(self) -> List[str]:
        """Get all test methods"""
        return [m for m in dir(self) if m.startswith('test_')]


class TestFixture:
    """Test fixtures for setup and teardown"""
    
    def __init__(self, name: str = "Fixture"):
        """Initialize fixture"""
        self.name = name
        self.setup_called = False
        self.teardown_called = False
        self.data: Dict[str, Any] = {}
    
    def setup(self) -> None:
        """Setup fixture"""
        self.setup_called = True
    
    def teardown(self) -> None:
        """Teardown fixture"""
        self.teardown_called = True
    
    def set_data(self, key: str, value: Any) -> None:
        """Set fixture data"""
        self.data[key] = value
    
    def get_data(self, key: str) -> Any:
        """Get fixture data"""
        return self.data.get(key)


class Assertion:
    """Collection of assertion methods"""
    
    @staticmethod
    def assert_true(condition: bool, message: str = "") -> None:
        """Assert condition is true"""
        if not condition:
            raise AssertionError(f"Expected True, got False. {message}")
    
    @staticmethod
    def assert_false(condition: bool, message: str = "") -> None:
        """Assert condition is false"""
        if condition:
            raise AssertionError(f"Expected False, got True. {message}")
    
    @staticmethod
    def assert_equal(a: Any, b: Any, message: str = "") -> None:
        """Assert equal"""
        if a != b:
            raise AssertionError(f"Expected {b}, got {a}. {message}")
    
    @staticmethod
    def assert_not_equal(a: Any, b: Any, message: str = "") -> None:
        """Assert not equal"""
        if a == b:
            raise AssertionError(f"Expected not equal to {a}. {message}")
    
    @staticmethod
    def assert_is_none(value: Any, message: str = "") -> None:
        """Assert value is None"""
        if value is not None:
            raise AssertionError(f"Expected None, got {value}. {message}")
    
    @staticmethod
    def assert_is_not_none(value: Any, message: str = "") -> None:
        """Assert value is not None"""
        if value is None:
            raise AssertionError(f"Expected not None. {message}")
    
    @staticmethod
    def assert_in(member: Any, container: Any, message: str = "") -> None:
        """Assert member in container"""
        if member not in container:
            raise AssertionError(f"Expected {member} in {container}. {message}")
    
    @staticmethod
    def assert_not_in(member: Any, container: Any, message: str = "") -> None:
        """Assert member not in container"""
        if member in container:
            raise AssertionError(f"Expected {member} not in {container}. {message}")
    
    @staticmethod
    def assert_greater(a: Any, b: Any, message: str = "") -> None:
        """Assert greater than"""
        if a <= b:
            raise AssertionError(f"Expected {a} > {b}. {message}")
    
    @staticmethod
    def assert_less(a: Any, b: Any, message: str = "") -> None:
        """Assert less than"""
        if a >= b:
            raise AssertionError(f"Expected {a} < {b}. {message}")
    
    @staticmethod
    def assert_greater_equal(a: Any, b: Any, message: str = "") -> None:
        """Assert greater or equal"""
        if a < b:
            raise AssertionError(f"Expected {a} >= {b}. {message}")
    
    @staticmethod
    def assert_less_equal(a: Any, b: Any, message: str = "") -> None:
        """Assert less or equal"""
        if a > b:
            raise AssertionError(f"Expected {a} <= {b}. {message}")
    
    @staticmethod
    def assert_almost_equal(a: float, b: float, places: int = 7, message: str = "") -> None:
        """Assert almost equal"""
        if round(a - b, places) != 0:
            raise AssertionError(f"Expected {a} ≈ {b}. {message}")
    
    @staticmethod
    def assert_raises(exception_type: type, func: Callable, *args, **kwargs) -> None:
        """Assert function raises exception"""
        try:
            func(*args, **kwargs)
            raise AssertionError(f"Expected {exception_type.__name__} but none was raised")
        except exception_type:
            pass
    
    @staticmethod
    def assert_is_instance(obj: Any, cls: type, message: str = "") -> None:
        """Assert object is instance of class"""
        if not isinstance(obj, cls):
            raise AssertionError(f"Expected instance of {cls.__name__}, got {type(obj).__name__}. {message}")
    
    @staticmethod
    def assert_list_equal(list1: List, list2: List, message: str = "") -> None:
        """Assert lists are equal"""
        if list1 != list2:
            raise AssertionError(f"Lists not equal: {list1} != {list2}. {message}")
    
    @staticmethod
    def assert_dict_equal(dict1: Dict, dict2: Dict, message: str = "") -> None:
        """Assert dicts are equal"""
        if dict1 != dict2:
            raise AssertionError(f"Dicts not equal: {dict1} != {dict2}. {message}")


class TestResult:
    """Represents test result"""
    
    def __init__(self):
        """Initialize test result"""
        self.tests_run = 0
        self.successes = 0
        self.failures = 0
        self.errors = 0
        self.skipped = 0
        self.test_details: List[Dict[str, Any]] = []
        self.start_time = 0.0
        self.end_time = 0.0
    
    def add_success(self, test_name: str, duration: float) -> None:
        """Add successful test"""
        self.successes += 1
        self.tests_run += 1
        self.test_details.append({
            'name': test_name,
            'status': 'PASS',
            'duration': duration,
            'message': ''
        })
    
    def add_failure(self, test_name: str, message: str, duration: float) -> None:
        """Add failed test"""
        self.failures += 1
        self.tests_run += 1
        self.test_details.append({
            'name': test_name,
            'status': 'FAIL',
            'duration': duration,
            'message': message
        })
    
    def add_error(self, test_name: str, message: str, duration: float) -> None:
        """Add test with error"""
        self.errors += 1
        self.tests_run += 1
        self.test_details.append({
            'name': test_name,
            'status': 'ERROR',
            'duration': duration,
            'message': message
        })
    
    def add_skip(self, test_name: str, reason: str) -> None:
        """Add skipped test"""
        self.skipped += 1
        self.tests_run += 1
        self.test_details.append({
            'name': test_name,
            'status': 'SKIP',
            'duration': 0.0,
            'message': reason
        })
    
    def was_successful(self) -> bool:
        """Check if all tests passed"""
        return self.failures == 0 and self.errors == 0
    
    def get_summary(self) -> str:
        """Get result summary"""
        total_time = self.end_time - self.start_time
        summary = f"\n{'='*60}\n"
        summary += f"Tests run: {self.tests_run}\n"
        summary += f"Passed: {self.successes} ✓\n"
        summary += f"Failed: {self.failures} ✗\n"
        summary += f"Errors: {self.errors} ⚠\n"
        summary += f"Skipped: {self.skipped} ⊘\n"
        summary += f"Total time: {total_time:.3f}s\n"
        summary += f"{'='*60}\n"
        return summary


class TestRunner:
    """Runs tests and collects results"""
    
    def __init__(self, verbosity: int = 1):
        """Initialize test runner"""
        self.verbosity = verbosity
        self.result = TestResult()
        self.fixtures: Dict[str, TestFixture] = {}
    
    def add_fixture(self, name: str, fixture: TestFixture) -> None:
        """Add test fixture"""
        self.fixtures[name] = fixture
    
    def run_test(self, test_func: Callable, test_name: str, 
                 setup: Optional[Callable] = None,
                 teardown: Optional[Callable] = None) -> None:
        """Run single test"""
        start_time = time.time()
        
        try:
            if setup:
                setup()
            
            test_func()
            
            if teardown:
                teardown()
            
            duration = time.time() - start_time
            self.result.add_success(test_name, duration)
            
            if self.verbosity > 0:
                print(f"✓ {test_name} ({duration:.3f}s)")
        
        except AssertionError as e:
            duration = time.time() - start_time
            self.result.add_failure(test_name, str(e), duration)
            if self.verbosity > 0:
                print(f"✗ {test_name}: {e}")
        
        except Exception as e:
            duration = time.time() - start_time
            self.result.add_error(test_name, str(e), duration)
            if self.verbosity > 0:
                print(f"⚠ {test_name}: {e}")
    
    def run_tests(self, test_case: TestCase) -> TestResult:
        """Run all tests in test case"""
        self.result = TestResult()
        self.result.start_time = time.time()
        
        test_methods = test_case.get_test_methods()
        
        for method_name in test_methods:
            method = getattr(test_case, method_name)
            self.run_test(
                method,
                f"{test_case.name}.{method_name}",
                test_case.setUp if hasattr(test_case, 'setUp') else None,
                test_case.tearDown if hasattr(test_case, 'tearDown') else None
            )
        
        self.result.end_time = time.time()
        return self.result
    
    def run_test_suite(self, test_cases: List[TestCase]) -> TestResult:
        """Run multiple test cases"""
        combined_result = TestResult()
        combined_result.start_time = time.time()
        
        for test_case in test_cases:
            result = self.run_tests(test_case)
            combined_result.successes += result.successes
            combined_result.failures += result.failures
            combined_result.errors += result.errors
            combined_result.skipped += result.skipped
            combined_result.tests_run += result.tests_run
            combined_result.test_details.extend(result.test_details)
        
        combined_result.end_time = time.time()
        return combined_result


class MockObject:
    """Mock object for testing"""
    
    def __init__(self):
        """Initialize mock"""
        self.calls: List[Tuple[str, tuple, dict]] = []
        self.return_values: Dict[str, Any] = {}
    
    def __getattr__(self, name: str):
        """Get method"""
        def mock_method(*args, **kwargs):
            self.calls.append((name, args, kwargs))
            return self.return_values.get(name, None)
        return mock_method
    
    def set_return_value(self, method_name: str, value: Any) -> None:
        """Set return value for method"""
        self.return_values[method_name] = value
    
    def get_calls(self, method_name: str) -> List[Tuple[tuple, dict]]:
        """Get calls to method"""
        return [(args, kwargs) for name, args, kwargs in self.calls if name == method_name]
    
    def assert_called(self, method_name: str) -> bool:
        """Check if method was called"""
        return any(name == method_name for name, _, _ in self.calls)
    
    def assert_called_with(self, method_name: str, *args, **kwargs) -> bool:
        """Check if method called with args"""
        for name, call_args, call_kwargs in self.calls:
            if name == method_name and call_args == args and call_kwargs == kwargs:
                return True
        return False


class ParameterizedTest:
    """Parameterized test runner"""
    
    def __init__(self, test_func: Callable, parameters: List[Tuple]):
        """Initialize parameterized test"""
        self.test_func = test_func
        self.parameters = parameters
    
    def run(self, runner: TestRunner) -> TestResult:
        """Run parameterized tests"""
        result = TestResult()
        result.start_time = time.time()
        
        for i, params in enumerate(self.parameters):
            test_name = f"{self.test_func.__name__}[{i}]"
            try:
                self.test_func(*params)
                result.add_success(test_name, 0.0)
            except AssertionError as e:
                result.add_failure(test_name, str(e), 0.0)
            except Exception as e:
                result.add_error(test_name, str(e), 0.0)
        
        result.end_time = time.time()
        return result


class TestSkip:
    """Skip test decorator"""
    
    @staticmethod
    def skip(reason: str = "Test skipped"):
        """Decorator to skip test"""
        def decorator(func):
            func.skip = True
            func.skip_reason = reason
            return func
        return decorator
    
    @staticmethod
    def skip_if(condition: bool, reason: str = "Test skipped"):
        """Conditionally skip test"""
        def decorator(func):
            if condition:
                func.skip = True
                func.skip_reason = reason
            return func
        return decorator


class TestSuite:
    """Collection of test cases"""
    
    def __init__(self, name: str = "TestSuite"):
        """Initialize test suite"""
        self.name = name
        self.test_cases: List[TestCase] = []
    
    def add_test(self, test_case: TestCase) -> None:
        """Add test case to suite"""
        self.test_cases.append(test_case)
    
    def add_tests(self, test_cases: List[TestCase]) -> None:
        """Add multiple test cases"""
        self.test_cases.extend(test_cases)
    
    def run(self, runner: TestRunner) -> TestResult:
        """Run all tests in suite"""
        return runner.run_test_suite(self.test_cases)


# Public API
__all__ = [
    'TestCase',
    'TestFixture',
    'Assertion',
    'TestResult',
    'TestRunner',
    'MockObject',
    'ParameterizedTest',
    'TestSkip',
    'TestSuite'
]
