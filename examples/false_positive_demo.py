#!/usr/bin/env python3
"""
False Positive Rate Demonstration

Shows how false positive rate increases as the filter approaches capacity,
and demonstrates the probabilistic nature of Bloom filters.
"""

import sys
from pathlib import Path
import random

# 親ディレクトリのモジュールをインポート
sys.path.insert(0, str(Path(__file__).parent.parent))
from bloomfilter import SimpleBloomFilter


def demonstrate_false_positives():
    """Demonstrate false positive behavior with controlled testing."""
    print("=== False Positive Demonstration ===")
    
    # レポートの記述に合わせて小さなフィルタを作成（m=26, n=10, p=0.3）
    bf = SimpleBloomFilter(capacity=10, false_positive_probability=0.3)
    print(f"BloomFilter initialized: n={bf.n}, p={bf.p}, m={bf.m}, k={bf.k}")
    print()
    
    # 人名データを追加（レポートに合わせる）
    added_names = ["Alice", "Bob", "Charlie", "David", "Eve"]
    print("Adding names to the filter:")
    for name in added_names:
        bf.add(name)
        print(f"  Added: {name}")
    
    print()
    
    # 追加した要素の確認
    print("Testing items that were added:")
    for name in added_names:
        result = bf.contains(name)
        print(f"'{name}': {'Found' if result else 'Not found'}")
    
    print()
    
    # 追加していない要素をテスト（偽陽性の確認）
    test_names = ["Frank", "Grace", "Henry", "Iris", "Jack", "Kate", "Leo", "Mia"]
    print("Testing items that were NOT added:")
    false_positives = 0
    
    for name in test_names:
        result = bf.contains(name)
        if result:
            print(f"'{name}': Found (False Positive!)")
            false_positives += 1
        else:
            print(f"'{name}': Not found")
    
    print()
    print(f"Summary: {false_positives}/{len(test_names)} false positives detected")
    
    # 統計情報
    print()
    bf.print_stats()


def main():
    """Run false positive demonstration matching the report description."""
    demonstrate_false_positives()


if __name__ == "__main__":
    main()
