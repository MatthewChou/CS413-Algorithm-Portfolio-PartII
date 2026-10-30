import argparse
import json
from pathlib import Path

from algorithms.task_a_closest import closest_pair
from algorithms.task_b_inversions import count_inversions
from algorithms.task_c_selection import select_kth


def main() -> None:
    parser = argparse.ArgumentParser(description="Pioneer Delivery: Part II")
    parser.add_argument("task", choices=("closest", "inversions", "select"))
    parser.add_argument("input_file", type=Path, help="JSON input; see README")
    args = parser.parse_args()
    try:
        with args.input_file.open("r", encoding="utf-8") as stream:
            data = json.load(stream)
        if args.task == "closest":
            a, b, d_squared = closest_pair(
                [(p["id"], p["x"], p["y"]) for p in data["locations"]]
            )
            result = {"ids": [a, b], "distance_squared": d_squared}
        elif args.task == "inversions":
            result = {"inversions": count_inversions(data["planned"], data["actual"])}
        else:
            result = {"kth_smallest": select_kth(data["times"], data["k"])}
    except (OSError, ValueError, TypeError, KeyError, json.JSONDecodeError) as exc:
        parser.exit(2, f"Input error: {exc}\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
