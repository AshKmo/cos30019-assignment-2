#this file is for exectuting pathfinding scripts, named 'search.py' as per the assignment specifications
#you will need to add code here for importing your own algorithms and executing scripts based on commands
#in the same directory as this file, run 'python search.py (file path) (alogrithm), to run this code

import sys

from test_file_lib import read_test_file

from BFS import breadth_first_search
from DFS import depth_first_search
from A_star import a_star_search
from GBFS import greedy_best_first_search
from CUS1 import uniform_cost_search
from beam_search import beam_search

import heuristics

def main():
    if len(sys.argv) < 3:
        print("usage: python search.py <data-file> <search-method>")
        sys.exit(1)

    filename = sys.argv[1]
    method = sys.argv[2].lower()

    (origin, destinations, graph_nodes) = read_test_file(filename)

    #when writing your scripts, please have them return path as a list of GraphNode objects ordered from origin to destination
    result = None

    match method:
        #add a case for your scripts here
        case "bfs":
            result = breadth_first_search(origin)
        case "dfs":
            result = depth_first_search(origin)
        case "gbfs":
            result = greedy_best_first_search(origin, heuristics.DistanceHeuristic(origin, destinations, graph_nodes))
        case "a_star":
            result = a_star_search(origin, heuristics.DistanceHeuristic(origin, destinations, graph_nodes))
        case "cus1":
            result = uniform_cost_search(origin)
        case "cus2":
            result = beam_search(origin, heuristics.DistanceHeuristic(origin, destinations, graph_nodes))
        case _:
            print("no such search method: " + method)
            sys.exit(1)

    path = result[0]
    node_count = result[1]

    # if no path was found, still print something sensible
    if path is None:
        print(f"{filename} {method}\nNo goal found {node_count}")
        return

    #prints in expected output format as per the assignment specification e.g.
    #(filename) (method)
    #(goal) (number of nodes)
    #path
    #note that additional line breaks are acceptable for the final output
    print(f"{filename} {method}\n{path[-1].name if path else None} {node_count}")

    print(" -> ".join(str(l.name) for l in path))

if __name__ == "__main__":
    main()
