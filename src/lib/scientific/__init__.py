"""
TOMBO Scientific Computing Library
Linear Algebra, Statistics, Signal Processing, Optimization
"""

import math
from typing import List, Tuple, Optional, Union
from dataclasses import dataclass


# ============================================================================
# MATRIX & LINEAR ALGEBRA
# ============================================================================

@dataclass
class Matrix:
    """Matrix representation and operations"""
    
    def __init__(self, data: List[List[float]]):
        """Initialize matrix from 2D list"""
        if not data or not data[0]:
            raise ValueError("Matrix cannot be empty")
        self.data = data
        self.rows = len(data)
        self.cols = len(data[0])
        
        # Verify rectangular matrix
        for row in data:
            if len(row) != self.cols:
                raise ValueError("Matrix rows must have equal length")
    
    def __str__(self):
        """String representation"""
        lines = []
        for row in self.data:
            row_str = "  ".join(f"{x:8.4f}" for x in row)
            lines.append(f"[ {row_str} ]")
        return "\n".join(lines)
    
    def __getitem__(self, key):
        """Access element or row"""
        if isinstance(key, tuple):
            i, j = key
            return self.data[i][j]
        return self.data[key]
    
    def transpose(self):
        """Return transposed matrix"""
        transposed = [[self.data[j][i] for j in range(self.rows)] 
                      for i in range(self.cols)]
        return Matrix(transposed)
    
    def add(self, other):
        """Element-wise addition"""
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrices must have same dimensions")
        result = [[self.data[i][j] + other.data[i][j] 
                  for j in range(self.cols)] for i in range(self.rows)]
        return Matrix(result)
    
    def subtract(self, other):
        """Element-wise subtraction"""
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrices must have same dimensions")
        result = [[self.data[i][j] - other.data[i][j] 
                  for j in range(self.cols)] for i in range(self.rows)]
        return Matrix(result)
    
    def multiply(self, other):
        """Matrix multiplication"""
        if isinstance(other, (int, float)):
            # Scalar multiplication
            result = [[x * other for x in row] for row in self.data]
            return Matrix(result)
        else:
            # Matrix multiplication
            if self.cols != other.rows:
                raise ValueError("Incompatible dimensions for multiplication")
            result = []
            for i in range(self.rows):
                row = []
                for j in range(other.cols):
                    val = sum(self.data[i][k] * other.data[k][j] 
                             for k in range(self.cols))
                    row.append(val)
                result.append(row)
            return Matrix(result)
    
    def determinant(self):
        """Calculate determinant"""
        if self.rows != self.cols:
            raise ValueError("Determinant only for square matrices")
        
        if self.rows == 1:
            return self.data[0][0]
        if self.rows == 2:
            return (self.data[0][0] * self.data[1][1] - 
                   self.data[0][1] * self.data[1][0])
        
        # Recursive determinant using Laplace expansion
        det = 0
        for j in range(self.cols):
            minor = self._get_minor(0, j)
            cofactor = ((-1) ** j) * minor.determinant()
            det += self.data[0][j] * cofactor
        return det
    
    def _get_minor(self, row_idx, col_idx):
        """Get minor matrix by removing row and column"""
        minor_data = []
        for i in range(self.rows):
            if i == row_idx:
                continue
            row = []
            for j in range(self.cols):
                if j == col_idx:
                    continue
                row.append(self.data[i][j])
            minor_data.append(row)
        return Matrix(minor_data)
    
    def inverse(self):
        """Calculate matrix inverse"""
        if self.rows != self.cols:
            raise ValueError("Inverse only for square matrices")
        
        det = self.determinant()
        if abs(det) < 1e-10:
            raise ValueError("Matrix is singular (determinant is zero)")
        
        if self.rows == 1:
            return Matrix([[1.0 / self.data[0][0]]])
        
        if self.rows == 2:
            a, b = self.data[0]
            c, d = self.data[1]
            return Matrix([[d/det, -b/det], [-c/det, a/det]])
        
        # Gauss-Jordan elimination for larger matrices
        # Create augmented matrix [A | I]
        aug = []
        for i in range(self.rows):
            row = self.data[i][:] + [0.0] * self.cols
            row[self.cols + i] = 1.0
            aug.append(row)
        
        # Forward elimination
        for i in range(self.rows):
            # Find pivot
            max_row = i
            for k in range(i + 1, self.rows):
                if abs(aug[k][i]) > abs(aug[max_row][i]):
                    max_row = k
            aug[i], aug[max_row] = aug[max_row], aug[i]
            
            # Make diagonal 1
            pivot = aug[i][i]
            if abs(pivot) < 1e-10:
                raise ValueError("Matrix is singular")
            
            for j in range(2 * self.cols):
                aug[i][j] /= pivot
            
            # Eliminate column
            for k in range(self.rows):
                if k != i:
                    c = aug[k][i]
                    for j in range(2 * self.cols):
                        aug[k][j] -= c * aug[i][j]
        
        # Extract inverse from right half
        inv_data = []
        for i in range(self.rows):
            inv_data.append(aug[i][self.cols:])
        return Matrix(inv_data)
    
    def trace(self):
        """Sum of diagonal elements"""
        if self.rows != self.cols:
            raise ValueError("Trace only for square matrices")
        return sum(self.data[i][i] for i in range(self.rows))
    
    def norm(self, order=2):
        """Calculate matrix norm"""
        if order == 'fro':  # Frobenius norm
            return math.sqrt(sum(x*x for row in self.data for x in row))
        elif order == 1:  # Column sum norm
            return max(sum(abs(self.data[i][j]) for i in range(self.rows))
                      for j in range(self.cols))
        elif order == float('inf'):  # Row sum norm
            return max(sum(abs(x) for x in row) for row in self.data)
        return self.norm('fro')  # Default to Frobenius


