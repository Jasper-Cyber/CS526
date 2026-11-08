"""Problem 3: longest increasing sequence whose elements alternate between A and B.

Usage: python longest_seq.py longest_seq1.txt [longest_seq2.txt ...]
       python longest_seq.py longest_seq*.txt
       python longest_seq.py longest_seq1.txt --show    (also print one longest sequence)

Input:  line 1 = size of A, line 2 = size of B, line 3 = the A values,
        line 4 = the B values.
Output: File Input: longest_seq1.txt
        Longest Sequence: 4
"""
import glob
import os
import sys


class PrefixMax:
    """Fenwick tree (binary indexed tree) for prefix maximums.

    Positions are value ranks 1..size. update(rank, item) records item at that
    rank, and best(rank) returns the largest item recorded at ranks 1..rank.
    Both take O(log size) time. Items are (length, position) pairs, so "largest"
    means longest, and the position says where that sequence ends.
    """

    def __init__(self, size):
        self.tree = [(0, -1)] * (size + 1)

    def update(self, rank, item):
        while rank < len(self.tree):
            if item > self.tree[rank]:
                self.tree[rank] = item
            rank += rank & -rank          # move to the next range that covers rank

    def best(self, rank):
        result = (0, -1)                  # (0, -1) means "no sequence"
        while rank > 0:
            if self.tree[rank] > result:
                result = self.tree[rank]
            rank -= rank & -rank          # move to the range just before this one
        return result


def longest_alternating(a, b):
    """Return one longest valid sequence as a list of (array, position, value), positions from 1.

    A valid sequence takes its elements alternately from A and B. Its values
    increase, and every element sits at a later position (index in its own
    array) than the element before it sits in the other array.

    len_a[t] is the length of the longest valid sequence that ends with a[t]:
        len_a[t] = 1 + max(len_b[q] for q < t with b[q] < a[t])   (1 if there is none)
    and len_b[t] is defined the same way with A and B swapped.

    Positions are processed in increasing order. ends_in_a and ends_in_b hold the
    sequences found so far that end in A and in B, indexed by the value of their
    last element, so "longest one with last value < v" is a single best() call.
    Total time O((i + j) log(i + j)) for arrays of sizes i and j.
    """
    rank = {value: r for r, value in enumerate(sorted(set(a) | set(b)), start=1)}
    ends_in_a = PrefixMax(len(rank))
    ends_in_b = PrefixMax(len(rank))
    # prev_a[t] is the position in B of the element before a[t] (-1: a[t] starts the
    # sequence); prev_b[t] is the position in A of the element before b[t].
    len_a, prev_a = [0] * len(a), [-1] * len(a)
    len_b, prev_b = [0] * len(b), [-1] * len(b)

    for t in range(max(len(a), len(b))):
        # Work out a[t] and b[t] before storing either, so that two elements at
        # the same position can never follow each other.
        if t < len(a):
            length, position = ends_in_b.best(rank[a[t]] - 1)     # b[q] < a[t], q < t
            len_a[t], prev_a[t] = length + 1, position
        if t < len(b):
            length, position = ends_in_a.best(rank[b[t]] - 1)     # a[p] < b[t], p < t
            len_b[t], prev_b[t] = length + 1, position
        if t < len(a):
            ends_in_a.update(rank[a[t]], (len_a[t], t))
        if t < len(b):
            ends_in_b.update(rank[b[t]], (len_b[t], t))

    ends = [(len_a[t], "A", t) for t in range(len(a))] + [(len_b[t], "B", t) for t in range(len(b))]
    if not ends:
        return []
    # Walk back from the end of a longest sequence, switching arrays at every step.
    _, array, t = max(ends)
    sequence = []
    while t != -1:
        if array == "A":
            sequence.append(("a", t + 1, a[t]))
            array, t = "B", prev_a[t]
        else:
            sequence.append(("b", t + 1, b[t]))
            array, t = "A", prev_b[t]
    return sequence[::-1]


def read_arrays(path):
    """Return the lists A and B from an input file."""
    with open(path, encoding="utf-8-sig") as f:
        tokens = f.read().split()
    size_a, size_b = int(tokens[0]), int(tokens[1])
    values = [int(token) for token in tokens[2:]]
    return values[:size_a], values[size_a:size_a + size_b]


def expand_wildcards(args):
    """Expand names such as longest_seq*.txt, which PowerShell and cmd pass on unexpanded."""
    paths = []
    for arg in args:
        matches = sorted(glob.glob(arg), key=lambda path: (len(path), path))
        paths.extend(matches or [arg])
    return paths


def main():
    args = sys.argv[1:]
    show = "--show" in args
    paths = expand_wildcards([arg for arg in args if arg != "--show"])
    if not paths:
        print("Usage: python longest_seq.py longest_seq1.txt [more input files ...] [--show]")
        sys.exit(2)
    for index, path in enumerate(paths):
        if index > 0:
            print()
        sequence = longest_alternating(*read_arrays(path))
        print(f"File Input: {os.path.basename(path)}")
        print(f"Longest Sequence: {len(sequence)}")
        if show:
            print("X = " + " ".join(str(value) for _, _, value in sequence))
            print("    from " + ", ".join(f"{array}_{position}" for array, position, _ in sequence))


if __name__ == "__main__":
    main()
