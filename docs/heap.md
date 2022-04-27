# Heap

## Introduction

The **heap** is a data structure that efficiently stores the maximum or minimum
of as set of values. The heap efficiently implements the _abstract data type_
called a _priority queue_.

## Binary Heap

The most common type of heap is the **binary heap** which takes the form of a
_binary tree_ which maintains the **heap property**. In a max heap, for example,
the heap property holds that for all parent nodes, each child node is strictly
less than or equal to its parent.

<!-- markdownlint-capture -->
<!-- markdownlint-disable -->
<img src="https://upload.wikimedia.org/wikipedia/commons/c/c4/Max-Heap-new.svg" width="50%" alt="Max Heap">
<!-- markdownlint-restore -->

Note that a [fibonacci heap](https://en.wikipedia.org/wiki/Fibonacci_heap) has a
better _amortized_ runtime complexity on insert and decrease-key.

### Implementation

For ease of implementation, the binary heap is usually constructed as an _almost
complete binary tree_. In an almost complete binary tree, for all levels except
for the last one, the parents have two children. If the last level is not full,
the nodes must be ordered left to right. We chose to hold the almost complete
binary tree property to maintain good runtime asymptotics. In the worst case,
a normal binary tree can degenerate to a linked list which has $O(n)$ insertion
and deletion run times. Whereas, a complete binary tree has $O(\log(n))$
insertion and deletion runtimes. Additionally, a complete binary tree is easier
to store as a flat array.

We can make sense of the flat array using the following three formulas which
give us the relationships between parent, left child, and right child. Note that
// is the integer division symbol.

* left child: $2 * \textrm{index} + 1$
* right child: $2 * \textrm{index} + 2$
* parent: $(\textrm{index} - 1) // 2$

This particular implementation defines both a max and min heap. The Binary Tree
is implemented as a separate class and the nodes store key, value pairs where
the keys represent the priority of the value. We factor out the common methods
between the min and max heap in an abstract class called `BaseHeap`. There are
five main methods that aid in this implementation. Their explanations refer
specifically to the max heap implementation:

* `_sift_up`
* `_sift_down`
* `insert`
* `extract_root`
* `heapify`

The `_sift_up` method sends nodes up the tree until the heap property is met.
Given a node index, the method swaps parent with child if the node's parent
fails to meet the heap property. This repeats until the heap property is met
for a parent child pair, or we reach the root node.

The `_sift_down` method sends nodes down the tree until the heap property is met.
Given an index, the method determines the largest (in a max heap) among trio of
parent, left child, and right child. If the largest is the parent, the algorithm
does nothing and exits. Otherwise, the parent is swapped with the largest item
(either the left or right child) and is recursively called on the new child.

The `insert` method adds a new node to the next open slot on the bottom of the
binary tree. It then calls `_sift_up` on this node. This method has a worst-case
time complexity of $O(\log(n))$.

The `extract_root` method stores the value of the root node (the max value) and
then swaps the root with the last element (last node on last row) This node is
then popped. Lastly, we call `_sift_down` on the root node. This method has a
worst-case time complexity of $O(\log(n))$.

The `heapfiy` method allows for the efficient creation of the binary heap
without the use of repeated inserts. It iterates over the list of new elements
starting at the parent of the last child and proceeds backward. On each of
these nodes, `_sift_down` is called. This iteratively builds sorted sub-trees
in the binary tree, working its way up. The runtime for this algorithm is
$O(n)$. This may be counter-intuitive, but the intuition follows from the fact
that we avoid duplicated work by working our way up the tree and each level has
to swap at most $h-1$ times. The proof is a bit more involved and requires an
infinite sum.

![Heapify Node Order](https://i.imgur.com/Oz3PlVY.png)

This implementation also supports changing the key (priority) of the nodes. In
the max heap if we want to increase the priority of a node, we update the key
and then call `_sift_up`. If we can to decrease the priority, we update the key
and then call `_sift_down`. The min heap implementation reverses the calls to
sift up and down.

Lastly, the implementation also provides a `heapsort` function that makes use of
the heap data structure. The canonical implementation of heapsort is an in-place
algorithm. It has the following steps:

* First run `heapify` on the array
* Set the variable `end` to `count - 1`
* Now in a loop while `end > 0`
  * Swap the root with the first element (the max)
  * Set `end` to `end - 1`
  * Run `_sift_down` on the all indices from 0 to `end`

This has a runtime of $O(n \log(n))$. Although `heapify` runs in $O(n)$, we
still need to run `_sift_down` $n$ times to extract the maxes. In our source
code, we choose not to adhere to the in place max extraction for ease of
implementation. Also, note that heap sort is not a stable sorting algorithm
because it does not maintain the relative order of elements after sorting. In
other words, when two items have the same key, it is an implementation detail as
to which order they will end up.

## Priority Queue

In this implementation, the priority queue simply extends the min heap
implementation adding item lookup by value. This enables the changing of
item priority only referring to it's value rather than its index. This
particular implementation detail is required for dijkstra's algorithm.

We achieve the above through the use of a dictionary that maps values to
indices. This has the drawback of requiring that values inserted into the
priority queue are unique. This tracking adds no overhead in terms of big O
complexity but does incur and $O(n)$ runtime overhead cost for the n inserts of
values into the look-up table.
