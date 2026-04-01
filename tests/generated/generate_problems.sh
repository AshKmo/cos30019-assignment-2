#!/bin/bash
for i in {1..100}; do
	python ../../problem_generator.py > "GeneratedProblem-$i.txt"
done
