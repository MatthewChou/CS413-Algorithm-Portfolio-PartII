# Pioneer Delivery Algorithm Portfolio — Part II

**Course assignment:** CS413, Fall 2026  
**Programming language:** Python 3.10+  
**Dependencies:** Python standard library only for the algorithms, CLI, tests, and benchmarks

This project solves all three problems using divide-and-conquer algorithms. Each is independently runnable through `main.py`.

Task A: Find the two closest delivery locations — O(n log n) time.
Task B: Count inversions between planned and actual dispatch orders — O(n log n) time.
Task C: Find the kth smallest delivery time using deterministic median of medians — O(n) worst-case time.

Run these commands in Command Prompt:


A — Closest pair `py main.py closest data\A1.json`
B — Inversion count |`py main.py inversions data\B1.json`
C — kth smallest value  `py main.py select data\C1.json`

Replace `A1.json`, `B1.json`, or `C1.json` with another input file in `data` to run other cases.

## Input and Output
Each program reads a JSON file and prints a JSON result.


 A  takes in `locations`: list of objects with `id`, `x`, `y` and outputs `ids`: closest location IDs and `distance_squared`: squared distance.
 B  takes in `planned`: list of delivery IDs; `actual`: list of those IDs in actual order and outputs `inversions`: number of inversions.
 C  takes in `times`: list of nonnegative integers; `k`: 1-based rank and outputs `kth_smallest`: selected delivery time.

## Reproducing Tests and Results
Run all required and additional test cases:

py -m unittest discover -s tests -v


Generate the example inputs and output records (`data\` and `results\sample_outputs.txt`):

py make_examples.py

Repeat the performance tests at three input sizes (`results\benchmarks.csv`):

py benchmarks.py --sizes 100 1000 5000 --repeats 5 --output results\benchmarks.csv

