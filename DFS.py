from test_file_lib import read_test_file
from nodes import Node

# creates a list of the names of the states in the path from the root node to the node containing said state
def action_path(branch): return action_path(branch.parent) + [branch.state] if branch else []

# performs depth first search from a given origin vertex
def depth_first_search(origin):
    # create the initial frontier, containing only the origin node
    frontier = [Node(origin)]

    # create a set of nodes that have at some point been added to the frontier
    seen = set(frontier)

    # keep a count of the number of nodes created
    node_count = 1

    # keep track of the last explored state
    branch = None

    # explore all nodes in the frontier until it is emptied
    while frontier:
        # consider the last node in the frontier
        branch = frontier[-1]

        # if a goal state has been reached we can exit the loop
        if branch.state.is_destination: break

        # remove the last element from the frontier
        frontier.pop()

        # iterate through each edge pointing from the vertex
        for edge in reversed(branch.state.edges):
            # ignore nodes that are already in the frontier or that have been visited in the past
            if edge.node_to in seen: continue

            # create a new node for this state and add it to the frontier for exploration
            frontier.append(Node(edge.node_to, edge, branch))

            # exclude this state from being added to the frontier again
            seen.add(edge.node_to)

            # increment the node creation count
            node_count += 1

    # if the loop exited normally then a destination was not found
    if not frontier:
        return (None, node_count)

    # return the path to the destination
    return (action_path(branch), node_count)
