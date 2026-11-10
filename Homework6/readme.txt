CS526 Homework 6
Jia Chen
================================================================================

CONTENTS

  1. Files
  2. How to run (all problems)
  3. Problem 1 - Merge k sorted lists        merge_logs.py
  4. Problem 2 - Implement a heap            linked_heap.py
  5. Problem 3 - Running median              running_median.py
  6. Testing                                 run_tests.py


================================================================================
1. FILES
================================================================================

  merge_logs.py                  Problem 1 program
  linked_heap.py                 Problem 2 program
  running_median.py              Problem 3 program (imports MinHeap from
                                 linked_heap.py)
  run_tests.py                   tests all three problems (section 6)
  readme.txt                     this file
  README.md                      the same information, formatted for GitHub
  homework6.txt                  the assignment

Each problem's input and output files are kept in their own folder:

  merge/   merge_input1.txt - 9.txt       Problem 1 inputs
           merge_output<id>.txt           outputs written by run_tests.py
           problem1_answers.txt           expected summary of each output
  heap/    heap_input1.txt - 10.txt       Problem 2 inputs
           heap_output<id>.txt
           heap_demo_output.txt           the other methods, shown with --demo
           problem2_answers.txt
  median/  median_input1.txt - 11.txt     Problem 3 inputs
           median_output<id>.txt
           problem3_answers.txt


================================================================================
2. HOW TO RUN (ALL PROBLEMS)
================================================================================

Requirements: Python 3.7 or newer. Only the Python standard library is used,
so there is nothing to install. Check the version with:

    python --version

Step 1. Open a terminal window and go to the Homework6 folder:

    cd path/to/CS526/Homework6

Step 2. The programs read STANDARD INPUT. How to send a file to standard input
depends on the terminal:

    Git Bash, macOS, Linux:  python merge_logs.py < merge/merge_input1.txt
    Command Prompt:          python merge_logs.py < merge\merge_input1.txt
    PowerShell:              Get-Content merge/merge_input1.txt | python merge_logs.py

PowerShell has no "<" operator, which is why it needs Get-Content and a pipe.

The programs also accept file names as arguments. This works the same in
every terminal:

    python merge_logs.py merge/merge_input1.txt
    python linked_heap.py heap/heap_input1.txt
    python running_median.py median/median_input1.txt
    python running_median.py median/median_input*.txt
    python run_tests.py

With more than one file, each output starts with a "File Input: <file name>"
line. The programs expand "*" themselves, because PowerShell and Command
Prompt pass it through unchanged. On macOS and Linux, type python3 instead of
python if python is not found.

Run with no input file, a program waits for the input to be typed. End it
with Ctrl+D (macOS, Linux) or Ctrl+Z and Enter (Windows).

A line that is not a list of numbers, or a register log that is not in
increasing order, stops the program with a message such as:

    Error: register 1 is not in increasing order: 1 comes after 3


================================================================================
3. PROBLEM 1 - MERGE K SORTED LISTS  (merge_logs.py)
================================================================================

How to run
----------
    python merge_logs.py < merge/merge_input1.txt

Input, one register per line ([] is an empty log):

    [3, 9, 14]
    [1, 9, 20, 25]
    []
    [5]

Output:

    Registers: 4
    Total sales: 8
    Merged log: [(1, 2), (3, 1), (5, 4), (9, 1), (9, 2), (14, 1), (20, 2), (25, 2)]

Solution and algorithm
----------------------
Each register's log is already sorted, so the next sale of the merged log is
always the first not-yet-merged sale of SOME register. A priority queue holds
exactly those candidates, at most one per register:

  1. Push the first sale of every non-empty log as (time, register, position).
  2. Pop the smallest entry and append (time, register) to the result.
  3. If that register has another sale, push (next time, register,
     position + 1).
  4. Repeat steps 2 and 3 until the queue is empty.

Equal times: entries are compared as tuples, first by time and then by
register number, so for equal times the lower-numbered register comes out
first. Sales from the same register keep their order, because a register's
next sale is pushed only after the previous one is popped.

The k-entry rule: a register's entry is pushed only after its previous entry
is popped. So the queue never holds two entries from one register, and never
more than k entries. run_tests.py checks this on every push.

