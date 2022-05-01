# Binary Tree

A binary tree is a common data structure that extends from a root node with
each node having at most two children.

## Implementation

This particular binary tree was implemented using a flat array since the heap
data structure that extends it holds the "almost complete" binary tree property.

Given an index:

* left child: $2 * \textrm{index} + 1$
* right child: $2 * \textrm{index} + 2$
* parent: $(\textrm{index} - 1) // 2$

## Traversal

There are two main methods of binary tree traversal: breadth first traversal
and depth first traversal.

### Breadth First Traversal (BFT)

Breadth first traversal follows each tree level in successive order. Breadth
first traversal is the only method that is feasible for infinite trees. Breadth
first traversal can also be used to determine if a graph is bi-partite.

The breadth first order of the nodes follows as in the below figure. The node
order is F, B, G, A, D, I, C, E, and H.

![Breadth First Traversal](https://upload.wikimedia.org/wikipedia/commons/thumb/d/d1/Sorted_binary_tree_breadth-first_traversal.svg/220px-Sorted_binary_tree_breadth-first_traversal.svg.png)

#### BFT Implementation

* Highlights
  * Queue to track nodes
  * Set to track explored nodes
  * Implements visited set tracking (though it's not needed for trees)

It makes most sense to implement breadth first traversal iteratively instead of
recursively. In the iterative implementation, we need to use extra memory in the
form of a queue. The queue tracks the children of the nodes as we encounter them
while maintaining the order of their discovery. When adding the children to the
queue, we add them left to right. Breadth first traversal can also be
generalized to graphs as long as we track which nodes we have already visited.
The average runtime complexity of breadth first traversal can be thought of as
$O(|v|+|e|)$ where $v$ is the number of vertices in the graph and $e$ is the
number of edges in the graph. Though in the worst case $|e| = |v|^2$ for a fully
connected graph which results in a worst-case runtime complexity of $O(|v|^2)$.
When dealing with just trees, we can drop the $|E|$ term since $E = V-1$. The
space complexity is $O(w)$ where $w$ is the maximum width of the binary tree.
For generic graphs, the space complexity varies.

### Depth First Traversal (DFT)

Depth first traversal follows the children of the nodes in successive order
rather than the levels, as in breadth first traversal. The order of the nodes
depends on the type of depth first traversal. There are three main types:

* Pre-order (node, left, right)
* In-order (left, node, right)
* Post-order (left, right, node)

![Binary Tree Traversal](https://upload.wikimedia.org/wikipedia/commons/7/75/Sorted_binary_tree_ALL_RGB.svg)

In the above diagram, here are the node orders (source: wikipedia)

Pre-order (node visited at position red 🔴): F, B, A, D, C, E, G, I, H

In-order (node visited at position green 🟢): A, B, C, D, E, F, G, H, I

Post-order (node visited at position blue 🔵): A, C, E, D, B, H, I, G, F

Of the three, pre-order traversal is the most common depth first traversal
method. The pre-order traversal method is considered a topological sort of the
nodes. An alternative algorithm to find the topological sort is (Kahn's
algorithm) The post-order traversal is sometimes useful to get the postfix
expression of a binary expression tree. (a+b into ab+) Postfix notation is
preferred for compilers and calculators because it is easy to process
left-to-right. Additionally, there are less common reverse variants of each of
these node orders which you may come across.

#### DFT Implementation

Depth first traversal, in contrast to breadth first traversal can be implemented
both iteratively and recursively. Generally, we would rather implement the
algorithm iteratively to avoid stack overflows unless we know the graphs we are
exploring are relatively small. The iterative implementation of depth first
travel uses a stack and the recursive implementation uses the "call stack" as
its implicit stack to track the order of the nodes. An important note is that
we need to **add the nodes in the reverse order to the stack** so that they are
processed in the correct order since the stacks are first in first out.

In our particular approach, we use a pre-order depth first traversal
implementation. In fact, there are only two differences between the breadth
first traversal implementation:

* Uses a stack instead of a queue
* Appends right then left instead of left then right

The time complexity of depth first traversal is the same as breadth first
traversal. Though, the space complexity is $O(d)$ where $d$ is the maximum
depth of the binary tree.

The implementation for in-order and post-order traversal is a slightly more
involved and requires tracking additional variables.
