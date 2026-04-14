from os import listdir
from time import perf_counter_ns

from test_file_lib import read_test_file

from BFS import breadth_first_search
from DFS import depth_first_search
from A_star import a_star_search
from GBFS import greedy_best_first_search
from CUS1 import uniform_cost_search
from beam_search import beam_search

import heuristics

test_path="tests/generated"

all_algorithms = [("BFS", False, breadth_first_search), ("DFS", False, depth_first_search), ("A_star", True, a_star_search), ("GBFS", True, greedy_best_first_search), ("Uniform_Cost", False, uniform_cost_search), ("Beam", True, beam_search)]

all_heuristics = [("Distance", heuristics.DistanceHeuristic), ("Angle", heuristics.AngleHeuristic)]

print("test", end='')

for a in all_algorithms:
    for h in (all_heuristics if a[1] else [None]):
        for m in ["time", "nodes"]:
            print(f"\t{a[0]}{f" using heuristic {h[0]}" if a[1] else ""}: {m}", end='')

for test in listdir(test_path):
    print(f"\n{test}", end='')

    for algorithm in all_algorithms:
        for heuristic in (all_heuristics if algorithm[1] else [None]):
            test_data = read_test_file(test_path + "/" + test)

            start = None
            end = None
            test_result = None

            if algorithm[1]:
                heuristic_object = heuristic[1](*test_data)

                start = perf_counter_ns()
                test_result = algorithm[2](test_data[0], heuristic_object)
                end = perf_counter_ns()
            else:
                start = perf_counter_ns()
                test_result = algorithm[2](test_data[0])
                end = perf_counter_ns()

            print(f"\t{end - start}\t{test_result[1]}", end='')
