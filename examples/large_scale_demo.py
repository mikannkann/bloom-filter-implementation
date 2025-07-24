#!/usr/bin/env python3
"""
Large Scale Performance and Statistical Validation

Tests Bloom filter performance with large datasets and validates
theoretical vs actual false positive rates across different configurations.
"""

import sys
from pathlib import Path
import random
import time
import string
from typing import List, Tuple

# 親ディレクトリのモジュールをインポート
sys.path.insert(0, str(Path(__file__).parent.parent))
from bloomfilter import SimpleBloomFilter


def generate_random_strings(count: int, length: int = 10) -> List[str]:
    """Generate random strings for testing."""
    chars = string.ascii_letters + string.digits
    return [''.join(random.choices(chars, k=length)) for _ in range(count)]


def performance_test():
    """Test insertion and lookup performance with large datasets."""
    print("=== Performance Test ===")
    
    # Large filter configuration
    capacity = 100000
    fp_prob = 0.001
    bf = SimpleBloomFilter(capacity=capacity, false_positive_probability=fp_prob)
    
    print(f"Filter config: n={capacity}, p={fp_prob}, m={bf.m}, k={bf.k}")
    print(f"Memory usage: {bf.m / 8 / 1024:.1f} KB")
    
    # Generate test data
    print(f"\nGenerating {capacity} random strings...")
    start_time = time.time()
    test_items = generate_random_strings(capacity)
    generation_time = time.time() - start_time
    print(f"Data generation: {generation_time:.2f} seconds")
    
    # Insertion performance
    print(f"\nInserting {capacity} items...")
    start_time = time.time()
    for item in test_items:
        bf.add(item)
    insertion_time = time.time() - start_time
    
    print(f"Insertion time: {insertion_time:.2f} seconds")
    print(f"Insertion rate: {capacity / insertion_time:.0f} items/second")
    
    # Lookup performance (positive cases)
    print(f"\nTesting {capacity} lookups (all should be found)...")
    start_time = time.time()
    found_count = sum(1 for item in test_items if bf.contains(item))
    lookup_time = time.time() - start_time
    
    print(f"Lookup time: {lookup_time:.2f} seconds")
    print(f"Lookup rate: {capacity / lookup_time:.0f} items/second")
    print(f"Found: {found_count}/{capacity} (should be {capacity})")
    
    return bf, test_items


def statistical_validation():
    """Validate theoretical vs actual false positive rates."""
    print("\n=== Statistical Validation ===")
    
    test_configs = [
        (1000, 0.1),    # High FP rate
        (5000, 0.01),   # Medium FP rate  
        (10000, 0.001), # Low FP rate
    ]
    
    test_sample_size = 10000
    
    print(f"Testing with {test_sample_size} random samples per configuration")
    print("Config       | Expected FP | Actual FP | Difference | Memory")
    print("-" * 60)
    
    for capacity, expected_fp in test_configs:
        bf = SimpleBloomFilter(capacity=capacity, false_positive_probability=expected_fp)
        
        # Fill filter to capacity
        for i in range(capacity):
            bf.add(f"real_item_{i}")
        
        # Test with random strings (should not be in filter)
        test_items = generate_random_strings(test_sample_size, length=15)
        false_positives = sum(1 for item in test_items if bf.contains(item))
        actual_fp = false_positives / test_sample_size
        
        difference = abs(actual_fp - expected_fp)
        memory_kb = bf.m / 8 / 1024
        
        print(f"n={capacity:5d} p={expected_fp:.3f} | {expected_fp:10.3f} | "
              f"{actual_fp:8.3f} | {difference:9.3f} | {memory_kb:6.1f} KB")


def capacity_stress_test():
    """Test behavior when exceeding designed capacity."""
    print("\n=== Capacity Stress Test ===")
    
    capacity = 1000
    fp_prob = 0.01
    bf = SimpleBloomFilter(capacity=capacity, false_positive_probability=fp_prob)
    
    print(f"Filter designed for {capacity} items with {fp_prob} FP rate")
    
    # Test at different load factors
    load_factors = [0.5, 1.0, 1.5, 2.0]
    test_sample_size = 1000
    
    print("Load Factor | Items Added | Actual FP Rate | Degradation")
    print("-" * 55)
    
    for load_factor in load_factors:
        # Create fresh filter for each test
        test_bf = SimpleBloomFilter(capacity=capacity, false_positive_probability=fp_prob)
        
        items_to_add = int(capacity * load_factor)
        
        # Add items
        for i in range(items_to_add):
            test_bf.add(f"item_{i}")
        
        # Test false positive rate
        test_items = generate_random_strings(test_sample_size, length=12)
        false_positives = sum(1 for item in test_items if test_bf.contains(item))
        actual_fp = false_positives / test_sample_size
        
        degradation = actual_fp / fp_prob
        
        print(f"{load_factor:10.1f} | {items_to_add:10d} | {actual_fp:13.3f} | "
              f"{degradation:10.1f}x")


def main():
    """Run comprehensive performance and statistical tests."""
    print("Starting large scale Bloom filter testing...\n")
    
    # Performance testing
    bf, test_items = performance_test()
    
    # Statistical validation
    statistical_validation()
    
    # Capacity stress testing
    capacity_stress_test()
    
    print(f"\n=== Final Filter Statistics ===")
    bf.print_stats()
    
    print("\nTesting completed successfully!")


if __name__ == "__main__":
    # Set random seed for reproducible results
    random.seed(42)
    main()
