# Hash Maps
## Introduction
In its most basic form, hash maps map keys to values. A hash function is used to compute indices which are placed into buckets in a hash table.  
Ideally, the selected hash function will place each key in a unique bucket. Though *hash collisions* will occur and need to be handled. The average cost of lookup is independent of the number of indices.

## Hashing
Hashing distributes keys across an array buckets. Where f(k, array_size) is a hashing function where:  
_index_ = f(_key_, _array_size_).

## Load Factor
Load factor is defined as:  
_load_factor_ = _n_/_k_  
Where n is the number of entries and k is the number of buckets. As the load factor grows larger, the hash table becomes slower.

## Open Addressing
Due to the birthday paradox, hash collisions are nearly unavoidable. Open addressing is one method to resolve collisions between hashes.

Hash collisions are resolved by a method known as *probing*: search through the array until the target record is found or an unused memory slot is found. Known probing sequences include:
* *Linear probing*: fixed probing interval
* *Quadratic probing*: the interval between probes linearly increases
* *Double hashing*: interval for probing is fixed but computed by another hash function

Linear probing has the best caching performance but struggles with clustering. Double hashing is computationally intensive but has no clustering issues. Quadratic is in between both.

## Specific Implementation
This specific implementation was built in Python. The author made sure to not use primitive dictionaries in any way including in the construction of classes which used slots instead of the primitive dictionary form. The author used open addressing to solve the hash collision issues and used the implementation provided in Knuth Vol. 2 to address this challenge. The specific implementation also used probing was used linear probing during insertion

### Testing the implementation
Run `$ ./tests.py ` in terminal to run through the unit tests. To manually use the class

```python

from datastructures import FixedHashMap
from datastructures.FixedHashMap
```

## Sources
* [https://en.wikipedia.org/wiki/Hash_table](https://en.wikipedia.org/wiki/Hash_table)
* [https://en.wikipedia.org/wiki/Linear_probing](https://en.wikipedia.org/wiki/Linear_probing)