class Vector:
    """Vector operations"""
    
    def __init__(self, data: List[float]):
        self.data = data
        self.length = len(data)
    
    def __str__(self):
        return f"[ {' '.join(f'{x:.4f}' for x in self.data)} ]"
    
    def add(self, other):
        """Vector addition"""
        if self.length != other.length:
            raise ValueError("Vectors must have same length")
        return Vector([self.data[i] + other.data[i] for i in range(self.length)])
    
    def subtract(self, other):
        """Vector subtraction"""
        if self.length != other.length:
            raise ValueError("Vectors must have same length")
        return Vector([self.data[i] - other.data[i] for i in range(self.length)])
    
    def dot(self, other):
        """Dot product"""
        if self.length != other.length:
            raise ValueError("Vectors must have same length")
        return sum(self.data[i] * other.data[i] for i in range(self.length))
    
    def cross(self, other):
        """Cross product (3D vectors only)"""
        if self.length != 3 or other.length != 3:
            raise ValueError("Cross product only for 3D vectors")
        x = self.data[1]*other.data[2] - self.data[2]*other.data[1]
        y = self.data[2]*other.data[0] - self.data[0]*other.data[2]
        z = self.data[0]*other.data[1] - self.data[1]*other.data[0]
        return Vector([x, y, z])
    
    def magnitude(self):
        """Vector magnitude (length)"""
        return math.sqrt(sum(x*x for x in self.data))
    
    def normalize(self):
        """Normalize to unit vector"""
        mag = self.magnitude()
        if abs(mag) < 1e-10:
            raise ValueError("Cannot normalize zero vector")
        return Vector([x / mag for x in self.data])
    
    def scale(self, scalar):
        """Scalar multiplication"""
        return Vector([x * scalar for x in self.data])


# ============================================================================
# STATISTICS
# ============================================================================

