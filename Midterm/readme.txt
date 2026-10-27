CS526 Midterm
Jia Chen
================================================================================

CONTENTS

  1. Files
  2. How to run (all problems)
  3. Problem 1 - Snowfall              snowfall.py
  4. Problem 2 - Pandemic              pandemic.py
  5. Problem 3 - Symbol Puzzle Game    puzzle_game.py
  6. Testing


================================================================================
1. FILES
================================================================================

  snowfall.py                    Problem 1 program
  pandemic.py                    Problem 2 program
  puzzle_game.py                 Problem 3 program
  run_tests.py                   runs and checks all input files (section 6)
  readme.txt                     this file
  README.md                      the same information, formatted for GitHub

  snowfall_input1.txt - 5.txt    Problem 1 inputs (input5: an extra n = 3 case)
  pandemic_input1.txt - 2.txt    Problem 2 inputs
  puzzle_game_input1.txt - 4.txt Problem 3 inputs (inputs 3 and 4 are 4x4)

  answers_snowfall.txt           expected results for run_tests.py
  answers_pandemic.txt
  answers_puzzle_game.txt
  <problem>_output<id>.txt       program outputs, written by run_tests.py


================================================================================
2. HOW TO RUN (ALL PROBLEMS)
================================================================================

Requirements: Python 3.8 or newer. Only the Python standard library is used,
so there is nothing to install. Check the version with:

    python --version

Step 1. Open a terminal window and go to the Midterm folder:

    cd path/to/CS526/Midterm

Step 2. Run a program with the input file name after it, for example:

    python snowfall.py snowfall_input1.txt

This form works the same in every terminal: Windows PowerShell, Windows Command
Prompt, Git Bash, macOS and Linux. On macOS and Linux, type python3 instead of
python if python is not found.

The programs also read standard input when no file name is given:

    python snowfall.py < snowfall_input1.txt              (Command Prompt, bash)
    Get-Content snowfall_input1.txt | python snowfall.py  (PowerShell)

PowerShell does not support "<", which is why it needs the Get-Content form.

The exact commands used for every result in this file are listed in the
"How to run" part of each problem below.


================================================================================
3. PROBLEM 1 - SNOWFALL  (snowfall.py)
================================================================================

Heart of the algorithm
----------------------
The array already holds running totals, so the snowfall of any three
consecutive days takes a single subtraction:

    snowfall on days i, i+1, i+2  =  A[i+2] - A[i-1]        (with A[0] = 0)

The program slides this three-day window from days 1-3 up to days (n-2)-n and
compares each window with the total snowfall A[n]. It answers YES as soon as
one window satisfies

    2 * window > A[n]

This means "window is strictly more than half of A[n]", but it needs no
division, so a window of exactly half is always judged correctly as NO. If no
window passes, or if n < 3 (there is no window at all), the answer is NO.

Running time: O(n), one pass over the array. Memory: O(n).

Example, snowfall_input1.txt: A = 1 4 10 14 15 17 17 23, total 23, half 11.5

    days 1-3:  A[3] - A[0] = 10 - 0 = 10      2 * 10 = 20 > 23?  no
    days 2-4:  A[4] - A[1] = 14 - 1 = 13      2 * 13 = 26 > 23?  yes  -> YES

Explanation of the code
-----------------------
has_heavy_window(totals)
    totals holds A[1..n]. The line  A = [0] + totals  puts a 0 in front, so
    the list indexes match the problem exactly: A[0] = 0, A[1] = day 1, and so
    on. The loop  for i in range(1, n - 1)  visits the windows that start on
    days 1 to n-2. It returns True at the first window where
    2 * (A[i + 2] - A[i - 1]) > A[n], and False if n < 3 or no window passes.

solve(text)
    Splits the file into lines, reads n from line 1 and the n values after
    it. The values are read with Fraction, which stores whole numbers and
    decimal totals such as 2.5 exactly (no float rounding). It returns the
    output line, showing the values exactly as written in the file:
        <input> solution: <YES|NO>

