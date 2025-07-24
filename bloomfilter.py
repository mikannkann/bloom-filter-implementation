#!/usr/bin/env python3
"""
Simple Bloom Filter Implementation

A space-efficient probabilistic data structure for membership testing.
Supports optimal parameter calculation based on expected number of elements
and desired false positive probability.
"""

import hashlib
import math
from typing import Union, Any


class SimpleBloomFilter:
    """
    A simple Bloom filter implementation using MD5 hash functions.
    
    Attributes:
        n (int): Expected number of elements
        p (float): Desired false positive probability
        m (int): Optimal number of bits in the bit array
        k (int): Optimal number of hash functions
        bit_array (list): The bit array for the filter
        num_elements (int): Current number of elements added
    """
    
    def __init__(self, capacity: int, false_positive_probability: float):
        """
        Initialize Bloom filter with optimal parameters.
        
        Args:
            capacity: Expected number of elements to be inserted
            false_positive_probability: Desired false positive rate (0 < p < 1)
        """
        self.n = capacity
        self.p = false_positive_probability
        
        # Calculate optimal number of bits and hash functions
        self.m = self._calculate_optimal_m()
        self.k = self._calculate_optimal_k()
        
        # Initialize bit array
        self.bit_array = [False] * self.m
        self.num_elements = 0
    
    def _calculate_optimal_m(self) -> int:
        """
        Calculate optimal number of bits in the filter.
        Formula: m = -(n × ln(p)) / (ln(2)²)
        """
        return int(-self.n * math.log(self.p) / (math.log(2) ** 2))
    
    def _calculate_optimal_k(self) -> int:
        """
        Calculate optimal number of hash functions.
        Formula: k = (m/n) × ln(2)
        """
        return int((self.m / self.n) * math.log(2))
    
    def _hash(self, item: Union[str, int], seed: int) -> int:
        """
        Generate hash value for an item with given seed.
        
        Args:
            item: Item to hash
            seed: Seed value for hash function variation
            
        Returns:
            Hash value modulo m
        """
        # Convert item to string if it's not already
        if isinstance(item, int):
            item_str = str(item)
        else:
            item_str = str(item)
        
        # Create hash with seed
        hash_input = f"{item_str}_{seed}".encode('utf-8')
        hash_value = int(hashlib.md5(hash_input).hexdigest(), 16)
        return hash_value % self.m
    
    def add(self, item: Union[str, int]) -> None:
        """
        Add an item to the Bloom filter.
        
        Args:
            item: Item to add to the filter
        """
        for i in range(self.k):
            index = self._hash(item, i)
            self.bit_array[index] = True
        self.num_elements += 1
    
    def contains(self, item: Union[str, int]) -> bool:
        """
        Test if an item might be in the set.
        
        Args:
            item: Item to test for membership
            
        Returns:
            True if item might be in set (could be false positive)
            False if item is definitely not in set
        """
        for i in range(self.k):
            index = self._hash(item, i)
            if not self.bit_array[index]:
                return False
        return True
    
    def __contains__(self, item: Union[str, int]) -> bool:
        """Support for Python's 'in' operator."""
        return self.contains(item)
    
    def get_current_false_positive_probability(self) -> float:
        """
        Calculate current false positive probability based on actual fill ratio.
        Formula: p = (1 - e^(-k×n_actual/m))^k
        """
        if self.num_elements == 0:
            return 0.0
        return (1 - math.exp(-self.k * self.num_elements / self.m)) ** self.k
    
    def get_fill_ratio(self) -> float:
        """Get the ratio of set bits in the filter."""
        return sum(self.bit_array) / self.m
    
    def print_stats(self) -> None:
        """Print current filter statistics."""
        current_fp = self.get_current_false_positive_probability()
        fill_ratio = self.get_fill_ratio()
        
        print("=== Bloom Filter Statistics ===")
        print(f"Configuration: n={self.n}, p={self.p:.3f}")
        print(f"Parameters: m={self.m}, k={self.k}")
        print(f"Memory usage: {self.m / 8:.0f} bytes ({self.m / 8 / 1024:.2f} KB)")
        print(f"Elements added: {self.num_elements}")
        print(f"Fill ratio: {fill_ratio:.3f} ({sum(self.bit_array)}/{self.m} bits set)")
        print(f"Expected FP rate: {self.p:.3f}")
        print(f"Current FP rate: {current_fp:.3f}")
        if self.num_elements > 0:
            print(f"Load factor: {self.num_elements / self.n:.2f}")