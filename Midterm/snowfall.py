"""Problem 1: do three consecutive days hold more than half of all the snowfall?

Usage: python snowfall.py snowfall_input1.txt [snowfall_input2.txt ...]
       python snowfall.py < snowfall_input1.txt

Input:  line 1 = n, line 2 = the n cumulative snowfall totals A[1..n].
Output: <input> solution: <YES|NO>
"""
import sys
from fractions import Fraction


def has_heavy_window(totals):
    """Return True if some three consecutive days have strictly more than half the total.

    totals holds A[1..n]. With A[0] = 0, the snowfall on days i, i+1, i+2 is
    A[i+2] - A[i-1], so each window costs one subtraction. The test
    2 * window > total is "more than half" without dividing by 2.
    O(n) time and O(n) memory for the copy with A[0] added.
    """
    n = len(totals)
    if n < 3:
        return False
    A = [0] + totals              # A[0] = 0, then A[1..n] as in the problem
    for i in range(1, n - 1):     # windows start on days 1 .. n-2
        if 2 * (A[i + 2] - A[i - 1]) > A[n]:
            return True
    return False


def solve(text):
    """Return the output line for one input file."""
    lines = [line.split() for line in text.splitlines() if line.strip()]
    n = int(lines[0][0])
    tokens = [token for line in lines[1:] for token in line][:n]
    totals = [Fraction(token) for token in tokens]
    answer = "YES" if has_heavy_window(totals) else "NO"
    return f"{' '.join(tokens)} solution: {answer}"


def main():
    if len(sys.argv) > 1:
        for path in sys.argv[1:]:
            with open(path, encoding="utf-8-sig") as f:
                print(solve(f.read()))
    else:
        # Decode as UTF-8 and drop the byte order mark that a PowerShell pipe can add.
        print(solve(sys.stdin.buffer.read().decode("utf-8-sig")))


if __name__ == "__main__":
    main()
