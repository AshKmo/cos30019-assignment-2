'''

USAGE:

Put this script in the same folder as your script, and add this line to the top of your script:

    import read_test_file

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

from ast import literal_eval

class GraphNode:
    def __init__(self, name, x, y, edges = None, is_origin = False, is_destination = False):
        self.name = name
        self.x = x
        self.y = y
        self.edges = edges or []
        self.is_destination = is_destination
        self.is_origin = is_origin

    def goal_test():
        return self.is_destination

    def __repr__(self):
        return f"GraphNode{{{self.name}: {(self.x, self.y)}}}"

class Edge:
    def __init__(self, node_from, node_to, cost):
        self.node_from = node_from
        self.node_to = node_to
        self.cost = cost

    def __repr__(self):
        return f"Edge{{{(self.node_from.name, self.node_to.name)}: {self.cost}}}"

def read_test_file(path):
    nodes = {}
    origin = None

    mode = 0

    with open(path) as file:
        for line in file:
            content = line.strip()

            match content:
                case "":
                    continue
                case "Nodes:":
                    mode = 1
                    continue
                case "Edges:":
                    mode = 2
                    continue
                case "Origin:":
                    mode = 3
                    continue
                case "Destinations:":
                    mode = 4
                    continue

            match mode:
                case 1:
                    s = content.split(": ")

                    name = int(s[0])
                    (x, y) = literal_eval(s[1])

                    nodes[name] = GraphNode(name, x, y)

                case 2:
                    s = content.split(": ")

                    (start, end) = literal_eval(s[0])
                    cost = int(s[1])

                    nodes[start].edges.append(Edge(nodes[start], nodes[end], cost))

                case 3:
                    origin = nodes[int(content)]
                    origin.is_origin = True

                case 4:
                    for x in content.split("; "):
                        if not x: continue

                        nodes[int(x)].is_destination = True

    for node in nodes.values():
        node.edges.sort(key=lambda o : o.node_to.name)

    return origin

def to_test_file(node):
    result = ""

    origin = 0
    nodes = []
    edges = []
    destinations = []

    def discover(node):
        if node in nodes: return

        nodes.append(node)

        for edge in node.edges:
            edges.append(edge)
            discover(edge.node_to)

    discover(node)

    nodes.sort(key=lambda n : n.name)

    result += "Nodes:\n"

    for node in nodes:
        if node.is_origin: origin = node.name
        if node.is_destination: destinations.append(str(node.name))

        result += f"{node.name}: ({node.x},{node.y})\n"

    result += "Edges:\n"

    for edge in edges:
        result += f"({edge.node_from.name},{edge.node_to.name}): {edge.cost}\n"

    result += f"\nOrigin:\n{str(origin)}"

    result += "\nDestinations:\n" + "; ".join(destinations)

    return result

print(to_test_file(read_test_file("tests/PathFinder-test.txt")))
