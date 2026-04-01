import math
import random

from test_file_lib import *

def generate_problem(width, height, node_count_range, dest_count_range, spanning_tree_selection_range, extra_edge_range, max_added_distance):
    nodes = []

    def make_node(name):
        new_node = None

        while new_node == None:
            new_node = GraphNode(
                    name,
                    random.randrange(width) + 1,
                    random.randrange(height) + 1,
                    )

            for other_node in nodes:
                if other_node.x == new_node.x and other_node.y == new_node.y:
                    new_node = None
                    break

        nodes.append(new_node)

        return new_node

    for i in range(1, random.choice(node_count_range)):
        make_node(i)

    destinations = random.sample(nodes, random.choice(dest_count_range))

    for dest in destinations:
        dest.is_destination = True

    origin = make_node(len(nodes) + 1)
    origin.is_origin = True

    not_in_tree = nodes.copy()
    not_in_tree.remove(origin)

    def edge_between(node_from, node_to):
        new_edge = Edge(node_from,
                    node_to,
                    math.ceil(
                        math.dist((node_from.x, node_from.y), (node_to.x, node_to.y)) +
                        random.randrange(max_added_distance)
                        )
                    )

        node_from.edges.append(new_edge)

    def spanning_tree(branch):
        nonlocal not_in_tree

        new_tree_nodes = random.sample(not_in_tree, min(random.choice(spanning_tree_selection_range), len(not_in_tree)))

        not_in_tree = [n for n in not_in_tree if n not in new_tree_nodes]

        for next_node in new_tree_nodes:
            edge_between(branch, next_node)
            spanning_tree(next_node)

        not_next_tree_nodes = [n for n in nodes if n not in new_tree_nodes and n != branch]

        for next_node in random.sample(not_next_tree_nodes, min(random.choice(extra_edge_range), len(not_next_tree_nodes))):
            edge_between(branch, next_node)

    spanning_tree(origin)

    return (origin, destinations, nodes)

for i in range(0, 1000):
    print("\n====== TEST ======\n")
    print(to_test_file(*generate_problem(10, 10, range(4, 13), range(1, 3), range(1, 4), range(0, 3), 4)))
