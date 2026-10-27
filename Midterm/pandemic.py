"""Problem 2: spread the infection until it stops, then check for healthy counties.

Usage: python pandemic.py pandemic_input1.txt
       python pandemic.py pandemic_input1.txt --quiet    (final message only)
       python pandemic.py < pandemic_input1.txt

Input:  line 1 = N, then one "row column" line per initially infected county.
Output: the board for each day, then "There are healthy counties left" or
        "There are no healthy counties left" as the final line.
"""
import sys

STEPS = ((-1, 0), (1, 0), (0, -1), (0, 1))    # up, down, left, right


def neighbors(r, c, n):
    """Yield the counties directly above, below, left and right of (r, c) on an n x n grid."""
    for dr, dc in STEPS:
        nr, nc = r + dr, c + dc
        if 0 <= nr < n and 0 <= nc < n:
            yield nr, nc


def new_infections(grid, recent):
    """Return the healthy counties that become infected on the next day.

    A healthy county's number of infected neighbors only changes when one of its
    neighbors becomes infected. So only the healthy neighbors of the counties in
    recent (the ones infected most recently) need to be checked.
    """
    n = len(grid)
    candidates = {(nr, nc) for r, c in recent
                  for nr, nc in neighbors(r, c, n) if not grid[nr][nc]}
    # sum() of True/False values counts the True ones (True = 1, False = 0).
    return [(r, c) for r, c in candidates
            if sum(grid[nr][nc] for nr, nc in neighbors(r, c, n)) >= 2]


def print_board(day, grid):
    print(f"Day {day}")
    for row in grid:
        print(" ".join("X" if infected else "." for infected in row))
    print()


def simulate(n, initial, show=True):
    """Spread the infection day by day until it stops and return the final grid.

    grid[r][c] is True when county (r, c) is infected. Each day, all new
    infections are found first and only then marked on the grid, so a county
    infected today does not count as an infected neighbor until the next day.
    Each county is infected at most once and is checked only when a neighbor
    changes, so the whole run takes O(N^2) time.
    """
    grid = [[False] * n for _ in range(n)]
    for r, c in initial:
        grid[r][c] = True

    day = 1
    recent = initial
    if show:
        print_board(day, grid)
    while True:
        new = new_infections(grid, recent)
        if not new:
            break
        for r, c in new:
            grid[r][c] = True
        day += 1
        recent = new
        if show:
            print_board(day, grid)
    if show:
        print(f"Day {day + 1}: no new counties are infected, so the infection has stopped spreading.")
        print()
    return grid


def read_input(text):
    """Return N and the list of initially infected (row, column) counties."""
    lines = [line.split() for line in text.splitlines() if line.strip()]
    n = int(lines[0][0])
    initial = [(int(line[0]), int(line[1])) for line in lines[1:]]
    return n, initial


def main():
    args = sys.argv[1:]
    show = "--quiet" not in args
    files = [arg for arg in args if arg != "--quiet"]
    if files:
        with open(files[0], encoding="utf-8-sig") as f:
            text = f.read()
    else:
        # Decode as UTF-8 and drop the byte order mark that a PowerShell pipe can add.
        text = sys.stdin.buffer.read().decode("utf-8-sig")

    n, initial = read_input(text)
    grid = simulate(n, initial, show)
    if any(not infected for row in grid for infected in row):
        print("There are healthy counties left")
    else:
        print("There are no healthy counties left")


if __name__ == "__main__":
    main()
