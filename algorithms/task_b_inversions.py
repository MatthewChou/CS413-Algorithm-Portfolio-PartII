from typing import Sequence


def count_inversions(planned: Sequence[str], actual: Sequence[str]) -> int:
    if not planned or not actual:
        raise ValueError("Both dispatch orders must contain at least one ID.")
    if len(planned) != len(actual):
        raise ValueError("Planned and actual orders must have the same length.")
    if any(not isinstance(v, str) or not v for v in (*planned, *actual)):
        raise ValueError("Delivery IDs must be nonempty strings.")
    if len(set(planned)) != len(planned) or len(set(actual)) != len(actual):
        raise ValueError("IDs must be distinct within each order.")
    if set(planned) != set(actual):
        raise ValueError("Planned and actual orders must contain the same IDs.")

    planned_ranks = {delivery_id: i for i, delivery_id in enumerate(planned)}
    ranks = [planned_ranks[delivery_id] for delivery_id in actual]
    buffer = [0] * len(ranks)

    def merge_count(lo: int, hi: int) -> int:
        if hi - lo <= 1:
            return 0
        mid = (lo + hi) // 2
        inversions = merge_count(lo, mid) + merge_count(mid, hi)
        i, j, k = lo, mid, lo
        while i < mid and j < hi:
            if ranks[i] <= ranks[j]:
                buffer[k] = ranks[i]
                i += 1
            else:
                buffer[k] = ranks[j]
                inversions += mid - i 
                j += 1
            k += 1
        while i < mid:
            buffer[k] = ranks[i]
            i += 1
            k += 1
        while j < hi:
            buffer[k] = ranks[j]
            j += 1
            k += 1
        ranks[lo:hi] = buffer[lo:hi]
        return inversions

    return merge_count(0, len(ranks))
