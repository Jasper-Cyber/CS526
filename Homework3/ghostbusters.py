"""Problem 4: can every Ghostbuster fire at once without any two streams crossing?

Usage: python3 ghostbusters.py < ghostbusters/ghostbusters_input_0.txt

Each stream is an infinite line. Two infinite lines in the plane always meet
unless they are parallel and distinct, and lines that coincide count as
crossing. So all ghosts are eliminated exactly when every stream has the same
direction and no two streams lie on the same line.
"""
import sys
from math import gcd


def line_key(bx, by, gx, gy):
    """Return (direction, offset) identifying the infinite line through B and G.

    direction is (dx, dy) reduced by their gcd with a canonical sign, so
    parallel lines share it. offset = dy*x - dx*y is constant along the line,
    so parallel lines share it only if they are the same line.
    """
    dx, dy = gx - bx, gy - by
    g = gcd(dx, dy)
    dx, dy = dx // g, dy // g
    if dx < 0 or (dx == 0 and dy < 0):
        dx, dy = -dx, -dy
    offset = dy * bx - dx * by
    return (dx, dy), offset


def all_eliminated(pairs):
    direction = None
    offsets = set()
    for bx, by, gx, gy in pairs:
        d, offset = line_key(bx, by, gx, gy)
        if direction is None:
            direction = d
        elif d != direction:
            return False  # not parallel, so the lines cross somewhere
        if offset in offsets:
            return False  # same line as an earlier stream
        offsets.add(offset)
    return True


def read_pairs(stream):
    lines = [line.split() for line in stream if line.strip()]
    n = int(lines[0][0])
    pairs = []
    for parts in lines[1:n + 1]:
        # B <x> <y> G <x> <y>
        pairs.append((int(parts[1]), int(parts[2]), int(parts[4]), int(parts[5])))
    return pairs


def main():
    pairs = read_pairs(sys.stdin)
    if all_eliminated(pairs):
        print("All Ghosts: were eliminated")
    else:
        print("All Ghosts: were not eliminated")


if __name__ == "__main__":
    main()
