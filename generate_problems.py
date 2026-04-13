from problem_generator import generate_problem

from test_file_lib import to_test_file

for i in range(0, 100):
    with open(f"tests/generated/test-generated-{i}.txt", "w") as f:
        f.write(to_test_file(*generate_problem()))
