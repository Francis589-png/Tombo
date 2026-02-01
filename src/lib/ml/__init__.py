"""
TOMBO ML Domain - Basic Machine Learning Library

Provides basic ML models, training utilities, and data preprocessing.
Note: This is a simplified implementation. Production code should use scikit-learn, TensorFlow, etc.
"""

import random
import math
from typing import List, Dict, Tuple, Any, Callable


class DataSet:
    """Simple dataset wrapper."""
    
    def __init__(self, features: List[List[float]], labels: List[Any]):
        if len(features) != len(labels):
            raise ValueError("Features and labels must have same length")
        self.features = features
        self.labels = labels
        self.n_samples = len(features)
        self.n_features = len(features[0]) if features else 0
    
    def split(self, test_ratio=0.2):
        """Split dataset into train/test sets."""
        n_test = int(self.n_samples * test_ratio)
        indices = list(range(self.n_samples))
        random.shuffle(indices)
        
        test_indices = set(indices[:n_test])
        train_features = [self.features[i] for i in range(self.n_samples) if i not in test_indices]
        train_labels = [self.labels[i] for i in range(self.n_samples) if i not in test_indices]
        test_features = [self.features[i] for i in test_indices]
        test_labels = [self.labels[i] for i in test_indices]
        
        return (DataSet(train_features, train_labels), 
                DataSet(test_features, test_labels))
    
    def shuffle(self):
        """Shuffle the dataset in-place."""
        indices = list(range(self.n_samples))
        random.shuffle(indices)
        self.features = [self.features[i] for i in indices]
        self.labels = [self.labels[i] for i in indices]
    
    def normalize(self):
        """Normalize features to [0, 1] range."""
        if not self.features or not self.n_features:
            return
        
        # Find min/max for each feature
        mins = [float('inf')] * self.n_features
        maxs = [float('-inf')] * self.n_features
        
        for features in self.features:
            for i, f in enumerate(features):
                mins[i] = min(mins[i], f)
                maxs[i] = max(maxs[i], f)
        
        # Normalize
        for features in self.features:
            for i in range(self.n_features):
                range_val = maxs[i] - mins[i]
                if range_val > 0:
                    features[i] = (features[i] - mins[i]) / range_val
    
    def __len__(self):
        return self.n_samples
    
    def __getitem__(self, idx):
        return self.features[idx], self.labels[idx]


class LinearRegression:
    """Simple linear regression model."""
    
    def __init__(self, learning_rate=0.01, iterations=1000):
        self.lr = learning_rate
        self.iterations = iterations
        self.weights = None
        self.bias = None
    
    def fit(self, X: List[List[float]], y: List[float]):
        """Train the model."""
        n_samples = len(X)
        n_features = len(X[0])
        
        # Initialize weights
        self.weights = [0.0] * n_features
        self.bias = 0.0
        
        # Gradient descent
        for _ in range(self.iterations):
            # Predictions
            predictions = [
                sum(self.weights[j] * X[i][j] for j in range(n_features)) + self.bias
                for i in range(n_samples)
            ]
            
            # Calculate gradients
            dw = [0.0] * n_features
            db = 0.0
            
            for i in range(n_samples):
                error = predictions[i] - y[i]
                db += error
                for j in range(n_features):
                    dw[j] += error * X[i][j]
            
            # Update parameters
            db /= n_samples
            for j in range(n_features):
                dw[j] /= n_samples
                self.weights[j] -= self.lr * dw[j]
            self.bias -= self.lr * db
    
    def predict(self, X: List[List[float]]) -> List[float]:
        """Make predictions."""
        predictions = []
        for features in X:
            pred = sum(self.weights[j] * features[j] for j in range(len(self.weights))) + self.bias
            predictions.append(pred)
        return predictions
    
    def score(self, X: List[List[float]], y: List[float]) -> float:
        """Calculate R² score."""
        predictions = self.predict(X)
        y_mean = sum(y) / len(y)
        
        ss_res = sum((y[i] - predictions[i]) ** 2 for i in range(len(y)))
        ss_tot = sum((y[i] - y_mean) ** 2 for i in range(len(y)))
        
        return 1 - (ss_res / ss_tot) if ss_tot > 0 else 0


