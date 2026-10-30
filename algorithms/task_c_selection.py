from typing import Sequence


def select_kth(times: Sequence[int], k: int) -> int:
    if not times:
        raise ValueError("Selection requires at least one delivery time.")
    if type(k) is not int or not 1 <= k <= len(times):
        raise ValueError(f"k must be an integer between 1 and {len(times)}.")
    if any(type(t) is not int or t < 0 for t in times):
        raise ValueError("All delivery times must be nonnegative integers.")

    def choose(values: list[int], rank: int) -> int:
        if len(values) <= 5:
            return sorted(values)[rank - 1] 

        medians = []
        for start in range(0, len(values), 5):
            group = sorted(values[start:start + 5])
            medians.append(group[len(group) // 2])
        pivot = choose(medians, (len(medians) + 1) // 2)

        smaller: list[int] = []
        equal: list[int] = []
        larger: list[int] = []
        for value in values:
            if value < pivot:
                smaller.append(value)
            elif value > pivot:
                larger.append(value)
            else:
                equal.append(value)

        if rank <= len(smaller):
            return choose(smaller, rank)
        if rank <= len(smaller) + len(equal):
            return pivot
        return choose(larger, rank - len(smaller) - len(equal))

    return choose(list(times), k)
