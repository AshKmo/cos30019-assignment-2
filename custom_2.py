import test_file_lib
import heuristics
import nodes

def get_path(destination: nodes.Node):
    "Return the full path from origin to destination."
    path: list[nodes.Node] = [destination]
    location = destination.parent
    while destination:
        path.append(location)
        location = location.parent
    return path.reverse()

def custom_2(origin: test_file_lib.GraphNode, heuristic: heuristics.Heuristic):
    "Custom informed search algorithm. Alternates between picking the lowest path cost and the best heuristic score."

    start = nodes.Node(origin)
    visited: set[nodes.Node] = set([])
    to_visit: list[nodes.Node] = [start]
    mode = False

    while to_visit:
        if mode:
            location = min(to_visit, key = lambda node: node.root_cost)
        else:
            location = min(to_visit, key = lambda node: node.value)
        mode = not mode

        to_visit.remove(location)
        visited.add(location)

        if location.state.is_destination:
            return (get_path(location), len(visited) + 1)
        
        for neighbor in location.state.edges:
            if neighbor.node_to not in visited and neighbor.node_to not in to_visit:
                child = nodes.Node(neighbor.node_to, neighbor, location)
                child.value = heuristic.judge(child)
                to_visit.append(child)

(start, destinations, graph_nodes) = test_file_lib.read_test_file("tests/PathFinder-test.txt")
custom_2(start, heuristics.AngleHeuristic(start, destinations, graph_nodes))