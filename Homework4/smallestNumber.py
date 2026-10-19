"""Problem 2: fewest array elements whose sum is greater than a target T.

Usage: python3 smallestNumber.py < fewest_1.txt

Input:  line 1 = n, line 2 = T, line 3 = n space-separated values.
Output: Input: 8,3,9,2,7,1,5 Target: 18 Answer: 3
"""
import sys


def smallest_count(values, target):
    """Return the fewest elements of values whose sum is strictly greater than target.

    Taking the largest remaining element each time gives the largest possible
    sum for every count k, so the first k whose sum passes target is the minimum.
    Returns -1 if even the sum of every element is not greater than target.
    """
    total = 0
    for count, value in enumerate(sorted(values, reverse=True), start=1):
        total += value
        if total > target:
            return count
    return -1


def parse_number(token):
    """Read a whole number as int and anything else (e.g. "2.5") as float."""
    try:
        return int(token)
    except ValueError:
        return float(token)


def main():
    # Decode as UTF-8 and drop the byte order mark that a PowerShell pipe can add.
    text = sys.stdin.buffer.read().decode("utf-8-sig")
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    n = int(lines[0])
    target = parse_number(lines[1])
    values = [parse_number(token) for token in " ".join(lines[2:]).split()][:n]

    answer = smallest_count(values, target)
    print(f"Input: {','.join(map(str, values))} Target: {target} Answer: {answer}")


if __name__ == "__main__":
    main()
