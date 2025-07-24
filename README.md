# Simple Bloom Filter Implementation

A space-efficient probabilistic data structure for membership testing in Python, featuring automatic parameter optimization and comprehensive performance monitoring.

## Features

- **Zero False Negatives**: Guaranteed accurate negative results - if the filter says an item is not present, it definitely isn't
- **Automatic Parameter Optimization**: Calculates optimal bit array size and hash function count based on capacity and false positive probability
- **MD5-based Hashing**: Uses MD5 with seeds for multiple independent hash functions
- **Performance Statistics**: Monitoring of false positive rates, fill ratios, and memory usage

## Quick Start

```bash
git clone https://github.com/mikannkann/bloom-filter-implementation.git
cd bloom-filter-implementation
python examples/basic_demo.py
```

## Usage

### Basic Operations

```python
from bloomfilter import SimpleBloomFilter

# Create filter: capacity=100, false positive rate=1%
bf = SimpleBloomFilter(capacity=100, false_positive_probability=0.01)

# Add elements
bf.add("apple")
bf.add("banana")

# Check membership (two equivalent ways)
print("apple" in bf)        # True (definitely exists)
print(bf.contains("apple")) # True (definitely exists)
print("grape" in bf)        # False (definitely not in set)

# View detailed statistics
bf.print_stats()
```

### Statistics Output Example

```
=== Bloom Filter Statistics ===
Configuration: n=100, p=0.010
Parameters: m=958, k=7
Memory usage: 120 bytes (0.12 KB)
Elements added: 3
Fill ratio: 0.022 (21/958 bits set)
Expected FP rate: 0.010
Current FP rate: 0.000
Load factor: 0.03
```

## Implementation Details

### Parameter Calculation

The filter uses optimal formulas from Bloom's original paper:

```python
# Optimal bit array size
m = int(-n * math.log(p) / (math.log(2) ** 2))

# Optimal number of hash functions
k = int((m / n) * math.log(2))
```

Where:
- `n` = expected number of elements (capacity)
- `p` = desired false positive probability
- `m` = number of bits in the filter
- `k` = number of hash functions

### Hash Function Implementation

```python
def _hash(self, item, seed):
    """Generate hash using MD5 with seed for variation"""
    hash_input = f"{str(item)}_{seed}".encode('utf-8')
    hash_value = int(hashlib.md5(hash_input).hexdigest(), 16)
    return hash_value % self.m
```

### Core Membership Test

```python
def contains(self, item):
    """Test membership with zero false negatives"""
    for i in range(self.k):
        index = self._hash(item, i)
        if not self.bit_array[index]:
            return False  # Definitely not in set
    return True  # Possibly in set (may be false positive)
```

## Class Reference

### SimpleBloomFilter

#### Constructor
- `SimpleBloomFilter(capacity: int, false_positive_probability: float)`

#### Methods
- `add(item: Union[str, int])` - Add an item to the filter
- `contains(item: Union[str, int]) -> bool` - Test membership
- `__contains__(item)` - Support for `in` operator
- `get_current_false_positive_probability() -> float` - Calculate actual FP rate
- `get_fill_ratio() -> float` - Get ratio of set bits
- `print_stats()` - Display comprehensive statistics

#### Properties
- `n` - Expected capacity
- `p` - Target false positive probability  
- `m` - Bit array size
- `k` - Number of hash functions
- `num_elements` - Current number of added elements

## Examples

### 1. Basic Operations (`examples/basic_demo.py`)
Demonstrates initialization, adding elements, and membership testing with clear output.

### 2. False Positive Analysis (`examples/false_positive_demo.py`)
Shows how false positive rates behave in practice and validates theoretical predictions.

### 3. Performance Testing (`examples/large_scale_demo.py`)
Large-scale performance analysis with timing measurements and statistical validation.

## Performance Characteristics

Theoretical performance for 100,000 elements:

| Target FP Rate | Bit Array Size | Hash Functions | Memory Usage |
|----------------|----------------|----------------|--------------|
| 1%             | 958,506 bits   | 7              | 117.3 KB     |
| 0.1%           | 1,437,759 bits | 10             | 176.0 KB     |
| 0.01%          | 1,917,012 bits | 13             | 234.6 KB     |

## Project Structure

```
bloom-filter-implementation/
├── bloomfilter.py           # Main implementation
├── examples/
│   ├── basic_demo.py        # Basic usage demonstration
│   ├── false_positive_demo.py # False positive analysis
│   └── large_scale_demo.py  # Performance testing
├── LICENSE                  # MIT License
└── README.md               # This file
```

## License

MIT License - see [LICENSE](LICENSE) file for details.

## References

- Bloom, B. H. (1970). "Space/time trade-offs in hash coding with allowable errors." *Communications of the ACM*, 13(7), 422-426.

---

*Educational implementation of Bloom filters with focus on clarity and correctness.*