main()
    Runs solve() on every file name given on the command line, so all the
    inputs can be tested in one run. With no file name it reads standard
    input.

How to run
----------
All five inputs in a single run (the exact command used for the results):

    python snowfall.py snowfall_input1.txt snowfall_input2.txt snowfall_input3.txt snowfall_input4.txt snowfall_input5.txt

One input at a time:

    python snowfall.py snowfall_input1.txt

Results
-------
    1 4 10 14 15 17 17 23 solution: YES
    44 127 166 231 238 320 363 429 500 511 577 642 689 764 812 886 solution: NO
    3 8 14 19 21 24 25 25 32 solution: NO
    1 2 3 4 5 solution: YES
    1 2 3 solution: YES

The first four lines match the expected results given in the assignment.

    Input  Total  Half   Deciding window
    1      23     11.5   days 2-4 = 13, more than half                -> YES
    2      886    443    largest is days 14-16 = 197, below half      -> NO
    3      32     16     largest is days 2-4 = 16, EXACTLY half       -> NO
    4      5      2.5    days 1-3 = 3, more than half                 -> YES
    5      3      1.5    days 1-3 = 3, the only window (n = 3)        -> YES

Input 3 tests the "strictly more than half" rule: days 2-4 give
19 - 3 = 16, exactly half of 32, so the answer is NO.
Input 5 is not in the assignment's list. With n = 3 there is exactly one
window, days 1-3, and it holds all of the snow, so the answer is YES.


================================================================================
4. PROBLEM 2 - PANDEMIC  (pandemic.py)
================================================================================

Heart of the algorithm
----------------------
The state is an N x N grid of True (infected) and False (healthy). Each day:

  1. Find every healthy county with at least two infected neighbors
     (up, down, left, right; diagonal counties are not neighbors).
  2. Only after the whole list for that day is found, mark them all infected.

Doing step 2 after step 1 is what makes all counties update at the same time:
a county infected today cannot help infect another county until tomorrow.
The simulation stops on the first day with no new infections. If any county
is still False at that point, there are healthy counties left.

Which counties need checking: a healthy county's number of infected neighbors
only goes up when one of its neighbors becomes infected. So each day the
program checks only the healthy neighbors of the counties infected the day
before (on the first step, the neighbors of the initially infected counties),
instead of scanning the whole grid every day.

Running time: every county is infected at most once, and each new infection
leads to at most 4 neighbor checks of 4 cells each, so the whole simulation
takes O(N^2) time, proportional to the number of counties. Memory: O(N^2).
Scanning the full grid each day would cost O(N^2) per day instead. For
example, a 1000 x 1000 grid with only the diagonal infected keeps spreading
for 999 days until every county is infected; this program finishes it in
about 5 seconds, while a full scan would check 1,000,000 counties on each of
those days.

Explanation of the code
-----------------------
neighbors(r, c, n)
    Yields the counties directly above, below, left and right of (r, c),
    skipping any that would fall outside the grid.

new_infections(grid, recent)
    candidates is the set of healthy neighbors of the counties in recent.
    A set is used so that a county next to two recent infections is checked
    only once. For each candidate, sum(...) counts its infected neighbors
    (True counts as 1, False as 0), and the candidates with 2 or more are
    returned. The grid itself is not changed here.

simulate(n, initial, show)
    Builds the grid, marks the initially infected counties and prints Day 1.
    Then it repeats: new = new_infections(grid, recent); if new is empty,
    stop; otherwise mark the new counties, add 1 to the day, print the board,
    and use new as recent for the next day. Returns the final grid.

print_board(day, grid)
    Prints the day number and the grid, X = infected, . = healthy.

read_input(text)
    Returns N from line 1 and the list of (row, column) pairs from the
    following lines.

