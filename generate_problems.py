# This script uses the problem generator ("problem_generator.py") to quickly generate a large number of random tests at once

# the number of tests to generate
n = 200

from problem_generator import generate_problem

from test_file_lib import to_test_file

for i in range(0, n):
    with open(f"tests/generated/test-generated-{i}.txt", "w") as f:
        # generate a random problem
        problem = generate_problem()

        # convert this problem to the text format
        test_file = to_test_file(*problem)

        # write this test to a new test file
        f.write(test_file)
