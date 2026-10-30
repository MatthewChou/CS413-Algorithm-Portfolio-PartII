import argparse
import csv
import platform
import random
import statistics
import time
from pathlib import Path

from algorithms.task_a_closest import closest_pair
from algorithms.task_b_inversions import count_inversions
from algorithms.task_c_selection import select_kth


def timed_call(function, repetitions):
    function()
    samples_ms = []
    for _ in range(repetitions):
        start = time.perf_counter_ns()
        function()
        samples_ms.append((time.perf_counter_ns() - start) / 1_000_000)
    return statistics.median(samples_ms)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sizes", nargs="+", type=int, default=[100, 1000, 5000])
    parser.add_argument("--repeats", type=int, default=7)
    parser.add_argument("--output", type=Path, default=Path("results/benchmarks.csv"))
    args = parser.parse_args()
    if args.repeats < 1 or any(n < 2 for n in args.sizes):
        parser.error("repeats >= 1 and each size >= 2 are required")
    rng = random.Random(413)
    rows = []
    for n in args.sizes:
        xs = rng.sample(range(20 * n), n)
        coords = [(f"P{i}", xs[i], rng.randrange(0, 20 * n)) for i in range(n)]
        planned = [f"D{i}" for i in range(n)]
        actual = planned[:]
        rng.shuffle(actual)
        times = [rng.randrange(0, max(10, n // 10)) for _ in range(n)]
        k = (n + 1) // 2
        functions = {
            "Task A: Closest pair": lambda: closest_pair(coords),
            "Task B: Inversion count": lambda: count_inversions(planned, actual),
            "Task C: Median of medians": lambda: select_kth(times, k),
        }
        for task, fn in functions.items():
            median_ms = timed_call(fn, args.repeats)
            rows.append({"task": task, "n": n, "median_ms": f"{median_ms:.4f}", "repeats": args.repeats})
            print(f"{task:28} n={n:>6} median={median_ms:>9.4f} ms")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["task", "n", "median_ms", "repeats"])
        writer.writeheader()
        writer.writerows(rows)
    metadata_path = args.output.with_suffix(".environment.txt")
    metadata_path.write_text(
        f"Python: {platform.python_version()}\nPlatform: {platform.platform()}\n"
        f"CPU: {platform.processor() or 'not reported by platform'}\n"
        "Timing: time.perf_counter_ns; median of repetitions after one warm-up\n"
        "Inputs: reproducible random seed 413, created outside timing\n"
        "Note: measurements reflect the runtime environment, not a guaranteed benchmark.\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
