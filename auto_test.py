# This script automatically tests each algorithm, using each heuristic (where applicable), against each test case

from sys import stderr
from pathlib import Path
from time import perf_counter_ns

from test_file_lib import read_test_file

from BFS import breadth_first_search
from DFS import depth_first_search
from A_star import a_star_search
from GBFS import greedy_best_first_search
from CUS1 import uniform_cost_search
from beam_search import beam_search

import heuristics

tests_per_algorithm = 1000

all_algorithms = [
        ("BFS", False, breadth_first_search),
        ("DFS", False, depth_first_search),
        ("A_star", True, a_star_search),
        ("GBFS", True, greedy_best_first_search),
        ("Uniform_Cost", False, uniform_cost_search),
        ("Beam", True, beam_search)
        ]

all_heuristics = [
        ("Distance", heuristics.DistanceHeuristic),
        ("Angle", heuristics.AngleHeuristic)
        ]

test_file_paths = [
        "tests/",
        "tests/generated/"
        ]

test_files = []

for path in test_file_paths:
    for file in [f for f in Path(path).iterdir() if f.is_file()]:
        test_files.append(path + file.name)

print("Algorithm\tHeuristic\tTest\tAverage Time\tNodes")

for test_i, test in enumerate(test_files):
    stderr.write(f"{test} ({test_i + 1} of {len(test_files)}; {test_i * 100 // len(test_files)}%)\n")

    for algorithm in all_algorithms:
        for heuristic in (all_heuristics if algorithm[1] else [None]):
            test_data = read_test_file(test)

            total_diff = 0

            start = None
            end = None
            test_result = None

            for i in range(tests_per_algorithm):
                if algorithm[1]:
                    heuristic_object = heuristic[1](*test_data)

                    start = perf_counter_ns()
                    test_result = algorithm[2](test_data[0], heuristic_object)
                    end = perf_counter_ns()
                else:
                    start = perf_counter_ns()
                    test_result = algorithm[2](test_data[0])
                    end = perf_counter_ns()

                total_diff += end - start

            print(f"{algorithm[0]}\t{heuristic[0] if heuristic else ""}\t{test}\t{total_diff / tests_per_algorithm}\t{test_result[1]}")
