import test_file_lib
import heuristics
import nodes

# creates a list of the names of the states in the path from the root node to the node containing said state
def get_path(branch): return get_path(branch.parent) + [branch.state] if branch else []

def beam_search(origin: test_file_lib.GraphNode, heuristic: heuristics.Heuristic):
    "Performs beam search algorithm. This only keeps track of a set number of options, and chooses the one which looks the best. The beam width is 3 nodes in this example."
    
    #change this const to change the beam width
    WIDTH = 3

    #beam is a list of max length WIDTH, backup is all of the nodes which do not make it into beam
    start = nodes.Node(origin)
    seen = set([origin])
    beam = [start]
    backup: list[nodes.Node] = []
    created = 1

    # explore until a solution is found or all options are exhausted
    while True:
        # check if the destination is in the beam
        for node in beam:
            if node.state.is_destination:
                return (get_path(node), created)

        # make an empty list of candidates (nodes which may make it into the new beam)
        candidates: list[nodes.Node] = []

        # create new child nodes as candidates to account for multiple possible paths to the same node
        for node in beam:
            for edge in node.state.edges:
                if edge.node_to in seen: continue

                child = nodes.Node(edge.node_to, edge, node)
                candidates.append(child)
                created += 1
        
        #if no candidates were found, try to populate the beam with backup candidates
        if not candidates:
            if not backup:
                return None
            beam = backup[:WIDTH]
            backup = backup[WIDTH:]
            continue

        #sort the candidates using f(n) = g(n) + h(n), then only add the best 3 to the beam
        candidates.sort(key = lambda candidate: heuristic.judge(candidate) + candidate.root_cost)
        beam = candidates[:WIDTH]
        backup.extend(candidates[WIDTH:])

        # if the beam is empty, try to populate it with backups
        if not beam:
            if not backup:
                return None
            beam = backup[:WIDTH]
            backup = backup[WIDTH:]