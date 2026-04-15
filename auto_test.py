# This script automatically tests each algorithm, using each heuristic (where applicable), against each test case

from sys import stderr, argv
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

# the number of tests to perform for each algorithm under each set of conditions
# more tests, in theory, means a more accurate timing average
tests_per_algorithm = 1000

# each algorithm to test
# for each algorithm, a tuple is stored containing the name of the algorithm, whether or not heuristics are applicable to this algorithm, and the algorithm itself
all_algorithms = [
        ("BFS", False, breadth_first_search),
        ("DFS", False, depth_first_search),
        ("A_star", True, a_star_search),
        ("GBFS", True, greedy_best_first_search),
        ("Uniform_Cost", False, uniform_cost_search),
        ("Beam", True, beam_search)
        ]

# each heuristic and its name
all_heuristics = [
        ("Distance", heuristics.DistanceHeuristic),
        ("Angle", heuristics.AngleHeuristic)
        ]

# the paths to the directories where the desired test case files are located
test_case_file_paths = [
        "tests/",
        "tests/generated/"
        ]

# add the option to perform a validation test whereby no actual test data is produced
# this is useful for quickly testing that all algorithms and test cases are valid
# this can be triggered by adding "val" as a command-line argument
validate_only = len(argv) > 1 and argv[1] == "val"

if validate_only:
    tests_per_algorithm = 1

test_case_files = []

# find all the test case files from all the test directories
for path in test_case_file_paths:
    for file in [f for f in Path(path).iterdir() if f.is_file()]:
        test_case_files.append(path + file.name)

# print the TSV header
print("Algorithm\tHeuristic\tTest\tNodes in Test\tAverage Time\tNodes")

# iterate through each combination of algorithm, heuristic, and test case, printing the results along the way
for test_i, test in enumerate(test_case_files):
    # show a progress report to the user each time a new test case is being worked on
    stderr.write(f"{test} ({test_i + 1} of {len(test_case_files)}; {test_i * 100 // len(test_case_files)}%)\n")

    for algorithm in all_algorithms:
        for heuristic in (all_heuristics if algorithm[1] else [None]):
            # read the test case file
            test_data = read_test_file(test)

            # the cumulative difference between the start and end times of each test
            total_diff = 0

            start = None
            end = None
            test_result = None

            # test the algorithm against each test case some number of times
            for i in range(tests_per_algorithm):
                # if heuristics are involved, call the algorithm with the heuristic
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

            if not validate_only:
                # print the algorithm name, the heuristic used (if applicable), the test case used, the number of nodes in this test case, the average amount of time this algorithm took to complete the test case, and the number of nodes created
                print(f"{algorithm[0]}\t{heuristic[0] if heuristic else ""}\t{test}\t{len(test_data[2])}\t{total_diff / tests_per_algorithm}\t{test_result[1]}")
