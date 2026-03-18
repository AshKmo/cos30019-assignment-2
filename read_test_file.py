'''

USAGE:

Put this script in the same folder as your script, and add this line to the top of your script:

    import read_test_file

Now you can use the function read_test_file(path) to read test files.

Just call the function with the path to the file you want to read, e.g.

    read_test_file("PathFinder-test.txt")

This function returns a Node object representing the origin.

You can use Node objects like this:

    node = read_test_file("PathFinder-test.txt")

    node.is_destination # this is True only if this is a destination node

    node.options # this is the list of possible options for this node

Each of the options in a node is an Option object

You can use Option objects like this:

    option = node.options[0] # get the first option. Options are sorted by name as per the assignment document

    option.next_node # this is the next node the agent will be at if it chooses this option

    option.cost # this is the cost of the path to the next node

'''

from ast import literal_eval

class Node:
    def __init__(self, name, x, y, is_destination = False):
        self.name = name
        self.x = x
        self.y = y
        self.options = []
        self.is_destination = is_destination

    def goal_test():
        return self.is_destination

    def __repr__(self):
        return f"Node{{{self.name}: {(self.x, self.y)}}}"

class Option:
    def __init__(self, node, next_node, cost):
        self.node = node
        self.next_node = next_node
        self.cost = cost

    def __repr__(self):
        return f"Option{{{(self.node.name, self.next_node.name)}: {self.cost}}}"

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

                    nodes[name] = Node(name, x, y)

                case 2:
                    s = content.split(": ")

                    (start, end) = literal_eval(s[0])
                    cost = int(s[1])

                    nodes[start].options.append(Option(nodes[start], nodes[end], cost))

                case 3:
                    origin = nodes[int(content)]

                case 4:
                    for x in content.split("; "):
                        if not x: continue

                        nodes[int(x)].is_destination = True

    for node in nodes.values():
        node.options.sort(key=lambda o : o.next_node.name)

    return origin

print(read_test_file("PathFinder-test.txt").options)