main()
    Reads the file (or standard input), runs the simulation and prints the
    final message, which is always the last line of output. The optional
    --quiet flag hides the daily boards, which is useful for a large N.

How to run
----------
    python pandemic.py pandemic_input1.txt
    python pandemic.py pandemic_input2.txt

Final message only:

    python pandemic.py pandemic_input1.txt --quiet

Results
-------
python pandemic.py pandemic_input1.txt
(the same days as the example in the assignment)

    Day 1
    . . . . .
    . . . X .
    . . X . .
    . . . . X
    . . . . .

    Day 2
    . . . . .
    . . X X .
    . . X X .
    . . . . X
    . . . . .

    Day 3
    . . . . .
    . . X X .
    . . X X X
    . . . X X
    . . . . .

    Day 4
    . . . . .
    . . X X X
    . . X X X
    . . X X X
    . . . . .

    Day 5: no new counties are infected, so the infection has stopped spreading.

    There are healthy counties left

python pandemic.py pandemic_input2.txt

    Day 1
    . . X . X
    . X . . X
    . . X . .
    X . . X .
    . . X . .

    Day 2
    . X X X X
    . X X . X
    . X X X .
    X . X X .
    . . X X .

    Day 3
    . X X X X
    . X X X X
    X X X X X
    X X X X .
    . . X X .

    Day 4
    . X X X X
    X X X X X
    X X X X X
    X X X X X
    . X X X .

    Day 5
    X X X X X
    X X X X X
    X X X X X
    X X X X X
    X X X X X

    Day 6: no new counties are infected, so the infection has stopped spreading.

    There are no healthy counties left

Both final messages match the expected results given in the assignment.


================================================================================
5. PROBLEM 3 - SYMBOL PUZZLE GAME  (puzzle_game.py)
================================================================================

Heart of the algorithm
----------------------
The board is read once, cell by cell. Three lists of sets remember which
symbols have been seen so far:

    rows[r]    symbols already seen in row r
    cols[c]    symbols already seen in column c
    boxes[b]   symbols already seen in sub-board b

For each non-empty cell (r, c) holding symbol v:

    - v is not one of the n listed symbols                  -> invalid
    - v is already in rows[r], cols[c] or boxes[b]          -> invalid
      (the symbol is repeated in that row, column or sub-board)
    - otherwise, add v to all three sets and go on

If every cell passes, the board is valid. Empty cells (.) are skipped, so
they never make the board invalid.

Which sub-board a cell is in: with k = sqrt(n) (k = 2 for 4x4, k = 3 for 9x9)

    b = (r // k) * k + (c // k)

r // k is the sub-board's row and c // k is its column. For a 9x9 board the
sub-boards are numbered:

                 cols 0-2   cols 3-5   cols 6-8
    rows 0-2        0          1          2
    rows 3-5        3          4          5
    rows 6-8        6          7          8

For example, cell (4, 7) is in sub-board (4 // 3) * 3 + (7 // 3) = 3 + 2 = 5.

Running time: O(n^2). Each of the n x n cells is visited once, and each set
lookup or insert takes O(1) time. Memory: O(n^2) for the sets. The program
stops at the first broken rule.

Explanation of the code
-----------------------
read_input(text)
    Line 1 gives n. Line 2 is split at the commas to get the list of symbols.
    The next n lines are split at the commas to get the board as a list of
    rows. Spaces around values are removed and blank lines are skipped.

is_valid(n, symbols, board)
    k = isqrt(n) is the sub-board size. allowed = set(symbols) makes the
    "is this a listed symbol" check O(1). rows, cols and boxes are lists of n
    empty sets. The two nested loops visit every cell and apply the checks
    described above, returning False at the first problem and True at the
    end. EMPTY = "." marks an empty cell.

main()
    Reads the file (or standard input) and prints "The board is valid" or
    "The board is invalid".

How to run
----------
    python puzzle_game.py puzzle_game_input1.txt
    python puzzle_game.py puzzle_game_input2.txt
    python puzzle_game.py puzzle_game_input3.txt
    python puzzle_game.py puzzle_game_input4.txt

Results
-------
    Input                    Output                 Reason
    puzzle_game_input1.txt   The board is valid     no rule is broken (9x9)
    puzzle_game_input2.txt   The board is invalid   see below (9x9)
    puzzle_game_input3.txt   The board is valid     the 4x4 example board from
                                                    the assignment
    puzzle_game_input4.txt   The board is invalid   see below (4x4)

Inputs 1 and 2 match the expected results given in the assignment.

puzzle_game_input2.txt is input1 with one change: row 0, column 0 holds }
instead of %. That } is now repeated in column 0 (rows 0 and 3) and in the
top-left 3x3 sub-board (cells (0,0) and (2,2)).

