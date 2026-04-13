# This script uses the problem generator ("problem_generator.py") to quickly generate a large number of random tests at once

# the number of tests to generate
n = 100

from problem_generator import generate_problem

from test_file_lib import to_test_file

for i in range(0, n):
    with open(f"tests/generated/test-generated-{i}.txt", "w") as f:
        f.write(to_test_file(*generate_problem()))