Worked example, the assignment's input:

    step   pop       push (same register)    queue afterwards
    start  -         (3,1) (1,2) (5,4)        (1,2) (3,1) (5,4)
    1      (1, 2)    (9, 2)                   (3,1) (5,4) (9,2)
    2      (3, 1)    (9, 1)                   (5,4) (9,1) (9,2)
    3      (5, 4)    - (register 4 is done)   (9,1) (9,2)
    4      (9, 1)    (14, 1)                  (9,2) (14,1)
    5      (9, 2)    (20, 2)                  (14,1) (20,2)
    6      (14, 1)   -                        (20,2)
    7      (20, 2)   (25, 2)                  (25,2)
    8      (25, 2)   -                        (empty)

Step 4 shows the tie rule: (9, 1) comes before (9, 2). Register 3 is empty, so
the queue never holds more than 3 entries.

The priority queue
------------------
PriorityQueue is my own binary min-heap kept in a Python list. Entry i has its
children at 2i + 1 and 2i + 2 and its parent at (i - 1) // 2.
  push(entry)  append it, then swap it with its parent while it is smaller.
  pop()        take the top entry, move the last entry to the top, then swap
               it with its smaller child while a child is smaller.
Both take O(log k) time. heapq, sort() and sorted() are not used.

Complexity: for k registers and N sales in total, O(N log k) time (each sale
is pushed and popped once) and O(k) memory for the queue. With 50 registers
and 20,737 sales (merge_input9.txt) the queue holds at most 50 entries.

Explanation of the code
-----------------------
PriorityQueue        the min-heap described above.
merge_logs(logs)     the algorithm; returns the merged list.
read_logs(text)      reads one log per non-blank line and checks that it is a
                     list of numbers in increasing order.
main()               reads standard input (or the files named on the command
                     line) and prints the three output lines.


================================================================================
4. PROBLEM 2 - IMPLEMENT A HEAP  (linked_heap.py)
================================================================================

How to run
----------
    python linked_heap.py < heap/heap_input1.txt

Output for the input [8, 3, 5, 1], the same as in the assignment:

    Input values: [8, 3, 5, 1]

    After insert(8):
      8

    After insert(3):
        3
       /
      8

    After insert(5):
        3
       / \
      8   5

    After insert(1):
            1
          /   \
        3       5
       /
      8

Add --demo to also try every other method on the same values: build, peek,
len, is_empty, heap_sort, delete (a value in the heap and one that is not),
extract_min until the heap is empty, and the IndexError from peek and
extract_min on an empty heap. run_tests.py saves this in
heap/heap_demo_output.txt.

    python linked_heap.py --demo heap/heap_input7.txt

The ADTs
--------
Node     holds a value and three links: left, right and parent.
MinHeap  holds only the root node and the number of values. It never stores
         its values in a list or an array. After every method call:
           - heap order: every node's value is <= its children's values, so
             the smallest value is at the root;
           - complete shape: every level is full except possibly the last,
             which is filled from the left.

Finding a position in O(log n)
------------------------------
Positions are numbered 1, 2, 3, ... in level order. Because the shape is
complete, n values always fill exactly positions 1 to n, so the next free spot
is position n + 1, the last node is position n, the parent of position p is
p // 2, and p is a left child when p is even.

The binary digits of p after the leading 1 are the path from the root:
0 = go left, 1 = go right. Example: 6 = 110, so right, then left. _node_at(p)
follows these digits and reaches any position in O(log n) steps.

                 1
             /       \
         2 = 10      3 = 11
         /   \        /   \
     4=100  5=101  6=110  7=111

