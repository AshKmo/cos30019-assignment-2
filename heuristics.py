import math

"""

USAGE:

This script contains DistanceHeuristic and AngleHeuristic classes that you can use to process heuristics.

If you want to use heuristics, you should add another argument to your search function (e.g. `a_star_search(origin, heuristic)`) so that you can pass a Heuristic object to it from "search.py". Within your search function, you can then use the Heuristic object to judge each Node (from "nodes.py"), like this:

    my_search(origin, heuristic):
        ...
        node = Node(graph_node, edge, parent)
        node.value = heuristic.judge(node) # an example for GBFS
        node.value = heuristic.judge(node) + node.root_cost # an example for A*

You can create a Heuristic object like this: `DistanceHeuristic(origin, destinations, nodes)`. The three arguments are all provided by `read_test_file()`, which I have updated to do so.

"""

# a 2D vector class
class Vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # the dot product of two vectors is the sum of the products of their components
    def dot(self, other):
        return self.x * other.x + self.y * other.y
    
    # the magnitude of a vector is the square root of the sum of the squares of its components
    def mag(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    # a vector can be converted to a unit vector by dividing its components by its magnitude
    def unit(self):
        m = self.mag()

        # if the vector has zero magnitude, return a zero vector
        if m == 0: return Vec2(0, 0)

        return Vec2(self.x / m, self.y / m)

# the base heuristic class
class Heuristic:
    def __init__(self, origin, destinations, nodes):
        self.origin = origin
        self.destinations = destinations
        self.nodes = nodes

    def judge(self, graph_node):
        raise NotImplementedError("you should have used a subclass, e.g. DistanceHeuristic")

# this heuristic judges nodes based on their distance to the nearest destination node
class DistanceHeuristic(Heuristic):
    def judge(self, node):
        min_distance = math.inf

        for dest in self.destinations:
            min_distance = min(min_distance, math.dist((node.state.x, node.state.y), (dest.x, dest.y)))

        return min_distance

# this heuristic judges each node based on how closely the angle from its parent to itself matches that from its parent to the nearest destination
class AngleHeuristic(Heuristic):
    def judge(self, node):
        # if this is the root node, then this is always going to be the right node to search first
        if not node.parent: return 0

        # go through each destination to find the closest one to the parent of the current node
        min_distance = math.inf
        parent_to_dest = Vec2(0, 0)
        for dest in self.destinations:
            # create a vector from the parent node to the destination node
            new_parent_to_dest = Vec2(dest.x - node.parent.state.x, dest.y - node.parent.state.y);

            # determine the distance from this parent node to the destination node
            new_distance = new_parent_to_dest.mag()

            # if a closer destination is found, choose that one
            if new_distance < min_distance:
                parent_to_dest = new_parent_to_dest
                min_distance = new_distance

        # find the vector from the parent of the option to the option itself
        parent_to_child = Vec2(node.state.x - node.parent.state.x, node.state.y - node.parent.state.y)

        # determine a measure of similarity between the direction of the unit vector from the parent to the child, and the direction of the unit vector from the parent to the closest destination
        angle_similarity = parent_to_child.unit().dot(parent_to_dest.unit())

        # return the full distance from parent to child if the angle is in the opposite direction, and zero distance if the angle is in the correct direction
        return min_distance * (1 - angle_similarity) / 2
