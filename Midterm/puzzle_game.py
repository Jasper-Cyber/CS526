"""Problem 3: decide whether a symbol puzzle board is in a valid state.

Usage: python puzzle_game.py puzzle_game_input1.txt
       python puzzle_game.py < puzzle_game_input1.txt

Input:  line 1 = n, line 2 = the n symbols separated by commas,
        then n rows of n comma-separated values ("." is an empty cell).
Output: "The board is valid" or "The board is invalid"
"""
import sys
from math import isqrt

EMPTY = "."


def is_valid(n, symbols, board):
    """Return True if the board breaks none of the rules.

    The board is read once, cell by cell. Every row, column and sub-board has a
    set of the symbols already seen in it. A cell is a problem if its symbol is
    not one of the listed symbols, or if it is already in the set of its row,
    its column or its sub-board. Empty cells are skipped.

    With k = sqrt(n), cell (r, c) is in sub-board (r // k) * k + c // k, which
    numbers the sub-boards 0 .. n-1 from left to right, top to bottom.
    O(n^2) time and memory: each cell is checked once with set lookups.
    """
    k = isqrt(n)
    allowed = set(symbols)
    rows = [set() for _ in range(n)]
    cols = [set() for _ in range(n)]
    boxes = [set() for _ in range(n)]

    for r in range(n):
        for c in range(n):
            value = board[r][c]
            if value == EMPTY:
                continue
            if value not in allowed:
                return False
            b = (r // k) * k + c // k
            if value in rows[r] or value in cols[c] or value in boxes[b]:
                return False
            rows[r].add(value)
            cols[c].add(value)
            boxes[b].add(value)
    return True


def read_input(text):
    """Return n, the list of symbols and the board as a list of rows."""
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    n = int(lines[0])
    symbols = [value.strip() for value in lines[1].split(",")]
    board = [[value.strip() for value in line.split(",")] for line in lines[2:n + 2]]
    return n, symbols, board


def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1], encoding="utf-8-sig") as f:
            text = f.read()
    else:
        # Decode as UTF-8 and drop the byte order mark that a PowerShell pipe can add.
        text = sys.stdin.buffer.read().decode("utf-8-sig")

    n, symbols, board = read_input(text)
    print("The board is valid" if is_valid(n, symbols, board) else "The board is invalid")


if __name__ == "__main__":
    main()
