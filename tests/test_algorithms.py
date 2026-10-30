import json
import random
import unittest
from pathlib import Path

from algorithms.task_a_closest import closest_pair
from algorithms.task_b_inversions import count_inversions
from algorithms.task_c_selection import select_kth

CASES = json.loads((Path(__file__).resolve().parents[1] / "data" / "test_cases.json").read_text())


def closest_bruteforce(locations):
    best_sq = None
    best = None
    for i in range(len(locations)):
        for j in range(i + 1, len(locations)):
            a, x1, y1 = locations[i]
            b, x2, y2 = locations[j]
            d_sq = (x1 - x2) ** 2 + (y1 - y2) ** 2
            if best_sq is None or d_sq < best_sq:
                best_sq, best = d_sq, (a, b)
    return best_sq, best


def inversions_bruteforce(planned, actual):
    positions = {name: i for i, name in enumerate(planned)}
    ranks = [positions[name] for name in actual]
    return sum(ranks[i] > ranks[j] for i in range(len(ranks)) for j in range(i + 1, len(ranks)))


class TaskATests(unittest.TestCase):
    def test_required_and_extra_cases(self):
        for case in CASES["closest"]:
            with self.subTest(case=case["name"]):
                a, b, distance = closest_pair(case["locations"])
                self.assertEqual(distance, case["expected_squared_distance"])
                if "expected_pair" in case:
                    self.assertEqual({a, b}, set(case["expected_pair"]))
                coordinates = {ident: (x, y) for ident, x, y in case["locations"]}
                self.assertNotEqual(a, b)
                self.assertEqual((coordinates[a][0] - coordinates[b][0]) ** 2 +
                                 (coordinates[a][1] - coordinates[b][1]) ** 2, distance)

    def test_random_oracle(self):
        randomizer = random.Random(413)
        for _ in range(250):
            size = randomizer.randrange(2, 35)
            coords = randomizer.sample([(x, y) for x in range(-9, 10) for y in range(-9, 10)], size)
            locations = [(f"P{i}", x, y) for i, (x, y) in enumerate(coords)]
            self.assertEqual(closest_pair(locations)[2], closest_bruteforce(locations)[0])

    def test_invalid(self):
        with self.assertRaises(ValueError):
            closest_pair([("A", 0, 0)])
        with self.assertRaises(ValueError):
            closest_pair([("A", 0, 0), ("B", 0, 0)])
        with self.assertRaises(ValueError):
            closest_pair([("A", 0, 0), ("A", 1, 1)])
        with self.assertRaises(ValueError):
            closest_pair([("A", 1.2, 0), ("B", 2, 0)])


class TaskBTests(unittest.TestCase):
    def test_required_and_extra_cases(self):
        for case in CASES["inversions"]:
            with self.subTest(case=case["name"]):
                self.assertEqual(count_inversions(case["planned"], case["actual"]),
                                 case["expected_inversions"])

    def test_large_count(self):
        n = 100_000
        planned = [str(i) for i in range(n)]
        self.assertEqual(count_inversions(planned, planned[::-1]), 4_999_950_000)

    def test_random_oracle(self):
        randomizer = random.Random(413)
        for _ in range(250):
            size = randomizer.randrange(1, 40)
            planned = [str(i) for i in range(size)]
            actual = planned[:]
            randomizer.shuffle(actual)
            self.assertEqual(count_inversions(planned, actual), inversions_bruteforce(planned, actual))

    def test_invalid(self):
        invalid = [([], []), (["A"], ["B"]), (["A", "A"], ["A", "A"]),
                   (["A", "B"], ["A"]), (["A", "B"], ["A", "C"])]
        for planned, actual in invalid:
            with self.subTest(planned=planned, actual=actual), self.assertRaises(ValueError):
                count_inversions(planned, actual)


class TaskCTests(unittest.TestCase):
    def test_required_and_extra_cases(self):
        for case in CASES["select"]:
            with self.subTest(case=case["name"]):
                self.assertEqual(select_kth(case["times"], case["k"]), case["expected_value"])

    def test_random_oracle(self):
        randomizer = random.Random(413)
        for _ in range(500):
            size = randomizer.randrange(1, 160)
            times = [randomizer.randrange(0, 30) for _ in range(size)]
            k = randomizer.randrange(1, size + 1)
            self.assertEqual(select_kth(times, k), sorted(times)[k - 1])

    def test_many_duplicate_values_large(self):
        times = [0] * 1000 + [3] * 3000 + [9] * 1000
        random.Random(413).shuffle(times)
        self.assertEqual(select_kth(times, 3500), 3)

    def test_invalid(self):
        for values, k in [([], 1), ([1, 2], 0), ([1, 2], 3), ([1, -2], 1),
                          ([1, 2.0], 1), ([1, 2], 1.5)]:
            with self.subTest(values=values, k=k), self.assertRaises(ValueError):
                select_kth(values, k)


if __name__ == "__main__":
    unittest.main()