class Statistics:
    """Statistical functions and analysis"""
    
    @staticmethod
    def mean(data: List[float]) -> float:
        """Calculate arithmetic mean"""
        return sum(data) / len(data) if data else 0
    
    @staticmethod
    def median(data: List[float]) -> float:
        """Calculate median"""
        sorted_data = sorted(data)
        n = len(sorted_data)
        if n % 2 == 0:
            return (sorted_data[n//2 - 1] + sorted_data[n//2]) / 2
        return sorted_data[n//2]
    
    @staticmethod
    def mode(data: List[float]) -> float:
        """Find most frequent value"""
        if not data:
            return None
        freq = {}
        for x in data:
            freq[x] = freq.get(x, 0) + 1
        return max(freq, key=freq.get)
    
    @staticmethod
    def variance(data: List[float]) -> float:
        """Calculate variance"""
        mean = Statistics.mean(data)
        return sum((x - mean) ** 2 for x in data) / len(data) if data else 0
    
    @staticmethod
    def std_dev(data: List[float]) -> float:
        """Calculate standard deviation"""
        return math.sqrt(Statistics.variance(data))
    
    @staticmethod
    def correlation(x: List[float], y: List[float]) -> float:
        """Pearson correlation coefficient"""
        if len(x) != len(y) or len(x) < 2:
            raise ValueError("Invalid data for correlation")
        
        mean_x = Statistics.mean(x)
        mean_y = Statistics.mean(y)
        
        numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(len(x)))
        denom_x = sum((val - mean_x) ** 2 for val in x)
        denom_y = sum((val - mean_y) ** 2 for val in y)
        
        denominator = math.sqrt(denom_x * denom_y)
        if abs(denominator) < 1e-10:
            return 0
        return numerator / denominator
    
    @staticmethod
    def covariance(x: List[float], y: List[float]) -> float:
        """Calculate covariance"""
        if len(x) != len(y):
            raise ValueError("Sequences must have same length")
        mean_x = Statistics.mean(x)
        mean_y = Statistics.mean(y)
        return sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(len(x))) / len(x)


# ============================================================================
# SIGNAL PROCESSING
# ============================================================================

class Signal:
    """Signal processing operations"""
    
    def __init__(self, data: List[float], sample_rate: float = 1.0):
        self.data = data
        self.sample_rate = sample_rate
        self.length = len(data)
    
    def fft(self):
        """Simple FFT implementation (Cooley-Tukey)"""
        # For simplicity, using naive DFT
        # In production, would use scipy.fft or similar
        N = self.length
        result = []
        for k in range(N):
            real = sum(self.data[n] * math.cos(-2 * math.pi * k * n / N) for n in range(N))
            imag = sum(self.data[n] * math.sin(-2 * math.pi * k * n / N) for n in range(N))
            magnitude = math.sqrt(real**2 + imag**2)
            result.append(magnitude)
        return result
    
    def power_spectrum(self):
        """Calculate power spectrum"""
        fft_result = self.fft()
        return [x**2 / self.length for x in fft_result]
    
    def filter_lowpass(self, cutoff: float):
        """Simple low-pass filter"""
        filtered = []
        alpha = 0.1
        filtered.append(self.data[0])
        for i in range(1, self.length):
            filtered.append(alpha * self.data[i] + (1 - alpha) * filtered[i-1])
        return Signal(filtered, self.sample_rate)
    
    def filter_highpass(self, cutoff: float):
        """Simple high-pass filter"""
        filtered = []
        alpha = 0.1
        filtered.append(self.data[0])
        for i in range(1, self.length):
            filtered.append(alpha * (filtered[i-1] + self.data[i] - self.data[i-1]))
        return Signal(filtered, self.sample_rate)


# ============================================================================
# OPTIMIZATION
# ============================================================================

class Optimization:
    """Optimization algorithms"""
    
    @staticmethod
    def gradient_descent(func, grad_func, x0, learning_rate=0.01, iterations=1000):
        """Gradient descent optimization"""
        x = x0
        history = [x]
        
        for _ in range(iterations):
            grad = grad_func(x)
            x = x - learning_rate * grad
            history.append(x)
            
            # Early stopping if gradient is very small
            if abs(grad) < 1e-10:
                break
        
        return x, history
    
    @staticmethod
    def newton_method(func, derivative, x0, iterations=100):
        """Newton's method for root finding"""
        x = x0
        
        for _ in range(iterations):
            fx = func(x)
            if abs(fx) < 1e-10:
                break
            
            df = derivative(x)
            if abs(df) < 1e-10:
                break
            
            x = x - fx / df
        
        return x


# ============================================================================
# PUBLIC API FUNCTIONS
# ============================================================================

def matrix(data):
    """Create matrix"""
    return Matrix(data)

def vector(data):
    """Create vector"""
    return Vector(data)

def mean(data):
    """Calculate mean"""
    return Statistics.mean(data)

def median(data):
    """Calculate median"""
    return Statistics.median(data)

def std(data):
    """Calculate standard deviation"""
    return Statistics.std_dev(data)

def variance(data):
    """Calculate variance"""
    return Statistics.variance(data)

def correlation(x, y):
    """Calculate correlation"""
    return Statistics.correlation(x, y)

def covariance(x, y):
    """Calculate covariance"""
    return Statistics.covariance(x, y)

def signal(data, sample_rate=1.0):
    """Create signal"""
    return Signal(data, sample_rate)

def fft(data):
    """Fast Fourier Transform"""
    sig = Signal(data)
    return sig.fft()

def power_spectrum(data):
    """Calculate power spectrum"""
    sig = Signal(data)
    return sig.power_spectrum()

def minimize(func, grad_func, x0, learning_rate=0.01, iterations=1000):
    """Minimize function using gradient descent"""
    return Optimization.gradient_descent(func, grad_func, x0, learning_rate, iterations)

def find_root(func, derivative, x0, iterations=100):
    """Find root using Newton's method"""
    return Optimization.newton_method(func, derivative, x0, iterations)
