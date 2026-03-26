from functools import total_ordering

"""

USAGE:

This script provides a Node object that you can use in your scripts to keep track of parent nodes and to run heuristics.

You can create a Node for the origin (the first GraphNode) by simply running `Node(origin)`, but for child nodes you should provide the parent and the edge as well like this: `Node(origin, edge, parent)`.

If you want to run heuristics, you must provide the GraphNode, Edge, and parent node. You should also set the value of the Node to the value of the evaluation function (including any heuristics), like this:

    node = Node(graph_node, edge, parent)
    node.value = heuristic.judge(node) # GBFS example, because the value of each node is just the heuristic value
    node.value = heuristic.judge(node) + root_cost # A* example, because the value of each node is the heuristic value plus the total path cost

Node objects are already sortable due to the built-in __lt__ function, so they will automatically work in Python PriorityQueue's.

Node objects contain the following useful properties:

    node.state # the current GraphNode
    node.edge # the edge from which this GraphNode was discovered, if any
    node.parent # the parent Node
    node.root_cost # the total cost of the path from the highest ancestor Node to this Node
    node.value # the value of the Node, which you must set yourself after creating the Node

    node.heuristic # the Heuristic object that will partially evaluate this Node
    node.evaluation_function # the evaluation function from which this Node was evaluated

Each Node object also has a `path_to()` method that returns the full path to this Node so that you don't have to implement your own logic for this when returning a search result.

"""

class Node:
    # `state` is the GraphNode object that represents the current state
    # (OPTIONAL) `edge` is the Edge from which this state was discovered
    # (OPTIONAL) `parent` is the previously visited Node
    def __init__(self, state, edge = None, parent = None):
        # the state that was discovered at this position
        self.state = state

        # the edge from which the new state was discovered
        self.edge = edge

        # the state from which this edge was discovered
        self.parent = parent

        # the total path cost from the root to this node
        self.root_cost = (parent.root_cost if parent else 0) + (self.edge.cost if self.edge else 0)

        # the value of the node. You should set this after creating the Node.
        self.value = 0

    # run this method to obtain the full path from the origin to this node
    def path_to(self):
        return (self.parent.path_to() if parent else []) + [self.state]

    # define a comparison method for sorting
    def __lt__(self, other):
        return self.value < other.value

    # define a string representation method for debugging
    def __repr__(self):
        return f"Node{{{self.state} value {self.value}}}";
