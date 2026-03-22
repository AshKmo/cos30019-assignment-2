#in the same folder as your script, add the line 'import BFS' or 'from BFS import breadth_first_search' to include this script

import test_file_lib

def breadth_first_search(node: test_file_lib.GraphNode):
    "Breadth first search algorithm. Returns a list of GraphNode objects from the origin to the destination of a path"

    #visited is a set (which is a list without duplicates) of nodes which have already been visited
    visited: set[test_file_lib.GraphNode] = set([])
    #to_visit is a list of nodes which are children of the nodes in the layer currently being visited
    to_visit: list[test_file_lib.GraphNode] = [node]

    #this is a dictionary which will keep track of the first parent node upon discovery of a new node
    parent = {node: None}

    while len(to_visit) > 0:
        #poping to_visit ensures a location is only visited once
        location = to_visit.pop(0)

        #once the destination is reached, we make a list of nodes tracing a path from the origin to the destination and return it
        if location.is_destination:
            path = []
            current = location
            while current != None:
                path.append(current)
                current = parent[current]
            path.reverse()
            return path
        
        if location not in visited:
            #make sure the location is flagged as visited so that it wont be re-visited
            visited.add(location)
            for neighbor in location.edges:
                #only discover neighbors which have not been discovered
                if neighbor.node_to not in visited and neighbor.node_to not in to_visit:
                    #mark the parent node of each newly discovered neighbor so that it can be re-traced at the end of the function
                    parent[neighbor.node_to] = location
                    to_visit.append(neighbor.node_to)