"""Problem 3: count the right triangles formed by choosing three of n distinct points.

Usage: python3 rightTriangles.py < rightangles_1.txt

Input:  line 1 = n, then n lines with one point "x y" each.
Output: The number of right triangles is: <answer>
"""
import sys
from collections import Counter
from fractions import Fraction
from math import gcd, lcm


def direction(dx, dy):
    """Reduce the vector (dx, dy) to the shortest integer vector pointing the same way.

    The sign is kept, so (2, 4) -> (1, 2) and (-2, -4) -> (-1, -2) are different
    rays. (dx, dy) must not be (0, 0).
    """
    g = gcd(dx, dy)
    return dx // g, dy // g


def count_right_triangles(points):
    """Return the number of right triangles whose corners are in points.

    Every right triangle has exactly one 90 degree corner, so each triangle is
    counted once, at that corner. For a corner P, two other points A and B form a
    right angle at P exactly when the ray P->B is the ray P->A turned 90 degrees.
    Turning (x, y) by +90 degrees gives (-y, x). Only +90 is counted, never -90,
    so each pair {A, B} is counted once. O(n^2) time, O(n) extra memory.
    """
    total = 0
    for i, (px, py) in enumerate(points):
        rays = Counter(direction(qx - px, qy - py)
                       for j, (qx, qy) in enumerate(points) if j != i)
        for (x, y), count in rays.items():
            total += count * rays.get((-y, x), 0)
    return total


def read_points(text):
    """Read the point count and the points from text, scaled to integers if needed.

    Integer coordinates are kept as they are. If any coordinate has a decimal part
    (e.g. "1.5"), every coordinate is read exactly as a Fraction and multiplied by
    the common denominator. Scaling keeps every angle, so the count is unchanged.
    Repeated points are kept only once.
    """
    lines = [line.split() for line in text.splitlines() if line.strip()]
    n = int(lines[0][0])
    coords = [[Fraction(token) for token in line[:2]] for line in lines[1:n + 1]]

    scale = lcm(*(c.denominator for point in coords for c in point))
    points = [(int(x * scale), int(y * scale)) for x, y in coords]
    return list(dict.fromkeys(points))


def main():
    # Decode as UTF-8 and drop the byte order mark that a PowerShell pipe can add.
    text = sys.stdin.buffer.read().decode("utf-8-sig")
    points = read_points(text)
    print(f"The number of right triangles is: {count_right_triangles(points)}")


if __name__ == "__main__":
    main()
