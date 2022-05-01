"""Tests for graph.py"""


def test_basic():
    from datastructures import SimpleGraph

    # Ground Truth Source: https://stackabuse.com/dijkstras-algorithm-in-python/
    graph = SimpleGraph(9)
    graph.set_edge_weight(0, 1, 4)
    graph.set_edge_weight(0, 6, 7)
    graph.set_edge_weight(1, 6, 11)
    graph.set_edge_weight(1, 7, 20)
    graph.set_edge_weight(1, 2, 9)
    graph.set_edge_weight(2, 3, 6)
    graph.set_edge_weight(2, 4, 2)
    graph.set_edge_weight(3, 4, 10)
    graph.set_edge_weight(3, 5, 5)
    graph.set_edge_weight(4, 5, 15)
    graph.set_edge_weight(4, 7, 1)
    graph.set_edge_weight(4, 8, 5)
    graph.set_edge_weight(5, 8, 12)
    graph.set_edge_weight(6, 7, 1)
    graph.set_edge_weight(7, 8, 3)

    # ground truth of distance from 0 to the node at the index 0 through 8
    dist_ground_truth = [0, 4, 11, 17, 9, 22, 7, 8, 11]
    # the previous nodes from the target node at the specific index (e.g. the
    # previous node to get from 0 to 2 is 4
    prev_ground_truth = [None, 0, 4, 2, 7, 3, 0, 6, 7]
    # the optimal node path from node 0 to node 5
    zero_to_five_ground_truth = [0, 6, 7, 4, 2, 3, 5]

    dist, prev = graph.dijkstra_path(0)
    assert dist == dist_ground_truth
    assert prev == prev_ground_truth

    zero_to_five = graph.shortest_path(0, 5, prev)
    assert list(zero_to_five) == zero_to_five_ground_truth


def test_circular_graph_with_longer_direct_path():
    from datastructures import SimpleGraph

    graph = SimpleGraph(8)
    graph.set_edge_weight(0, 1, 1)
    graph.set_edge_weight(1, 2, 1)
    graph.set_edge_weight(2, 3, 1)
    graph.set_edge_weight(3, 4, 1)
    graph.set_edge_weight(4, 5, 1)
    graph.set_edge_weight(5, 6, 1)
    graph.set_edge_weight(6, 7, 1)
    graph.set_edge_weight(0, 7, 10)

    dist, prev = graph.dijkstra_path(0)

    ground_truth_path = [0, 1, 2, 3, 4, 5, 6, 7]

    # path to node 7 takes a total weight of 7
    assert dist[7] == 7

    zero_to_seven = graph.shortest_path(0, 7, prev)

    assert list(zero_to_seven) == ground_truth_path


def test_circular_graph_with_shorter_direct_path():
    from datastructures import SimpleGraph

    graph = SimpleGraph(8)
    graph.set_edge_weight(0, 1, 1)
    graph.set_edge_weight(1, 2, 1)
    graph.set_edge_weight(2, 3, 1)
    graph.set_edge_weight(3, 4, 1)
    graph.set_edge_weight(4, 5, 1)
    graph.set_edge_weight(5, 6, 1)
    graph.set_edge_weight(6, 7, 1)
    graph.set_edge_weight(0, 7, 6)

    dist, prev = graph.dijkstra_path(0)

    # the direct path is shorter compared to the previous test case
    ground_truth_path = [0, 7]

    # path to node 7 takes a total weight of 6
    assert dist[7] == 6

    zero_to_seven = graph.shortest_path(0, 7, prev)

    assert list(zero_to_seven) == ground_truth_path


def test_negative_path_failure():
    from datastructures import SimpleGraph

    # if there is a negative weight cycle, there is no shortest path
    # dijkstra finds a path due to the greedy nature of the algorithm, but in
    # reality there should be no shortest path returned, or an "infinite path"
    # (to solve this problem, you need to use the bellman-ford algorithm)
    # dijkstra assumes that any path going out from the source is monotonically
    # increasing
    # in this graph the path from 0 to 5 is -infinity
    graph = SimpleGraph(6)
    graph.set_edge_weight(0, 1, 1)
    graph.set_edge_weight(1, 2, 1)
    graph.set_edge_weight(2, 3, -5)
    graph.set_edge_weight(3, 4, 1)
    graph.set_edge_weight(1, 4, 1)
    graph.set_edge_weight(1, 5, 1)
    graph.set_edge_weight(0, 5, 1)

    dist, prev = graph.dijkstra_path(0)

    # the actual shortest path from 0 to 5 is [0, 1, 2, 3, 4, 1, 5] (if you can
    # use each edge only once, otherwise, it is -infinity with a loop around
    # [1, 2, 3, 4] which has a cumulative weight of -1. Each time you go around
    # you get more negative which is why it is "optimal" to keep going around
    ground_truth_dist = [0, 1, 2, -3, 2, 1]
    assert dist == ground_truth_dist

    ground_truth_path = [0, 5]
    zero_to_five = graph.shortest_path(0, 5, prev)
    assert list(zero_to_five) == ground_truth_path


def test_directed_graph():
    from datastructures import SimpleGraph

    # Same as a test above, except now it's directed, this should not change the
    # result at least in this case for the graph
    graph = SimpleGraph(8)
    graph.set_edge_weight(0, 1, 1, True)
    graph.set_edge_weight(1, 2, 1, True)
    graph.set_edge_weight(2, 3, 1, True)
    graph.set_edge_weight(3, 4, 1, True)
    graph.set_edge_weight(4, 5, 1, True)
    graph.set_edge_weight(5, 6, 1, True)
    graph.set_edge_weight(6, 7, 1, True)
    graph.set_edge_weight(0, 7, 6, True)

    dist, prev = graph.dijkstra_path(0)

    # the direct path is shorter compared to the previous test case
    ground_truth_path = [0, 7]

    # path to node 7 takes a total weight of 6
    assert dist[7] == 6

    zero_to_seven = graph.shortest_path(0, 7, prev)

    assert list(zero_to_seven) == ground_truth_path
