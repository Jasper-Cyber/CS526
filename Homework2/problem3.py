"""
Problem 3 - Climbing Stairs

A staircase has n steps. Each move climbs 1, 2, or 3 steps. ways(n)
returns the number of distinct sequences of moves that reach the top.
"""


def ways(n):
    """Return the number of ways to climb a staircase of n steps,
    taking 1, 2, or 3 steps at a time.

    Recursive, no loops: think about the very first move.
    - If the first move is 1 step, ways(n - 1) ways remain.
    - If the first move is 2 steps, ways(n - 2) ways remain.
    - If the first move is 3 steps, ways(n - 3) ways remain.
    Summing these covers every possible first move.
    """
    if n < 0:
        # Overshot the top - this path is not a valid way to climb.
        return 0
    if n == 0:
        # Standing exactly at the top: this counts as exactly one way
        # (the "do nothing more" way) - it's what makes the recursive
        # sum above correct, since a move that lands exactly on step n
        # must contribute 1, not 0.
        return 1

    return ways(n - 1) + ways(n - 2) + ways(n - 3)


if __name__ == "__main__":
    print("ways(3) =", ways(3))
    print("ways(5) =", ways(5))
    print("ways(10) =", ways(10))
