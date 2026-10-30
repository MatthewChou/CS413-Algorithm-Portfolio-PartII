import json
from pathlib import Path

from algorithms.task_a_closest import closest_pair
from algorithms.task_b_inversions import count_inversions
from algorithms.task_c_selection import select_kth

ROOT = Path(__file__).resolve().parent
cases = json.loads((ROOT / "data/test_cases.json").read_text(encoding="utf-8"))

lines = ["Pioneer Delivery - Part II: verified sample outputs", ""]
for task, entries in cases.items():
    for case in entries:
        name = case["name"]
        if task == "closest":
            payload = {"locations": [{"id": pid, "x": x, "y": y} for pid, x, y in case["locations"]]}
            a, b, squared = closest_pair(case["locations"])
            result = {"ids": [a, b], "distance_squared": squared}
            assert squared == case["expected_squared_distance"]
        elif task == "inversions":
            payload = {"planned": case["planned"], "actual": case["actual"]}
            result = {"inversions": count_inversions(**payload)}
            assert result["inversions"] == case["expected_inversions"]
        else:
            payload = {"times": case["times"], "k": case["k"]}
            result = {"kth_smallest": select_kth(**payload)}
            assert result["kth_smallest"] == case["expected_value"]
        (ROOT / "data" / f"{name}.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        lines.append(f"{task} | {name} | input=data/{name}.json | output={json.dumps(result)}")
(ROOT / "results/sample_outputs.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"Generated {sum(len(entries) for entries in cases.values())} example input files and actual outputs.")
