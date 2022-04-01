# Hash Maps

## Introduction

The hash map data structure allows for efficient lookups of key value pairs. A
hash function is used to compute indices which are placed into buckets in a hash
table. Ideally, the selected hash function will place each key in a unique
bucket. Though *hash collisions* will occur and need to be handled. The average
cost of lookup is independent of the number of indices.

### Hashing

Hashing distributes keys across an array buckets. The choice of hash function
is an important aspect of hash map implementations. Though, this document will
dive into the details of the hash function choice since it varies from
language to language.

### Load Factor

Load factor is defined as:

$$\textrm{load_factor} = \frac{n}{k}$$

Where $n$ is the number of entries and $k$ is the number of buckets. As the load
factor grows larger, the hash table becomes slower. Generally, load factor is
used in dynamically sized hash tables to know when we should resize the table.

## Implementation Choices

There are two main implementation options for hash tables which each resolve
collisions slightly differently:

- [Open addressing](https://en.wikipedia.org/wiki/Open_addressing)
- [Separate Chaining](https://en.wikipedia.org/wiki/Hash_table#Separate_chaining)

This particular implementation uses:

- Open addressing
- [Linear probing](https://en.wikipedia.org/wiki/Linear_probing)
- [Tombstone deletion](https://en.wikipedia.org/wiki/Tombstone_(data_store))

### Separate Chaining

Separate chaining uses a core data structure of two components:

- Main bucket array list
- Component linked lists

At each index in the main bucket array list is a linked list. When two keys in
the hash table index to the same bucket, we simply append to the node's linked
list so that the key can be found on lookup.

On deletion, we simply remove the linked list node in question.

The main drawback of this approach is caching since the nodes of the linked list
are likely not nearby each other in physical memory thereby not making full use
of the CPU Cache.

### Open Addressing

Open Addressing follows an approach where the hash table is composed of an
array known as a bucket array. If two keys map to the same index in the bucket
array, we use a deterministic probing strategy to find a new bucket in the
bucket array to insert the key-value pair. There are a couple of common probing
strategies:

- Linear probing: look sequentially for indices until you find an open bucket
- Quadratic probing: use a quadratic function to find the index of the next
open bucket
- Double hashing: use a main hashing function to find the first index and use
a secondary hashing function times an incrementer to find an open bucket

Each of these different strategies evolved to solve the clustering problem in
open addressing hash tables. The clustering problem is most obvious in linear
addressing where a cluster is defined as a group of nodes that grows due to
hash collisions. One can only find a key from this "cluster" through linear
search which is not as efficient.

In terms of lookups, one uses the deterministic probing strategy to iterate
through the bucket array until we find a key or an empty bucket whereby we know
that the key does not exist. In the case of a fixed size hash map that is full
we also need to check if we have exceeded the hash map size since we will not
find an empty bucket array.

There are a couple of strategies for deletion:

- tombstone deletion
- [backward shift deletion](https://codecapsule.com/2013/11/17/robin-hood-hashing-backward-shift-deletion/)

With tombstone deletion, we just mark a slot as deleted and allow it to be
replaced. This means that we skip past it when applying a probing strategy. A
drawback of this approach is if reach a large number of tombstones, lookups are
slowed down.

With backward shift deletion, we move items that were added as a result of a
collision one slot backward.
