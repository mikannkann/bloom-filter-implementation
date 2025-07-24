# Python Bloom Filter

A clean and efficient Python implementation of Bloom Filter with automatic parameter optimization.

## Features

- **Optimal Parameters**: Automatic calculation of bit array size and hash function count
- **Zero False Negatives**: Guaranteed no false negative results
- **Performance Statistics**: Built-in monitoring and analysis tools
- **Clean Implementation**: Well-documented, readable code
- **Example Demos**: Comprehensive usage examples and performance tests

## Installation & Usage

### Quick Start

```bash
git clone https://github.com/mikannkann/bloom-filter-implementation.git
cd bloom-filter-implementation
python examples/basic_demo.py
```

### Basic Usage

```python
from bloomfilter import SimpleBloomFilter

# Create filter: capacity=1000, false positive rate=1%
bf = SimpleBloomFilter(capacity=1000, false_positive_probability=0.01)

# Add elements
bf.add("apple")
bf.add("banana")

# Check membership
print("apple" in bf)      # True (definitely exists)
print("grape" in bf)      # False (definitely does not exist)
print("unknown" in bf)    # True/False (may be false positive)

# View statistics
bf.print_stats()
```

## Implementation Details

### Automatic Parameter Optimization

The filter automatically calculates optimal parameters:

```python
# Optimal bit array size
m = int(math.ceil(-n * math.log(p) / (math.log(2)**2)))

# Optimal number of hash functions  
k = int(math.ceil((m / n) * math.log(2)))
```

### Core Algorithm

```python
def contains(self, item):
    """Zero false negatives guaranteed"""
    hashes = self._get_hashes(item)
    for h_index in hashes:
        if not self.bit_array[h_index]:
            return False  # Definitely not in set
    return True  # Possibly in set
```

## Examples

- `examples/basic_demo.py` - Basic operations
- `examples/false_positive_demo.py` - False positive demonstration  
- `examples/large_scale_test.py` - Performance verification

## Performance

For 1,000,000 elements:

| Target FP Rate | Memory | Hash Functions |
|----------------|--------|----------------|
| 1%             | 1.2 MB | 7              |
| 0.1%           | 1.8 MB | 10             |
| 0.01%          | 2.4 MB | 13             |

## License

MIT License

## References

- B. H. Bloom. "Space/time trade-offs in hash coding with allowable errors." Communications of the ACM, 1970.

---

*Clean, efficient Bloom Filter implementation for educational and practical use.*
