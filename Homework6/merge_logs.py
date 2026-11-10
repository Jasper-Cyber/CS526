"""Problem 1: merge the sorted sales logs of k registers with a priority queue.

Usage: python merge_logs.py < merge/merge_input1.txt               (bash, Command Prompt)
       Get-Content merge/merge_input1.txt | python merge_logs.py   (PowerShell)
       python merge_logs.py merge/merge_input1.txt                  (any shell)
       python merge_logs.py merge/merge_input*.txt                  (several files)

Input:  one register per line, each a list of sale times in increasing order,
        for example [3, 9, 14]. An empty log is written []. Registers are
        numbered from 1 in the order their lines appear.
Output: Registers: 4
        Total sales: 8
        Merged log: [(1, 2), (3, 1), (5, 4), (9, 1), (9, 2), (14, 1), (20, 2), (25, 2)]
"""
import ast
import glob
import sys


class PriorityQueue:
    """Binary min-heap of comparable entries, kept in a Python list.

    merge_logs stores (time, register, position) tuples in it. Entry i has its
    children at 2i + 1 and 2i + 2 and its parent at (i - 1) // 2.
    Entries compare as tuples: by time, and for equal times by register number,
    so the lower-numbered register comes out first. position (the index of the
    sale in its register's log) is never reached in a comparison: the queue holds
    at most one entry per register, so no two entries share (time, register).
    push and pop each take O(log m) time for a queue of m entries.
    """

    def __init__(self):
        self._entries = []

    def __len__(self):
        return len(self._entries)

    def push(self, entry):
        """Add entry, then move it up while it is smaller than its parent."""
        entries = self._entries
        entries.append(entry)
        child = len(entries) - 1
        while child > 0:
            parent = (child - 1) // 2
            if not entries[child] < entries[parent]:
                break
            entries[child], entries[parent] = entries[parent], entries[child]
            child = parent

    def pop(self):
        """Remove and return the smallest entry. Raise IndexError if the queue is empty."""
        entries = self._entries
        if not entries:
            raise IndexError("pop from an empty priority queue")
        smallest = entries[0]
        last = entries.pop()
        if entries:
            entries[0] = last          # move the last entry to the top, then sift it down
            self._sift_down(0)
        return smallest

    def _sift_down(self, parent):
        entries = self._entries
        count = len(entries)
        while True:
            smallest = parent
            for child in (2 * parent + 1, 2 * parent + 2):
                if child < count and entries[child] < entries[smallest]:
                    smallest = child
            if smallest == parent:
                return
            entries[parent], entries[smallest] = entries[smallest], entries[parent]
            parent = smallest


def merge_logs(logs):
    """Merge sorted logs into one list of (time, register) pairs, sorted by time.

    Registers are numbered from 1. Equal times come out lowest register first.
    The queue starts with the first sale of every non-empty log. Each step pops
    the earliest sale, appends it to the result and pushes the next sale from
    the same register, if there is one. A register therefore never has more
    than one entry in the queue, and the queue never holds more than k entries.
    For N sales in total: O(N log k) time and O(k) memory besides the result.
    """
    queue = PriorityQueue()
    for register, log in enumerate(logs, start=1):
        if log:
            queue.push((log[0], register, 0))
    merged = []
    while len(queue) > 0:
        time, register, position = queue.pop()
        merged.append((time, register))
        log = logs[register - 1]
        if position + 1 < len(log):
            queue.push((log[position + 1], register, position + 1))
    return merged


def read_logs(text):
    """Return the logs in text, one per non-blank line, checking that each is a sorted list of numbers."""
    logs = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        register = len(logs) + 1
        try:
            log = ast.literal_eval(line)
        except (ValueError, SyntaxError):
            log = None
        if not isinstance(log, list) or not all(is_number(time) for time in log):
            raise ValueError(f"register {register} is not a list of numbers: {line}")
        for before, after in zip(log, log[1:]):
            if after < before:
                raise ValueError(f"register {register} is not in increasing order: "
                                 f"{after} comes after {before}")
        logs.append(log)
    return logs


def is_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def expand_wildcards(args):
    """Expand names such as merge/merge_input*.txt, which PowerShell and cmd pass on unexpanded.

    The matches come out in numeric order (input2 before input10): they go through
    the PriorityQueue above keyed on (length, name), since sort() is not allowed.
    """
    paths = []
    for arg in args:
        queue = PriorityQueue()
        for match in glob.glob(arg):
            queue.push((len(match), match))
        if len(queue) == 0:
            paths.append(arg)          # no match: keep the name, so the error message shows it
        while len(queue) > 0:
            paths.append(queue.pop()[1])
    return paths


def read_text(path):
    """Return the text of the file at path, or of standard input when path is None.

    Both are decoded as UTF-8, skipping the byte order mark some Windows editors
    put at the start of a file (standard input is read as bytes, because Windows
    would otherwise decode it with the local code page).
    """
    if path is None:
        if sys.stdin.isatty():
            print("Type one log per line, then Ctrl+D (macOS/Linux) or Ctrl+Z and Enter (Windows):",
                  file=sys.stderr)
        return sys.stdin.buffer.read().decode("utf-8-sig", errors="replace")
    with open(path, encoding="utf-8-sig", errors="replace") as f:
        return f.read()


def main():
    paths = expand_wildcards(sys.argv[1:]) or [None]
    status = 0
    for index, path in enumerate(paths):
        if len(paths) > 1:
            if index > 0:
                print()
            print(f"File Input: {path}")
        try:
            logs = read_logs(read_text(path))
        except (OSError, ValueError) as error:
            print(f"Error: {error}", file=sys.stderr)
            status = 1
            continue
        merged = merge_logs(logs)
        print(f"Registers: {len(logs)}")
        print(f"Total sales: {len(merged)}")
        print(f"Merged log: {merged}")
    sys.exit(status)


if __name__ == "__main__":
    main()
