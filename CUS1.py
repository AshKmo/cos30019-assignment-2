import math
from queue import PriorityQueue

from nodes import Node

# creates a list of the names of the states in the path from the root node to the node containing said state
def action_path(branch): return action_path(branch.parent) + [branch.state] if branch else []

# performs Uniform Cost Search from a given origin vertex
def uniform_cost_search(origin):
    root = Node(origin)

    # create the initial frontier, containing only the origin node
    frontier = PriorityQueue()

    # set the root node value to its path cost
    root.value = root.root_cost

    frontier.put(root)

    # create a set of nodes that have at some point been added to the frontier
    seen = set([origin])

    # keep a count of the number of nodes created
    node_count = 1

    # explore all nodes in the frontier until it is emptied
    while frontier.qsize() > 0:
        # consider the next node in the frontier with the lowest path cost
        branch = frontier.get()

        # if a goal state has been reached we can return the path to the goal and the node count
        if branch.state.is_destination:
            return (action_path(branch), node_count)

        # iterate through each edge pointing from the vertex
        for edge in branch.state.edges:
            # ignore nodes that are already in the frontier or that have been visited in the past
            if edge.node_to in seen: continue

            # create a new node for this state and add it to the frontier for exploration
            new_node = Node(edge.node_to, edge, branch)

            # for UCS, only the total path cost from the root is used
            new_node.value = new_node.root_cost

            frontier.put(new_node)

            # exclude this state from being added to the frontier again
            seen.add(edge.node_to)

            # increment the node creation count
            node_count += 1

    # return a None path to signify no solution, but still provide the node count
    return (None, node_count)