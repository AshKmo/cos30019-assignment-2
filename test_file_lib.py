'''

USAGE:

Put this script in the same folder as your script, and add this line to the top of your script:

    from test_file_lib import read_test_file

Now you can use the function read_test_file(path) to read test files.

Just call the function with the path to the file you want to read, e.g.

    read_test_file("tests/PathFinder-test.txt")

This function returns a GraphNode object that represents the origin of the graph (the initial state).

You can use GraphNode objects like this:

    graph_node = read_test_file("tests/PathFinder-test.txt") # read the graph from the file

    graph_node.is_destination # this is True only if this is one of the destinations

    graph_node.edges # this is the list of possible edges for this graph node

Each of the edges in a graph node is an Edge object.

You can use Edge objects like this:

    edge = graph_node.edges[0] # get the first edge. Edges are sorted by the name of the graph node to which they point, as per the assignment document

    edge.node_to # the graph node that this edge points toward; the next node the agent will be at

    edge.node_from # the graph node that this edge points away from

    edge.cost # this is the cost of the path to the next graph node

'''

import math
from ast import literal_eval
from sys import argv

# a class representing a node on the graph
class GraphNode:
    def __init__(self, name, x, y, edges = None, is_origin = False, is_destination = False):
        # the node's name, aka its number
        self.name = name

        # the x value of the node
        self.x = x

        # the y value of the node
        self.y = y

        # the edges that originate from this node
        self.edges = edges or []

        # whether or not this node is a destination node
        self.is_destination = is_destination

        # whether or not this node is the origin
        self.is_origin = is_origin

    # this function performs the goal test on the node
    # it returns True only if this node is a destination node
    def goal_test():
        return self.is_destination

    # this function allows this object to be converted to a string for debugging purposes
    def __repr__(self):
        return f"GraphNode{{{self.name}: {(self.x, self.y)}}}"

# a class representing an edge from one node to another
class Edge:
    def __init__(self, node_from, node_to, cost):
        # the node from which this edge points
        self.node_from = node_from

        # the node to which this edge points; the next state that the agent will be in if it follows this path
        self.node_to = node_to

        # the cost of traversing the edge
        self.cost = cost

    # this function allows this object to be converted to a string for debugging purposes
    def __repr__(self):
        return f"Edge{{{(self.node_from.name, self.node_to.name)}: {self.cost}}}"

# retrieves a test file indicated by `path` and parses it into a graph of GraphNode and Edge objects
def read_test_file(path):
    # a list that will be populated with the destination nodes
    destinations = []

    # a dictionary that will be populated with all nodes
    nodes = {}

    # the origin node
    origin = None

    # the current segment of data that is being read
    # 0 is the initial state
    # 1 is the "Nodes" section
    # 2 is the "Edges" section
    # 3 is the "Origin" section
    # 4 is the "Destinations" section
    mode = 0

    # the lines in the file
    lines = None

    # read the file into `lines`
    with open(path) as file:
        lines = list(file)

    # iterate through each line and parse it
    for line in lines:
        content = line.strip()

        # ignore comment lines, which start with a '#' symbol
        if content == "" or content[0] == "#":
            continue

        # set the current reading state if a heading is found
        if "Nodes:" in content:
            mode = 1
            continue
        elif "Edges:" in content:
            mode = 2
            continue
        elif "Origin:" in content:
            mode = 3
            continue
        elif "Destinations:" in content:
            mode = 4
            continue

        match mode:
            # "Nodes" section
            case 1:
                s = content.split(":")

                # the name of the node is found before the colon
                name = int(s[0])

                # everything after the colon is the node's position
                # this uses Python's built-in expression-parsing tech to parse the (x, y) tuple
                (x, y) = literal_eval(s[1])

                # make a new node with the appropriate name and coordinates and add the node to the nodes dictionary
                nodes[name] = GraphNode(name, x, y)

            # "Edges" section
            case 2:
                s = content.split(":")

                # the names of the start and end nodes are found before the colon
                # this uses Python's built-in expression-parsing tech to parse the (start, end) tuple
                (start, end) = literal_eval(s[0])

                # the cost is found after the colon
                cost = literal_eval(s[1])

                # find the start and end nodes from their names
                start_node = nodes[start]
                end_node = nodes[end]

                for edge in start_node.edges:
                    # if an identical edge has already been defined, ignore this one
                    if edge.node_to == end_node:
                        break
                else:
                    # if the cost value is an ellipsis, generate a proper one using the euclidean distance
                    # this is useful for crafting test files manually
                    if cost == ...:
                        cost = math.ceil(math.dist((start_node.x, start_node.y), (end_node.x, end_node.y)))

                    # add the edge to the edge list of the node from which the edge points
                    start_node.edges.append(Edge(start_node, end_node, cost))

            # "Origin" section
            case 3:
                # the only thing in the origin section is the name of the origin node
                
                # obtain the origin node using its name
                origin = nodes[int(content)]

                # give this special node some boasting rights
                origin.is_origin = True

            # "Destinations" section
            case 4:
                # split the list of destinations into a sequence of numbers
                for x in content.split(";"):
                    # ignore extra whitespace
                    x = x.strip()

                    # ignore extra semicolons
                    if not x: continue

                    # find the destination node from its name
                    dest = nodes[int(x)]

                    # give this node some boasting rights
                    dest.is_destination = True

                    # add the newly-promoted destination node to the stash of destination nodes
                    destinations.append(dest)

    # go through each node and make sure its edges are ordered by the names of their destinations, so that lower-numbered nodes are searched first
    for node in nodes.values():
        node.edges.sort(key=lambda o : o.node_to.name)

    # return the origin node, the list of destination nodes, and the complete dictionary of nodes
    return (origin, destinations, nodes)

# converts a test back to its text representation
def to_test_file(origin, destinations, nodes):
    # maintain a list of all edges
    edges = []

    # create the Nodes section
    result = "Nodes:\n"

    # for each node, add each of its edges to the edge list and add the node's string representation to the result string
    for n in nodes.values():
        edges += [e for e in n.edges if e not in edges]
        result += f"{n.name}: ({n.x},{n.y})\n"

    # create the Edges section
    result += "Edges:\n"

    # add each edge's string representation to the result string
    for e in edges:
        result += f"({e.node_from.name},{e.node_to.name}): {e.cost}\n"

    # add the Origin section and the origin node's name to the result string
    result += f"\nOrigin:\n{origin.name}\n"

    # add the Destinations section and add each destination node's name to the result string
    result += "Destinations:\n" + "; ".join(str(d.name) for d in destinations)

    return result

# if this script is executed on its own, it will parse a given test file and then print an equivalent string representation back
# this is useful for testing the parser or for de-humanising a manually-written script file so that it becomes less disorganised
if __name__ == "__main__":
    # maintain a counter that will determine the new names of each node
    name_counter = 0

    # parse the test from the contents of the file given in the first command-line argument
    (origin, destinations, nodes) = read_test_file(argv[1])

    for node in nodes.values():
        # change the number of each node to a value in a sequence in case the original numbers were poorly chosen
        name_counter += 1
        node.name = name_counter

    # print the string representation of the test we just parsed
    print(to_test_file(origin, destinations, nodes))