The methods
-----------
insert(value)    Attach a new node at position n + 1, as a child of
                 _node_at((n + 1) // 2). Then move the value up while it is
                 STRICTLY smaller than its parent's value.        O(log n)
peek()           Return the root's value. IndexError if empty.    O(1)
extract_min()    Save the root's value. Unlink the last node (position n),
                 move its value into the root, and move it down while a child
                 is strictly smaller (the smaller child; the left one on a
                 tie). IndexError if empty.                       O(log n)
delete(value)    Find a node holding the value, then remove it like
                 extract_min: the last node's value replaces it and moves up
                 or down, since it can be too small or too large for its new
                 place. Returns True, or False if the value is not in the
                 heap.                O(n) to find, O(log n) to remove
build(values)    Replace the contents with values. The nodes are linked in
                 level order and each subtree is made into a heap bottom-up:
                 both child subtrees first, then the subtree's root moves
                 down.                                            O(n)
heap_sort()      Copy the tree and call extract_min on the copy until it is
                 empty. The heap itself is not changed.           O(n log n)
is_empty(), len(heap)   Use the stored count.                     O(1)
print_heap()     Draw the tree, root at the top (see below).      O(n)

delete needs O(n) to find a value because a heap is ordered only from top to
bottom, not from left to right. Still, every value in a subtree is at least
its root, so _find skips any subtree whose root is larger than the value.

build is O(n): half of the nodes are leaves and never move, a quarter move
down at most 1 level, an eighth at most 2, and so on. The total,
n/4*1 + n/8*2 + n/16*3 + ..., is less than n. Building with n separate
inserts would take O(n log n).

Drawing the tree
----------------
Each level is drawn on one line, with a line of / and \ between levels. The
bottom level has a slot every 4 columns, and each level above has slots twice
as far apart, so every parent is exactly halfway between its two children.
Each value is centered on its slot, and each / or \ is drawn halfway between
a parent and its child. Last tree of heap/heap_output5.txt:

    After insert(10):
                    10
                 /       \
            60              20
           /   \           /   \
        90      70      50      30
        / \     / \     / \     / \
      150 120 130 80  140 100 110 40

Values up to 3 characters wide fit in 4-column slots. If a value is wider, the
slots widen to the next multiple of 4 that leaves at least one space between
values, so the drawing stays correct for any numbers.

Example with duplicates, heap/heap_input7.txt = [5, 3, 5, 1, 3, 5, 1, 1, 3].
On the 7th insert, the new 1 is placed at position 7 under 5, swaps with that
5, and then stops below the root 1, because it is not strictly smaller:

    After insert(5):              After insert(1):
            1                             1
          /   \                         /   \
        3       5                     3       1
       / \     /                     / \     / \
      5   3   5                     5   3   5   5

Explanation of the code
-----------------------
Node, MinHeap        the ADTs. Helpers: _node_at, _sift_up, _sift_down,
                     _remove (shared by extract_min and delete), _find,
                     _build_subtree, _copy_subtree and draw.
show_inserts(values) the required output.
show_other_methods(values)   the --demo output.
parse_values, read_text, expand_wildcards   input handling, also used by
                     running_median.py.


================================================================================
5. PROBLEM 3 - RUNNING MEDIAN  (running_median.py)
================================================================================

How to run
----------
    python running_median.py < median/median_input1.txt

Output for the input [5, 15, 2, 4, 8]:

    [5.0, 10.0, 5.0, 4.5, 5.0]

An empty list [] prints [].

How the solution uses my heap
-----------------------------
The sales so far are split into two halves, each kept in a MinHeap from
Problem 2 (the class is imported from linked_heap.py, not replaced):

    lower   the smaller half of the sales, stored NEGATED.
            Its root is minus the largest sale of the smaller half.
    upper   the larger half of the sales.
            Its root is the smallest sale of the larger half.

Storing the negatives turns the min-heap into a max-heap without changing
MinHeap: the smallest of the negatives is minus the largest sale. So
-lower.peek() is the largest sale of the smaller half.

What must stay true after each sale (for the median in O(1) time)
-----------------------------------------------------------------
  1. Every sale in lower is <= every sale in upper,
     that is, -lower.peek() <= upper.peek().
  2. The halves differ in size by at most one, and lower is the bigger one:
     len(lower) == len(upper)  or  len(lower) == len(upper) + 1.

Together these mean the one or two middle sales are always at the two roots:
  odd count:   median = -lower.peek()
  even count:  median = (-lower.peek() + upper.peek()) / 2
peek() is O(1), so the median is available in O(1) time after every sale.

Overall algorithm and approach, for each new sale
-------------------------------------------------
  1. Put it in the right half: if lower is empty or the sale is
     <= -lower.peek(), insert -sale into lower; otherwise insert the sale
     into upper. This keeps invariant 1.
  2. Rebalance: if lower now has 2 more values than upper, move its root to
     upper; if upper has more values than lower, move its root to lower. The
     moved value is the one nearest the middle, so invariant 1 still holds,
     and invariant 2 is restored.
  3. Read the median from the two roots, as above, and add it to the output.

Each sale costs at most 3 heap operations: O(log n) time per sale and
O(n log n) for n sales, with O(n) memory. The sales are never kept in a sorted
list or re-sorted, and heapq, sort(), sorted() and statistics are not used.

Worked example, the assignment's input [5, 15, 2, 4, 8]:

    sale   smaller half (lower)   larger half (upper)   median
    5      5                      -                     5.0
    15     5                      15                    (5 + 15) / 2 = 10.0
    2      2, 5                   15                    5.0
    4      2, 4                   5, 15                 (4 + 5) / 2 = 4.5
    8      2, 4, 5                8, 15                 5.0

When 4 arrives it goes into the smaller half, which then has 3 values against
1, so its largest value, 5, moves to the larger half.

Explanation of the code
-----------------------
RunningMedian            the two heaps, with add(amount) and median().
running_medians(sales)   returns the list of medians, one after each sale.
main()                   reads the list from standard input (or the files
                         named on the command line) and prints the medians.


================================================================================
6. TESTING  (run_tests.py)
================================================================================

    python run_tests.py

run_tests.py does four things:

  1. Rules: it reads the three programs with Python's ast module and fails if
     any of them imports heapq, queue, bisect or statistics, or calls sorted()
     or .sort().
  2. Random tests against simple reference methods:
     - Problem 1: 2,000 random sets of logs with many equal times, plus every
       input file, compared with sorted(). The program's PriorityQueue is
       replaced by a checking version that fails if it ever holds more than k
       entries or two entries from the same register.
     - Problem 2: 100 runs of 200 random calls of every method, compared with
       a sorted list. After each call it checks every parent link, the heap
       order, the complete shape, and that print_heap draws each value in its
       place. It also checks that the heap keeps its values only in nodes.
     - Problem 3: 500 random sale lists, compared with the median of a sorted
       list. After every sale it checks that both halves are MinHeaps from
       Problem 2 and that the two invariants hold.
  3. Every input file: it runs each program on every
     <folder>/<name>_input<id>.txt through standard input and saves the
     output next to it as <name>_output<id>.txt. Each output is checked
     against a reference (sorted() for Problem 1, a sorted list for Problem 3,
     and for Problem 2 an array heap that replays the same inserts, with
     every drawn tree checked level by level).
  4. Answer files: it summarizes each output in the format of the folder's
     answer file, for example "4 registers, 8 sales, first (1, 2), last
     (25, 2)", and compares it with the line "1-1: ..." in
     problem1_answers.txt. It prints PASS, FAIL, NO ANSWER or NO INPUT for
     each test, then a summary. A crash is reported as FAIL with its error
     message. The exit code is 1 if any test fails, 0 otherwise.

Result (takes about 8 seconds):

    PASS      rules: no heapq, queue, bisect, statistics, sorted() or .sort() in the programs
    PASS      merge_logs.py: 2000 random merges and all input files match sorted(); ...
    PASS      linked_heap.py: 100 runs of 200 random calls of every method match a sorted list; ...
    PASS      linked_heap.py: the heap is stored only in linked nodes (value, left, right, parent)
    PASS      running_median.py: uses MinHeap from linked_heap.py; 500 random sale lists ...
    PASS      linked_heap.py --demo heap/heap_input7.txt: every method shown, ...
    PASS      merge/merge_input1.txt: 4 registers, 8 sales, first (1, 2), last (25, 2)
    ...       (merge_input2 - 9)
    PASS      heap/heap_input1.txt: 4 values, 3 levels, root 1
    ...       (heap_input2 - 10)
    NO INPUT  2-11 in heap/problem2_answers.txt: heap/heap_input11.txt does not exist
    PASS      median/median_input1.txt: 5 sales, final median 5.0
    ...       (median_input2 - 11)

    36 passed, 0 failed, 1 without an answer or an input file

Every output file the programs write is identical, byte for byte, to the
expected output that came with the test inputs, including every space of
every heap drawing. Answer 1-4 (0 registers) belongs to merge_input4.txt,
which is an empty file. problem2_answers.txt also lists
"2-11: 10 values, 4 levels, root 4", but there is no heap_input11.txt, so
that line is reported as NO INPUT.

To add a test, save the input in the problem's folder with the next number
(for example median/median_input12.txt) and add a line such as
"3-12: 3 sales, final median 2.0" to the answer file. run_tests.py finds new
input files by itself.

Notes
-----
  - "Strictly smaller" cannot change the picture: letting equal values move up
    as well would only swap equal values, which leaves every position holding
    the same value. The rule saves useless swaps.
  - No sorted() anywhere, even for file names: when "*" matches several input
    files, they are put in numeric order (2 before 10) by Problem 1's priority
    queue or Problem 2's heap_sort.
