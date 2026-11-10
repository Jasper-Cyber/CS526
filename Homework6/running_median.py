"""Problem 3: the running median of the day's sales, using the MinHeap from Problem 2.

Usage: python running_median.py < median/median_input1.txt                (bash, Command Prompt)
       Get-Content median/median_input1.txt | python running_median.py    (PowerShell)
       python running_median.py median/median_input1.txt                   (any shell)
       python running_median.py median/median_input*.txt                   (several files)

Input:  one list of sale amounts, for example [5, 15, 2, 4, 8].
Output: the median after each sale, for example [5.0, 10.0, 5.0, 4.5, 5.0].
"""
import sys

sys.dont_write_bytecode = True     # importing linked_heap must not leave a __pycache__ folder
from linked_heap import MinHeap, expand_wildcards, parse_values, read_text  # noqa: E402


class RunningMedian:
    """The median of all amounts added so far, available in O(1) time.

    The amounts are split between two MinHeaps from Problem 2:
      lower  the smaller half, stored NEGATED, so its root is -(largest of the smaller half);
      upper  the larger half, so its root is the smallest of the larger half.

    After every add these two invariants hold:
      1. every amount in the smaller half is <= every amount in the larger half;
      2. len(lower) == len(upper), or len(lower) == len(upper) + 1.
    Together they mean the one or two middle amounts are always at the two
    roots, where peek() reads them in O(1). add takes O(log n).
    """

    def __init__(self):
        self.lower = MinHeap()     # -amount for each amount in the smaller half
        self.upper = MinHeap()

    def __len__(self):
        return len(self.lower) + len(self.upper)

    def add(self, amount):
        # 1. Put the amount in the half it belongs to. This keeps invariant 1.
        if self.lower.is_empty() or amount <= -self.lower.peek():
            self.lower.insert(-amount)
        else:
            self.upper.insert(amount)
        # 2. If one half is now too big, move its root (the amount nearest the
        #    middle) to the other half. Invariant 1 still holds, and this
        #    restores invariant 2.
        if len(self.lower) > len(self.upper) + 1:
            self.upper.insert(-self.lower.extract_min())
        elif len(self.upper) > len(self.lower):
            self.lower.insert(-self.upper.extract_min())

    def median(self):
        if self.lower.is_empty():
            raise IndexError("median of no sales")
        if len(self.lower) > len(self.upper):          # odd count: the middle amount
            return float(-self.lower.peek())
        return (-self.lower.peek() + self.upper.peek()) / 2   # even count: average of the two middle amounts


def running_medians(sales):
    """Return the median after each sale, as a list of floats."""
    tracker = RunningMedian()
    medians = []
    for amount in sales:
        tracker.add(amount)
        medians.append(tracker.median())
    return medians


def main():
    paths = expand_wildcards(sys.argv[1:]) or [None]
    status = 0
    for index, path in enumerate(paths):
        if len(paths) > 1:
            if index > 0:
                print()
            print(f"File Input: {path}")
        try:
            sales = parse_values(read_text(path, "Type a list such as [5, 15, 2, 4, 8]"))
        except (OSError, ValueError) as error:
            print(f"Error: {error}", file=sys.stderr)
            status = 1
            continue
        print(running_medians(sales))
    sys.exit(status)


if __name__ == "__main__":
    main()
