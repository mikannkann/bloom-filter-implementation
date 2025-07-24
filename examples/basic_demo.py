#!/usr/bin/env python3
"""
Basic Bloom Filter Operations Demo

Demonstrates fundamental operations: initialization, adding elements,
and testing membership with clear examples.
"""

import sys
from pathlib import Path

# 親ディレクトリのモジュールをインポート
sys.path.insert(0, str(Path(__file__).parent.parent))
from bloomfilter import SimpleBloomFilter


def main():
    """Basic operations demonstration: add, contains, and property queries."""
    print("=== Basic BloomFilter Operations Demo ===")
    
    # 予想される要素数 n=100、目標偽陽性確率 p=0.01 (1%) でブルームフィルタを初期化
    bf = SimpleBloomFilter(capacity=100, false_positive_probability=0.01)
    print(f"BloomFilter initialized: n={bf.n}, p={bf.p}, m={bf.m}, k={bf.k}")
    print(f"Memory usage: {bf.m / 8 / 1024:.2f} KB\n")
    
    # 要素の追加
    items_to_add = ["apple", "banana", "orange"]
    print(f"Adding items: {items_to_add}")
    for item in items_to_add:
        bf.add(item)
    
    # 存在する要素の検索
    print(f"\nTesting items that were added:")
    for item in items_to_add:
        result = bf.contains(item)
        print(f"'{item}': {'Found' if result else 'Not found'}")
    
    # 存在しない要素の検索
    test_items = ["grape", "strawberry", "kiwi"]
    print(f"\nTesting items that were NOT added:")
    for item in test_items:
        result = bf.contains(item)
        print(f"'{item}': {'Found (False Positive!)' if result else 'Not found'}")
    
    # 統計情報の表示
    print()
    bf.print_stats()


if __name__ == "__main__":
    main()
