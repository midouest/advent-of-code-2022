def manhattan(a: tuple[int, int], b: tuple[int, int]) -> int:
    x1, y1 = a
    x2, y2 = b
    return abs(x1 - x2) + abs(y1 - y2)