class LogisticRegression:
    """Simple logistic regression for binary classification."""
    
    def __init__(self, learning_rate=0.01, iterations=1000):
        self.lr = learning_rate
        self.iterations = iterations
        self.weights = None
        self.bias = None
    
    def _sigmoid(self, x):
        """Sigmoid activation function."""
        return 1 / (1 + math.exp(-x))
    
    def fit(self, X: List[List[float]], y: List[int]):
        """Train the model."""
        n_samples = len(X)
        n_features = len(X[0])
        
        self.weights = [0.0] * n_features
        self.bias = 0.0
        
        for _ in range(self.iterations):
            # Predictions
            predictions = []
            for i in range(n_samples):
                z = sum(self.weights[j] * X[i][j] for j in range(n_features)) + self.bias
                pred = self._sigmoid(z)
                predictions.append(pred)
            
            # Gradients
            dw = [0.0] * n_features
            db = 0.0
            
            for i in range(n_samples):
                error = predictions[i] - y[i]
                db += error
                for j in range(n_features):
                    dw[j] += error * X[i][j]
            
            # Update
            db /= n_samples
            for j in range(n_features):
                dw[j] /= n_samples
                self.weights[j] -= self.lr * dw[j]
            self.bias -= self.lr * db
    
    def predict(self, X: List[List[float]]) -> List[int]:
        """Make predictions."""
        predictions = []
        for features in X:
            z = sum(self.weights[j] * features[j] for j in range(len(self.weights))) + self.bias
            pred = self._sigmoid(z)
            predictions.append(1 if pred > 0.5 else 0)
        return predictions
    
    def predict_proba(self, X: List[List[float]]) -> List[float]:
        """Get prediction probabilities."""
        probs = []
        for features in X:
            z = sum(self.weights[j] * features[j] for j in range(len(self.weights))) + self.bias
            pred = self._sigmoid(z)
            probs.append(pred)
        return probs
    
    def accuracy(self, X: List[List[float]], y: List[int]) -> float:
        """Calculate accuracy."""
        predictions = self.predict(X)
        correct = sum(1 for i in range(len(y)) if predictions[i] == y[i])
        return correct / len(y)


class KNearestNeighbors:
    """K-Nearest Neighbors classifier."""
    
    def __init__(self, k=3):
        self.k = k
        self.X_train = None
        self.y_train = None
    
    def fit(self, X: List[List[float]], y: List[Any]):
        """Store training data."""
        self.X_train = X
        self.y_train = y
    
    def _distance(self, x1: List[float], x2: List[float]) -> float:
        """Calculate Euclidean distance."""
        return math.sqrt(sum((x1[i] - x2[i]) ** 2 for i in range(len(x1))))
    
    def predict(self, X: List[List[float]]) -> List[Any]:
        """Make predictions."""
        predictions = []
        for x in X:
            # Find k nearest neighbors
            distances = [
                (self._distance(x, self.X_train[i]), self.y_train[i])
                for i in range(len(self.X_train))
            ]
            distances.sort()
            neighbors = distances[:self.k]
            
            # Vote on label
            from collections import Counter
            labels = [neighbor[1] for neighbor in neighbors]
            pred = Counter(labels).most_common(1)[0][0]
            predictions.append(pred)
        
        return predictions
    
    def accuracy(self, X: List[List[float]], y: List[Any]) -> float:
        """Calculate accuracy."""
        predictions = self.predict(X)
        correct = sum(1 for i in range(len(y)) if predictions[i] == y[i])
        return correct / len(y) if y else 0


def create_dataset(features, labels):
    """Create a dataset."""
    return DataSet(features, labels)


def linear_regression(lr=0.01, iterations=1000):
    """Create a linear regression model."""
    return LinearRegression(lr, iterations)


def logistic_regression(lr=0.01, iterations=1000):
    """Create a logistic regression model."""
    return LogisticRegression(lr, iterations)


def knn(k=3):
    """Create a K-Nearest Neighbors model."""
    return KNearestNeighbors(k)


def train_test_split(X, y, test_ratio=0.2):
    """Split data into train/test sets."""
    dataset = DataSet(X, y)
    train, test = dataset.split(test_ratio)
    return train.features, test.features, train.labels, test.labels


def normalize_features(X):
    """Normalize features to [0, 1]."""
    dataset = DataSet(X, [0] * len(X))
    dataset.normalize()
    return dataset.features


def mean_squared_error(y_true, y_pred):
    """Calculate MSE."""
    return sum((y_true[i] - y_pred[i]) ** 2 for i in range(len(y_true))) / len(y_true)


def accuracy_score(y_true, y_pred):
    """Calculate accuracy."""
    correct = sum(1 for i in range(len(y_true)) if y_true[i] == y_pred[i])
    return correct / len(y_true) if y_true else 0


def register(env):
    """Register ML functions in the environment."""
    ml_funcs = {
        'create_dataset': create_dataset,
        'linear_regression': linear_regression,
        'logistic_regression': logistic_regression,
        'knn': knn,
        'train_test_split': train_test_split,
        'normalize_features': normalize_features,
        'mean_squared_error': mean_squared_error,
        'accuracy_score': accuracy_score,
    }
    
    for name, func in ml_funcs.items():
        env.register_function(name, func, is_builtin=True)
