import math
import random

from test_file_lib import *



# SETTINGS:

# the maximum x coordinate; the width of the space
width = 10

# the maximum y coordinate; the height of the space
height = 10

# the total number of nodes (including destinations and the origin) will be randomly drawn from this range
# note that `range(0, x)` means "can be every value between 0 and x, EXCEPT x"
node_count_range = range(4, 21)

# the number of destination nodes will be randomly drawn from this range
# note that `range(0, x)` means "can be every value between 0 and x, EXCEPT x"
dest_count_range = range(1, 5)

# the problem generator uses a spanning tree to ensure that every node has a path to the origin
# the number of nodes that each node will attempt to connect to when forming the spanning tree will be randomly drawn from this range
# note that `range(0, x)` means "can be every value between 0 and x, EXCEPT x"
spanning_tree_selection_range = range(1, 4)

# once the problem generator creates the spanning tree, it allows each node to potentially form random connections with the other nodes
# the number of extra connections that each node can make will be randomly drawn from this range
# note that `range(0, x)` means "can be every value between 0 and x, EXCEPT x"
extra_edge_range = range(0, 3)

# by default, the path cost of each edge is equal to the length of the edge, rounded up
# however, the cost of each edge can be increased by a random amount up to this value
# set this to zero to disable this feature
max_added_distance = 4



def generate_problem(width, height, node_count_range, dest_count_range, spanning_tree_selection_range, extra_edge_range, max_added_distance):
    nodes = []

    # function to create a new node whose coordinates have not yet been claimed by another node
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

    # create a number of nodes according to the specified range
    for i in range(1, random.choice(node_count_range)):
        make_node(i)

    # select a few nodes as destination nodes, according to the range of destination node counts
    destinations = random.sample(nodes, min(random.choice(dest_count_range), len(nodes)))

    for dest in destinations:
        dest.is_destination = True

    # create an origin node
    origin = make_node(len(nodes) + 1)
    origin.is_origin = True

    # create a new array to keep track of the nodes that have not been added to the spanning tree
    not_in_tree = nodes.copy()
    not_in_tree.remove(origin)

    # function to establish an edge between two nodes
    def edge_between(node_from, node_to):
        new_edge = Edge(node_from,
                        node_to,
                        math.ceil(
                            math.dist((node_from.x, node_from.y), (node_to.x, node_to.y)) +
                            random.randrange(max_added_distance + 1)
                            )
                        )

        node_from.edges.append(new_edge)

    # this function starts at the origin and creates a non-looping spanning tree from the origin to all other nodes
    # this ensures that all nodes are reachable from the origin
    # this function also adds a random number of extra connections between nodes to allow for more complex structures to be generated
    def spanning_tree(branch):
        nonlocal not_in_tree

        # select a random sample of nodes to which the current node should be connected
        new_tree_nodes = random.sample(not_in_tree, min(random.choice(spanning_tree_selection_range), len(not_in_tree)))

        # remove the nodes in this sample from the list of not-added nodes, so that future recursions will not use them
        not_in_tree = [n for n in not_in_tree if n not in new_tree_nodes]

        # establish edges to these new nodes and use them to spread the tree further
        for next_node in new_tree_nodes:
            edge_between(branch, next_node)
            spanning_tree(next_node)

        # collect a list of nodes that this node is not already attached to
        not_next_tree_nodes = [n for n in nodes if n not in new_tree_nodes and n != branch]

        # select a random number of nodes according to the range and attach this node to them
        for next_node in random.sample(not_next_tree_nodes, min(random.choice(extra_edge_range), len(not_next_tree_nodes))):
            edge_between(branch, next_node)

    spanning_tree(origin)

    return (origin, destinations, nodes)

# execute the problem generation algorithm, convert it to a test file string, and print it to stdout
print(to_test_file(*generate_problem(
    width,
    height,
    node_count_range,
    dest_count_range,
    spanning_tree_selection_range,
    extra_edge_range,
    max_added_distance
    )))
