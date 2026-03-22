#this file is for exectuting pathfinding scripts, named 'search.py' as per the assignment specifications
#you will need to add code here for importing your own algorithms and executing scripts based on commands
#in the same directory as this file, run 'python search.py (file path) (alogrithm), to run this code
import sys
from test_file_lib import read_test_file
from BFS import breadth_first_search

def main():
    filename = sys.argv[1]
    method = sys.argv[2].lower()

    node = read_test_file(filename)
    #when writing your scripts, please have them return path as a list of GraphNode objects ordered from origin to destination
    path = [None]

    match method:
        #add a case for your scripts here
        case "bfs":
            path = breadth_first_search(node)

    #prints in expected output format as per the assignment specification e.g.
    #(filename) (method)
    #(goal) (number of nodes) *note that I am not fully sure on whether or not this should be the path length or how many steps it took to complete the path (I will ask in class)
    #path
    #note that additional line breaks are acceptable for the final output
    print(f"{filename} {method}\n{path[-1]} {len(path)}")
    for location in path:
        print(location)

if __name__ == "__main__":
    main()