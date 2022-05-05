# Graph

## Terminology

A graph is a data structure that consists of nodes and edges. A connected graph
is one such that there are no disconnected nodes. A directed graph is one where
the edges connecting nodes have a direction. A weighted graph stores a specific
weight for each of the edges. An adjacency matrix compactly stores the
information required to construct a graph. The matrix is square and each index
represents a connection from the row index node to the column index node. For
an undirected, the matrix is additionally symmetric (A^T = A).

## Shortest Path

Finding the shortest path between two nodes in the graph is an often interesting
and useful problem. Dijkstra's algorithm solves this problem under a couple of
constraints. First, the graph must have edge weights that are positive. And,
second it depends on the min priority queue data structure. Thus, the algorithm
depends on the runtime guarantees of the min priority queue implementation.

Additionally, there are two main variants of Dijkstra's algorithm. The first
variant simply finds the shortest path between a source and a target whereas the
more general version computes the shortest paths between a source and all other
target nodes.

### Intuition

Dijkstra is a greedy algorithm which means that it makes the locally optimal
choice at each stage. As the algorithm traverses nodes, it prioritizes exploring
the nodes with the smallest weighted sum without regard for the "directionality"
towards a target, for example. It does this prioritization using the priority
queue. As it traverses the graph iterating over the nodes in order of priority,
it marks them as explored so as not to re-explore nodes it has already visited.

### Implementation

The canonical implementation of Dijkstra's algorithm uses a binary heap that
explores all the node distances from the input start node. This implementation
follows that approach. There are variants of Dijkstra's algorithm that work in
an online fashion without the need for an adjacency matrix. Our implementation
uses an approach where the adjacency matrix is known ahead of time.

We first initialize the `dist` and `prev` arrays by filling them with
`float('inf')` and `None` respectively matching the length of the number of
nodes in the adjacency matrix. The source node's dist is set to `0`--we are
already there so no distance. The indices of the nodes correspond to their
location in the adjacency matrix. We then fill the min priority queue with
values representing indices of nodes and keys representing the *current* value
in the `dist` array. They are all infinity except for source, at this point. We
additionally initialize an empty hash set, `visited`, that corresponds to the
nodes we have explored.

Now while the queue is not empty, we extract the min, `u`, (the source node for
now) and then iterate over each neighbor, `v`, that we have not explored (using
the adjacency matrix). For each `v`, we calculate an alternative distance from
the source node by summing the current shortest distance from `source` to `u`,
`dist[u]`, and the edge weight of `u --> v`, `Graph.Edges(u, v)`. If this `alt`
distance is shorter than the current shortest distance, we update both `dist`
and `prev` for that node index. Additionally, we now have to update the priority
queue with the new priority for that index. We then iterate this process until
we run out of nodes to explore in the graph.

If we are only curious about the shortest path to a target node, then we can
exit the above while loop when `u` is equal to `target`.

Below, follows the pseudocode template of the [wikipedia Dijkstra
implementation](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm#Using_a_priority_queue).
The implementation in `graph.py` follows this pattern.

```text
function Dijkstra(Graph, source):
    dist[source] ← 0                           // Initialization

    create vertex priority queue Q

    for each vertex v in Graph.Vertices:
        if v ≠ source
            dist[v] ← INFINITY                 // Unknown distance from source
                                               // to v
            prev[v] ← UNDEFINED                // Predecessor of v

        Q.add_with_priority(v, dist[v])


    while Q is not empty:                      // The main loop
        u ← Q.extract_min()                    // Remove and return best vertex
        for each neighbor v of u:              // only v that are still in Q
            alt ← dist[u] + Graph.Edges(u, v)
            if alt < dist[v]
                dist[v] ← alt
                prev[v] ← u
                Q.decrease_priority(v, alt)

    return dist, prev
```

To actually get the shortest path, we now have to inspect the `prev` array which
holds the most recent node on the path to the target node. We can use this to
backtrack from a target node to the source using a `deque` where we use the
following wikipedia pseudocode. Essentially, we hop around prev until we find
the target node since each index will point to node that connects its shortest
path.

```text
S ← empty sequence
u ← target
if prev[u] is defined or u = source:          // Do something only if the vertex
                                              // is reachable
    while u is defined:                       // Construct the shortest path
                                              // with a stack S
        insert u at the beginning of S        // Push the vertex onto the stack
        u ← prev[u]                           // Traverse from target to source
```

### Complexity

#### Runtime Complexity

The runtime complexity boils down to the following equation
`O(|E| |decrease-priority(Q)| + |V| |extract-min(Q)|)`

This naturally follows since we will explore every node in the graph, and we
arrive at each of these nodes through the `extract-min` operation, hence
`|V| |extract-min(Q)|`. Additionally, in the worst case we will need to update
the priority of each node in the queue as a result of each edge in the graph,
hence the `|E| |decrease-priority(Q)|`.

Now, the canonical implementation of Dijkstra's algorithm that uses the binary
min-heap has an

```text
O(log(|V|)(|E| + |V|)
```

runtime since both `decrease-key` and `extract-min` have a `log(|V|)` runtime.
But, if you use a fibonacci heap, you can improve the `decrease-key` runtime to
`O(1)` which results in a runtime complexity of `O(|E| + log(|V|)|V|)`. A [post
on stackoverflow](https://stackoverflow.com/a/21066448) covers this in a bit
more detail.

#### Storage Complexity

The storage complexity is also pretty straight forward. We need to maintain a
visited set which is `O(|V|)`. We have the queue itself which is also `O(|V|)`
since it is implemented as an array. The `PriorityQueue` implementation also
maintains an additional value to key lookup for an `O(1)` runtime for
`decrease-priority` so you don't have to traverse the entire tree to find the
value. This also has an `O(|V|)` overhead. Lastly, the `dist` and `prev` arrays
are also `O(|V|)`. Net-net this amounts to an

```text
O(|V|)
```

storage complexity overhead.

### Other Specifics

In our implementation we additionally add the following niceties:

* A graph visualization feature that makes use of `netowrkx` and `graphviz`
* The ability to initialize the adjacency matrix one edge at a time
