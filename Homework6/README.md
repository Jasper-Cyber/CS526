# CS526 Homework 6
### Jia Chen
## Introduction

This homework has three problems. Every program is written in Python 3 and reads its input from standard input, as the assignment requires.

| Problem | Program | What it does |
|---|---|---|
| 1. Merge k sorted lists | `merge_logs.py` | Merges the sorted sales logs of k registers into one list of `(time, register)` pairs, using its own priority queue that never holds more than k entries. |
| 2. Implement a heap | `linked_heap.py` | A binary min-heap built from linked nodes (value, left, right, parent), with `insert`, `peek`, `extract_min`, `delete`, `build`, `heap_sort`, `is_empty`, `len` and `print_heap`. Prints the heap after each insert. |
| 3. Running median | `running_median.py` | Prints the median of the sales so far after each sale, using two heaps from Problem 2. |

`run_tests.py` tests all three problems in one command. `readme.txt` is the plain-text readme the assignment asks for, with the same explanations and commands as this file.

**Contents:** [How to run](#how-to-run) · [Running all the tests](#running-all-the-tests) · [Problem 1](#problem-1-merge-k-sorted-lists) · [Problem 2](#problem-2-implement-a-heap) · [Problem 3](#problem-3-running-median) · [Interesting aspects](#interesting-aspects)

### Folder layout

Each problem's input and output files are kept in their own folder:

```
Homework6/
|-- merge_logs.py              Problem 1
|-- linked_heap.py             Problem 2
|-- running_median.py          Problem 3 (imports MinHeap from linked_heap.py)
|-- run_tests.py               tests all three problems
|-- readme.txt                 plain-text readme required by the assignment
|-- README.md                  this file
|-- homework6.txt              the assignment
|-- merge/                     Problem 1 files
|   |-- merge_input<id>.txt      inputs 1-9
|   |-- merge_output<id>.txt     outputs written by run_tests.py
|   `-- problem1_answers.txt     expected summary of each output
|-- heap/                      Problem 2 files
|   |-- heap_input<id>.txt       inputs 1-10
|   |-- heap_output<id>.txt
|   |-- heap_demo_output.txt     the other methods, shown with --demo
|   `-- problem2_answers.txt
`-- median/                    Problem 3 files
    |-- median_input<id>.txt     inputs 1-11
    |-- median_output<id>.txt
    `-- problem3_answers.txt
```

## How to run

### Requirements

- **Python 3.7 or newer.** Check your version with `python --version`.
- **Nothing to install.** Only the Python standard library is used.

### Step 1: Open a terminal in the `Homework6` folder

```
cd path/to/CS526/Homework6
```

Run every command below from this folder.

### Step 2: Run a program

The programs read **standard input**. How to send a file to standard input depends on the terminal:

| Terminal | Command |
|---|---|
| Git Bash, macOS, Linux | `python merge_logs.py < merge/merge_input1.txt` |
| Command Prompt | `python merge_logs.py < merge\merge_input1.txt` |
| PowerShell | `Get-Content merge/merge_input1.txt \| python merge_logs.py` |

PowerShell has no `<` operator, which is why it needs `Get-Content` and a pipe.

The programs also accept file names as arguments. This works the same in **every** terminal:

```
python merge_logs.py merge/merge_input1.txt
python merge_logs.py merge/merge_input*.txt
```

With more than one file, each output starts with a `File Input: <file name>` line. The programs expand the `*` themselves, because PowerShell and Command Prompt pass it through unchanged. On macOS and Linux, type `python3` if `python` is not found.

Run with no input file, a program waits for you to type the input. End it with Ctrl+D (macOS, Linux) or Ctrl+Z and Enter (Windows).

### Run Problem 1: Merge k sorted lists

```
python merge_logs.py < merge/merge_input1.txt
```

Input, one register per line (`[]` is an empty log):

```
[3, 9, 14]
[1, 9, 20, 25]
[]
[5]
```

Output:

```
Registers: 4
Total sales: 8
Merged log: [(1, 2), (3, 1), (5, 4), (9, 1), (9, 2), (14, 1), (20, 2), (25, 2)]
```

### Run Problem 2: Implement a heap

```
python linked_heap.py < heap/heap_input1.txt
```

Output for the input `[8, 3, 5, 1]`, the same as in the assignment:

```
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
```

Add `--demo` to also try every other method on the same values: `build`, `peek`, `len`, `is_empty`, `heap_sort`, `delete` (a value in the heap and one that is not), `extract_min` until the heap is empty, and the `IndexError` from `peek` and `extract_min` on an empty heap:

```
python linked_heap.py --demo heap/heap_input7.txt
```

`run_tests.py` saves this demonstration in `heap/heap_demo_output.txt`.

### Run Problem 3: Running median

```
python running_median.py < median/median_input1.txt
```

Output for the input `[5, 15, 2, 4, 8]`:

```
[5.0, 10.0, 5.0, 4.5, 5.0]
```

An empty list `[]` prints `[]`.

### Invalid input

A line that is not a list of numbers, or a register log that is not in increasing order, stops the program with a message such as:

```
Error: register 1 is not in increasing order: 1 comes after 3
```

## Running all the tests

```
python run_tests.py
```

It also works from another folder if you give its path, for example `python Homework6/run_tests.py` from the `CS526` folder.

`run_tests.py` does four things:

1. **Rules.** It reads the three programs with Python's `ast` module and fails if any of them imports `heapq`, `queue`, `bisect` or `statistics`, or calls `sorted()` or `.sort()`.
2. **Random tests against simple reference methods.**
   - **Problem 1:** 2,000 random sets of logs with many equal times, plus every input file, compared with `sorted()`. The program's `PriorityQueue` is replaced by a checking version that fails if it ever holds more than k entries or two entries from the same register.
   - **Problem 2:** 100 runs of 200 random calls of every method, compared with a sorted list. After each call it checks every parent link, the heap order, the complete shape, and that `print_heap` draws each value in its place. It also checks that the heap keeps its values only in nodes, not in a list.
   - **Problem 3:** 500 random sale lists, compared with the median of a sorted list. After every sale it checks that both halves are `MinHeap`s from Problem 2 and that the two invariants hold.
3. **Every input file.** It runs each program on every `<folder>/<name>_input<id>.txt`, sending the file to standard input. The output is saved next to the input as `<name>_output<id>.txt`, overwritten on every run. Each output is checked against a reference: `sorted()` for Problem 1, a sorted list for Problem 3, and for Problem 2 an array-based heap that replays the same inserts, with every drawn tree checked level by level.
4. **Answer files.** It summarizes each output in the format of the folder's answer file, for example `4 registers, 8 sales, first (1, 2), last (25, 2)`, and compares it with the line `1-1: ...` in `problem1_answers.txt`. It prints `PASS`, `FAIL`, `NO ANSWER` or `NO INPUT` for each test, then a summary.

If a program crashes, the test shows `FAIL` with the error message. The exit code is 1 if any test fails, 0 otherwise.

Expected output (takes about 8 seconds):

```
PASS      rules: no heapq, queue, bisect, statistics, sorted() or .sort() in the programs
PASS      merge_logs.py: 2000 random merges and all input files match sorted(); queue never held more than k entries or two from one register
PASS      linked_heap.py: 100 runs of 200 random calls of every method match a sorted list; links, heap order, complete shape and drawing correct after each call
PASS      linked_heap.py: the heap is stored only in linked nodes (value, left, right, parent)
PASS      running_median.py: uses MinHeap from linked_heap.py; 500 random sale lists match a sorted-list median; both invariants hold after every sale
PASS      linked_heap.py --demo heap/heap_input7.txt: every method shown, output in heap/heap_demo_output.txt
PASS      merge/merge_input1.txt: 4 registers, 8 sales, first (1, 2), last (25, 2)
PASS      merge/merge_input2.txt: 1 registers, 6 sales, first (2, 1), last (64, 1)
PASS      merge/merge_input3.txt: 3 registers, 0 sales, first none, last none
PASS      merge/merge_input4.txt: 0 registers, 0 sales, first none, last none
PASS      merge/merge_input5.txt: 4 registers, 10 sales, first (7, 1), last (7, 4)
PASS      merge/merge_input6.txt: 3 registers, 9 sales, first (100, 3), last (320, 1)
PASS      merge/merge_input7.txt: 7 registers, 14 sales, first (1, 4), last (60, 4)
PASS      merge/merge_input8.txt: 10 registers, 108 sales, first (3, 9), last (500, 7)
PASS      merge/merge_input9.txt: 50 registers, 20737 sales, first (1, 25), last (28799, 31)
PASS      heap/heap_input1.txt: 4 values, 3 levels, root 1
PASS      heap/heap_input2.txt: 0 values, 0 levels, root none
PASS      heap/heap_input3.txt: 1 values, 1 levels, root 42
PASS      heap/heap_input4.txt: 15 values, 4 levels, root 10
PASS      heap/heap_input5.txt: 15 values, 4 levels, root 10
PASS      heap/heap_input6.txt: 8 values, 4 levels, root 7
PASS      heap/heap_input7.txt: 9 values, 4 levels, root 1
PASS      heap/heap_input8.txt: 8 values, 4 levels, root -9
PASS      heap/heap_input9.txt: 30 values, 5 levels, root 37
PASS      heap/heap_input10.txt: 100 values, 7 levels, root 2
NO INPUT  2-11 in heap/problem2_answers.txt: heap/heap_input11.txt does not exist
PASS      median/median_input1.txt: 5 sales, final median 5.0
PASS      median/median_input2.txt: 0 sales, final median none
PASS      median/median_input3.txt: 1 sales, final median 42.0
PASS      median/median_input4.txt: 2 sales, final median 17.5
PASS      median/median_input5.txt: 12 sales, final median 7.0
PASS      median/median_input6.txt: 20 sales, final median 105.0
PASS      median/median_input7.txt: 20 sales, final median 105.0
PASS      median/median_input8.txt: 12 sales, final median 500.5
PASS      median/median_input9.txt: 40 sales, final median 3.0
PASS      median/median_input10.txt: 100 sales, final median 540.0
PASS      median/median_input11.txt: 20000 sales, final median 502.0

36 passed, 0 failed, 1 without an answer or an input file
```

**About the test files.** Every output file the programs write is identical, byte for byte, to the expected output that came with the test inputs, including every space of every heap drawing. Answer `1-4` (0 registers) belongs to `merge/merge_input4.txt`, which is an empty file. `problem2_answers.txt` also lists `2-11: 10 values, 4 levels, root 4`, but there is no `heap_input11.txt`, so that line is reported as `NO INPUT`.

### Adding a test

1. Save a new input file in the problem's folder with the next number, for example `median/median_input12.txt`.
2. Add its expected summary to the answer file, for example `3-12: 3 sales, final median 2.0` in `median/problem3_answers.txt`.

`run_tests.py` finds new input files automatically. An input without an answer line is still run and checked against the reference, and reported as `NO ANSWER` with its result.

## Problem 1: Merge k sorted lists

### Algorithm

Each register's log is already sorted, so the next sale of the merged log is always **the first not-yet-merged sale of some register**. A priority queue holds exactly those candidates, at most one per register:

1. Push the first sale of every non-empty log, as an entry `(time, register, position)`.
2. Pop the smallest entry and append `(time, register)` to the result.
3. If that register has another sale, push it: `(next time, register, position + 1)`.
4. Repeat steps 2 and 3 until the queue is empty.

**Equal times.** Entries are compared as tuples: first by time, then by register number. So for equal times the lower-numbered register comes out first, as the assignment requires. Sales from the same register keep their order because a register's next sale is pushed only after the previous one is popped.

**The k-entry rule.** A register's entry is pushed only after its previous entry is popped. So the queue never holds two entries from one register, and never more than k entries. `run_tests.py` checks this on every push.

### Worked example (the assignment's input)

| Step | Pop | Push (next sale of the same register) | Queue afterwards |
|---|---|---|---|
| start | – | (3, 1), (1, 2), (5, 4); register 3 is empty | (1, 2) (3, 1) (5, 4) |
| 1 | (1, 2) | (9, 2) | (3, 1) (5, 4) (9, 2) |
| 2 | (3, 1) | (9, 1) | (5, 4) (9, 1) (9, 2) |
| 3 | (5, 4) | – (register 4 is done) | (9, 1) (9, 2) |
| 4 | (9, 1) | (14, 1) | (9, 2) (14, 1) |
| 5 | (9, 2) | (20, 2) | (14, 1) (20, 2) |
| 6 | (14, 1) | – | (20, 2) |
| 7 | (20, 2) | (25, 2) | (25, 2) |
| 8 | (25, 2) | – | (empty) |

Step 4 shows the tie rule: (9, 1) comes before (9, 2). The queue never holds more than 3 entries, fewer than k = 4, because register 3 is empty.

### The priority queue

`PriorityQueue` is a binary min-heap kept in a Python list. Entry `i` has its children at `2i + 1` and `2i + 2` and its parent at `(i - 1) // 2`.

- `push(entry)` appends the entry, then swaps it with its parent while it is smaller.
- `pop()` takes the top entry, moves the last entry to the top, then swaps it with its smaller child while a child is smaller.

Both take O(log k) time for a queue of at most k entries.

### Complexity

For k registers and N sales in total: **O(N log k)** time, because each sale is pushed and popped once. The queue uses **O(k)** memory. With one register (`merge_input2.txt`) the queue holds one entry at a time; with 50 registers and 20,737 sales (`merge_input9.txt`) it holds at most 50.

### Code

- **`PriorityQueue`**: the min-heap described above.
- **`merge_logs(logs)`**: the algorithm. Returns the merged list.
- **`read_logs(text)`**: reads one log per non-blank line and checks that it is a list of numbers in increasing order.
- **`main()`**: reads standard input (or the files named on the command line) and prints the three output lines.

## Problem 2: Implement a heap

### The two ADTs

**`Node`** holds a `value` and three links: `left`, `right` and `parent`.

**`MinHeap`** holds only the `root` node and the number of values. It never stores its values in a list or an array. Two rules hold after every method call:

- **Heap order:** every node's value is less than or equal to its children's values, so the smallest value is at the root.
- **Complete shape:** every level is full except possibly the last, which is filled from the left.

### Finding a position in O(log n)

The positions are numbered 1, 2, 3, ... in level order. Because the shape is complete, the n values always fill exactly positions 1 to n, so:

- the next free spot is position n + 1,
- the last node is position n,
- the parent of position p is p // 2, and p is a left child when p is even.

The binary digits of p after the leading 1 are the path from the root: 0 means go left and 1 means go right. For example, 6 = `110`, so the path is right, then left. `_node_at(p)` follows these digits, so it reaches any position in O(log n) steps.

```
                 1
             /       \
         2 = 10      3 = 11
         /   \        /   \
     4=100  5=101  6=110  7=111
```

### The methods

| Method | How it works | Time |
|---|---|---|
| `insert(value)` | Attach a new node at position n + 1, the child of `_node_at((n + 1) // 2)`. Then move the value up while it is **strictly smaller** than its parent's value. | O(log n) |
| `peek()` | Return the root's value. Raises `IndexError` on an empty heap. | O(1) |
| `extract_min()` | Save the root's value. Unlink the last node (position n), move its value into the root and move it down while a child is strictly smaller (the smaller child; the left one on a tie). Raises `IndexError` on an empty heap. | O(log n) |
| `delete(value)` | Find a node holding the value, then remove it the same way as `extract_min`: the last node's value replaces it. That value can be too small or too large for its new place, so it moves up or down. Returns `True`, or `False` if the value is not in the heap. | O(n) to find, O(log n) to remove |
| `build(values)` | Replace the contents with `values`. The nodes are linked in level order. Each subtree is made into a heap bottom-up: first both child subtrees, then the subtree's root moves down. | O(n) |
| `heap_sort()` | Copy the tree, then call `extract_min` on the copy until it is empty. The heap itself is not changed. | O(n log n) |
| `is_empty()`, `len(heap)` | Use the stored count. | O(1) |
| `print_heap()` | Draw the tree, root at the top (described below). | O(n) |

**Why `delete` needs O(n) to find a value.** A heap is ordered only from top to bottom, not from left to right, so the value could be in either subtree. Still, every value in a subtree is at least its root, so `_find` skips any subtree whose root is larger than the value it is looking for.

**Why `build` is O(n).** Half of the nodes are leaves and never move. A quarter move down at most 1 level, an eighth at most 2, and so on. The total, n/4 · 1 + n/8 · 2 + n/16 · 3 + ..., is less than n. Building with n separate inserts would take O(n log n).

### Drawing the tree

Each level is drawn on one line, with a line of `/` and `\` between levels. The bottom level has a slot every 4 columns. Each level above has slots twice as far apart, so every parent is exactly halfway between its two children. Each value is centered on its slot, and each `/` or `\` is drawn halfway between a parent and its child.

```
After insert(10):                          (heap/heap_output5.txt, last tree)
                10
             /       \
        60              20
       /   \           /   \
    90      70      50      30
    / \     / \     / \     / \
  150 120 130 80  140 100 110 40
```

Values up to 3 characters wide fit in 4-column slots. If a value is wider, the slots widen to the next multiple of 4 that leaves at least one space between values, so the drawing stays correct for any numbers.

### Example: duplicates (`heap/heap_input7.txt`)

The input is `[5, 3, 5, 1, 3, 5, 1, 1, 3]`. On the 7th insert, the new 1 is placed at position 7 under 5, swaps with that 5, and then stops below the root 1, because it is **not strictly smaller** than it:

```
After insert(5):              After insert(1):
        1                             1
      /   \                         /   \
    3       5                     3       1
   / \     /                     / \     / \
  5   3   5                     5   3   5   5
```

### Code

- **`Node`**, **`MinHeap`**: the ADTs. The helpers are `_node_at`, `_sift_up`, `_sift_down`, `_remove` (shared by `extract_min` and `delete`), `_find`, `_build_subtree`, `_copy_subtree` and `draw`.
- **`show_inserts(values)`**: the required output.
- **`show_other_methods(values)`**: the `--demo` output.
- **`parse_values(text)`**, **`read_text(path, prompt)`**, **`expand_wildcards(args)`**: input handling, also used by `running_median.py`.

## Problem 3: Running median

### How the heap is used

The sales so far are split into two halves, each kept in a `MinHeap` from Problem 2:

| Heap | Holds | Its root |
|---|---|---|
| `lower` | the smaller half of the sales, stored **negated** | minus the largest of the smaller half |
| `upper` | the larger half of the sales | the smallest of the larger half |

Storing the negatives turns the min-heap into a max-heap without changing `MinHeap`: the smallest of the negatives is minus the largest sale. So `-lower.peek()` is the largest sale of the smaller half.

### What must stay true after each sale

1. **Every sale in `lower` is ≤ every sale in `upper`**, which means `-lower.peek() <= upper.peek()`.
2. **The halves differ in size by at most one, and `lower` is the bigger one**: `len(lower) == len(upper)` or `len(lower) == len(upper) + 1`.

Together these mean the one or two middle sales are always at the two roots:

- odd count: the median is `-lower.peek()`;
- even count: the median is `(-lower.peek() + upper.peek()) / 2`.

`peek()` is O(1), so the median is available in **O(1)** time after every sale.

### Algorithm for each new sale

1. **Put it in the right half.** If `lower` is empty or the sale is ≤ `-lower.peek()`, insert `-sale` into `lower`. Otherwise insert it into `upper`. This keeps invariant 1.
2. **Rebalance.** If `lower` now has 2 more values than `upper`, move its root to `upper`. If `upper` has more values than `lower`, move its root to `lower`. The moved value is the one closest to the middle, so invariant 1 still holds, and invariant 2 is restored.
3. **Read the median** from the roots, as above.

Each sale costs at most 3 heap operations: **O(log n)** time. The sales are never kept in a sorted list and never re-sorted.

### Worked example (the assignment's input)

| Sale | Smaller half (`lower`) | Larger half (`upper`) | Median |
|---|---|---|---|
| 5 | 5 | – | 5.0 |
| 15 | 5 | 15 | (5 + 15) / 2 = 10.0 |
| 2 | 2, 5 | 15 | 5.0 |
| 4 | 2, 4 | 5, 15 | (4 + 5) / 2 = 4.5 |
| 8 | 2, 4, 5 | 8, 15 | 5.0 |

When 4 arrives, it goes into the smaller half, which then has 3 values against 1. Its largest, 5, moves to the larger half.

### Code

- **`RunningMedian`**: the two heaps, with `add(amount)` and `median()`.
- **`running_medians(sales)`**: returns the list of medians, one after each sale.
- **`main()`**: reads the list from standard input (or the files named on the command line) and prints the medians.

## Interesting aspects

- **The same drawing as the expected output, space for space (Problem 2).** The drawing rule (fixed slots that double in width at each level up, values centered, slashes halfway) reproduces the expected heap drawings exactly. That includes the 100-value, 7-level trees in `heap_output10.txt` and the negative numbers in `heap_output8.txt`.
- **Binary digits as a path (Problem 2).** A complete tree's shape is fixed by n alone, so the node at any position can be found from the position's binary digits, without an array.
- **O(n) `build` without an array (Problem 2).** `_build_subtree` creates the nodes recursively and sifts each subtree's root down after both of its child subtrees are heaps.
- **"Strictly smaller" cannot change the picture (Problem 2).** Letting equal values move up as well would only swap equal values, which leaves every position holding the same value. The rule saves useless swaps; the printed trees are the same either way.
- **A max-heap from a min-heap (Problem 3).** Storing negated values gives the smaller half a max-heap without adding any code to `MinHeap`.
- **No `sorted()` anywhere, even for file names.** When `*` matches several input files, they are put in numeric order (2 before 10) by Problem 1's priority queue or Problem 2's `heap_sort`.
- **Tests that check the rules, not only the results.** `run_tests.py` reads the programs' code to reject banned imports and calls. It also counts the priority queue's entries on every push and checks the tree's links and shape after every heap call.