puzzle_game_input4.txt is input3 with one change: row 1, column 1 holds @
instead of *. That @ is now repeated in the top-left 2x2 sub-board
(cells (0,0) and (1,1)).


================================================================================
6. TESTING
================================================================================

Running all the tests
---------------------
One command runs every program on all of its input files:

    python run_tests.py

For every snowfall_input<id>.txt, pandemic_input<id>.txt and
puzzle_game_input<id>.txt, run_tests.py:

  1. runs the matching program with the input file name as its argument
     (the same commands shown in sections 3 to 5),
  2. writes the full output to snowfall_output<id>.txt,
     pandemic_output<id>.txt or puzzle_game_output<id>.txt,
  3. compares the LAST line of the output with "answer <id>" in the
     problem's answer file, and
  4. prints PASS, FAIL or NO ANSWER, then a summary.

The last line is compared because, for Pandemic, the final message must be
the last line and the daily boards before it are optional. A program that
crashes is reported as FAIL with its error message. The exit code is 1 if any
test fails, 0 otherwise.

Result:

    PASS      snowfall_input1.txt: 1 4 10 14 15 17 17 23 solution: YES
    PASS      snowfall_input2.txt: 44 127 166 231 238 320 363 429 500 511 577 642 689 764 812 886 solution: NO
    PASS      snowfall_input3.txt: 3 8 14 19 21 24 25 25 32 solution: NO
    PASS      snowfall_input4.txt: 1 2 3 4 5 solution: YES
    PASS      snowfall_input5.txt: 1 2 3 solution: YES
    PASS      pandemic_input1.txt: There are healthy counties left
    PASS      pandemic_input2.txt: There are no healthy counties left
    PASS      puzzle_game_input1.txt: The board is valid
    PASS      puzzle_game_input2.txt: The board is invalid
    PASS      puzzle_game_input3.txt: The board is valid
    PASS      puzzle_game_input4.txt: The board is invalid

    11 passed, 0 failed, 0 without an answer

The assignment did not include answer files, so the answers_*.txt files were
written from the assignment text. Snowfall 1-4, Pandemic 1-2 and Puzzle 1-3
are the results stated in the assignment. Snowfall 5 and Puzzle 4 were worked
out by hand (see sections 3 and 5). Each answer file says this in its
# comment lines.

To add a test, save the input as the next number (for example
puzzle_game_input5.txt) and add a line such as "answer 5: The board is valid"
to the problem's answer file. run_tests.py finds new input files by itself.

Brute-force checks
------------------
Besides the sample inputs, each program was compared with a simple
brute-force version on random inputs, and all results matched:

  - Snowfall: 3,000 random arrays, including windows of exactly half, n < 3
    and decimal snowfall amounts.
  - Pandemic: 1,500 random grids (N = 1 to 9), compared with a version that
    scans the whole grid every day. Both the final grid and the number of
    days matched.
  - Puzzle: 3,000 random 1x1, 4x4 and 9x9 boards, including symbols that are
    not in the list, compared with a version that counts the symbols in every
    row, column and sub-board.

Every command in this file was also checked in Windows PowerShell, Windows
Command Prompt and Git Bash.
