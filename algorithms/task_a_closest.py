from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class Point:
    id: str
    x: int
    y: int


def _squared_distance(a: Point, b: Point) -> int:
    return (a.x - b.x) ** 2 + (a.y - b.y) ** 2


def closest_pair(locations: Sequence[tuple[str, int, int]]) -> tuple[str, str, int]:
    points: list[Point] = []
    ids: set[str] = set()
    coordinates: set[tuple[int, int]] = set()
    for item in locations:
        try:
            pid, x, y = item
        except (TypeError, ValueError) as exc:
            raise ValueError("Every location must have (id, x, y).") from exc
        if not isinstance(pid, str) or not pid:
            raise ValueError("Each point ID must be a nonempty string.")
        if not all(type(value) is int for value in (x, y)):
            raise ValueError("Coordinates must be integers.")
        if pid in ids:
            raise ValueError(f"Duplicate location ID: {pid!r}.")
        if (x, y) in coordinates:
            raise ValueError(f"Duplicate location coordinates: ({x}, {y}).")
        points.append(Point(pid, x, y))
        ids.add(pid)
        coordinates.add((x, y))

    if len(points) < 2:
        raise ValueError("Closest pair requires at least two locations.")

    by_x = sorted(points, key=lambda p: (p.x, p.y, p.id))
    by_y = sorted(points, key=lambda p: (p.y, p.x, p.id))

    def solve(px: list[Point], py: list[Point]) -> tuple[int, tuple[str, str]]:
        n = len(px)
        if n <= 3:
            best_sq = float("inf")
            best_pair = ("", "")
            for i in range(n):
                for j in range(i + 1, n):
                    d_sq = _squared_distance(px[i], px[j])
                    if d_sq < best_sq:
                        best_sq = d_sq
                        best_pair = (px[i].id, px[j].id)
            return int(best_sq), best_pair

        middle = n // 2
        left_x, right_x = px[:middle], px[middle:]
        dividing_x = right_x[0].x

        left_ids = {p.id for p in left_x}
        left_y: list[Point] = []
        right_y: list[Point] = []
        for point in py:
            if point.id in left_ids:
                left_y.append(point)
            else:
                right_y.append(point)

        left_sq, left_pair = solve(left_x, left_y)
        right_sq, right_pair = solve(right_x, right_y)
        if left_sq <= right_sq:
            best_sq, best_pair = left_sq, left_pair
        else:
            best_sq, best_pair = right_sq, right_pair

        strip = [p for p in py if (p.x - dividing_x) ** 2 < best_sq]
        for i, point in enumerate(strip):
            for neighbor in strip[i + 1:i + 8]:
                if (neighbor.y - point.y) ** 2 >= best_sq:
                    break
                d_sq = _squared_distance(point, neighbor)
                if d_sq < best_sq:
                    best_sq, best_pair = d_sq, (point.id, neighbor.id)
        return best_sq, best_pair

    squared, pair = solve(by_x, by_y)
    return pair[0], pair[1], squared
