# CS526 Homework 5
### Jia Chen
## Introduction

This homework has three problems. Every program is written in Python 3.

| Problem | Program | What it does |
|---|---|---|
| 1. Binary search tree | `bst.py` | Node and BST classes with `add_node`, `delete_node`, `find_node` and `print_tree`. A random demonstration builds a tree from 5–50 numbers between 1 and 1000, adds and deletes values (printing the tree after each call), and runs positive and negative searches. |
| 2. Vowel combinations | `vowel_combinations.py` | Counts how many letter sequences made only of vowels (A, E, I, O, U) a string of Morse dots and dashes can represent. |
| 3. Longest alternating sequence | `longest_seq.py` | Finds the length of the longest increasing sequence whose elements alternate between arrays A and B, each from a later position than the one before. |

`run_tests.py` tests all three problems in one command. `readme.txt` is the plain-text readme the assignment asks for, with the same explanations and commands as this file.

**Contents:** [How to run](#how-to-run) · [Running all the tests](#running-all-the-tests) · [Problem 1](#problem-1-binary-search-tree) · [Problem 2](#problem-2-vowel-combinations) · [Problem 3](#problem-3-longest-alternating-sequence) · [Interesting aspects](#interesting-aspects)

### Folder layout

```
Homework5/
|-- bst.py
|-- vowel_combinations.py
|-- longest_seq.py
|-- run_tests.py
|-- readme.txt                  plain-text readme required by the assignment
|-- README.md                   this file
|-- vowel_input<id>.txt         Problem 2 inputs (1-4)
|-- longest_seq<id>.txt         Problem 3 inputs (1-6)
|-- answers_vowel.txt           expected answers, one "answer <id>: ..." line per input
|-- answers_longest_seq.txt
|-- bst_output.txt              outputs written by run_tests.py
|-- vowel_output<id>.txt
`-- longest_output<id>.txt
```

## How to run

### Requirements

- **Python 3.6 or newer.** Check your version with `python --version`.
- **Nothing to install.** Only the Python standard library is used.

### Step 1: Open a terminal in the `Homework5` folder

```
cd path/to/CS526/Homework5
```

Run every command below from this folder.

### Step 2: Run the programs

The programs take the input file names as arguments. These commands work the same in **every** terminal: Windows PowerShell, Windows Command Prompt, Git Bash, macOS and Linux. On macOS and Linux, type `python3` if `python` is not found.

### Run Problem 1: Binary search tree

```
python bst.py
```

Each run uses new random numbers. The first line prints the random seed, and running with that seed repeats the same demonstration exactly:

```
python bst.py --seed 2
```

The output shows, in order:

1. the input set (5–50 random numbers between 1 and 1000),
2. the initial tree,
3. `add_node` three times with new values and once with a value already in the tree, printing the tree after each call,
4. `delete_node` on a leaf, a node with one child, a node with two children, the root, and a value that is not in the tree, printing the tree after each call,
5. `find_node` on three values in the tree (positive cases) and three random values that are not (negative cases).

How to read the printed trees is explained in [Problem 1](#printing-the-tree).

### Run Problem 2: Vowel combinations

```
python vowel_combinations.py vowel_input*.txt
```

`vowel_input*.txt` runs all four inputs in one go. A single file works too, for example `python vowel_combinations.py vowel_input1.txt`. Expected output:

```
File Input: vowel_input1.txt
The Number of Vowel combinations is:  6

File Input: vowel_input2.txt
The Number of Vowel combinations is:  8

File Input: vowel_input3.txt
The Number of Vowel combinations is:  0

File Input: vowel_input4.txt
The Number of Vowel combinations is:  193050000
```

### Run Problem 3: Longest alternating sequence

```
python longest_seq.py longest_seq*.txt
```

Expected output (takes under a second, including the 10,000 + 10,000 input):

```
File Input: longest_seq1.txt
Longest Sequence: 4

File Input: longest_seq2.txt
Longest Sequence: 7

File Input: longest_seq3.txt
Longest Sequence: 10

File Input: longest_seq4.txt
Longest Sequence: 39

File Input: longest_seq5.txt
Longest Sequence: 192

File Input: longest_seq6.txt
Longest Sequence: 1
```

Add `--show` to also print one longest sequence and where each element comes from:

```
python longest_seq.py longest_seq1.txt --show
```

```
File Input: longest_seq1.txt
Longest Sequence: 4
X = 2 3 4 6
    from a_2, b_4, a_5, b_6
```

### About the `*` wildcard

`bash` expands `vowel_input*.txt` into the file names before Python starts, but PowerShell and Command Prompt pass the `*` through unchanged. Both programs expand the wildcard themselves when the shell has not, so the same command works in every shell.

## Running all the tests

```
python run_tests.py
```

It also works from another folder if you give its path, for example `python Homework5/run_tests.py` from the `CS526` folder.

`run_tests.py` does three things:

1. **Problem 1 (no input files).** It imports `bst.py` and runs 200 rounds of 300 random `add_node`, `delete_node` and `find_node` calls, comparing every result with a Python `set`. After each call, the tree's in-order list must equal the sorted set. A binary tree is a valid BST exactly when its in-order list is sorted, so this checks the BST property as well as the contents. It then runs `python bst.py --seed 1` and saves the demonstration in `bst_output.txt`.
2. **Problems 2 and 3.** It runs the program on every `vowel_input<id>.txt` and `longest_seq<id>.txt`, using the same commands as above. It saves each output as `vowel_output<id>.txt` or `longest_output<id>.txt`, overwritten on every run.
3. **Checks.** It checks that the first line is `File Input: <file name>` and that the answer matches `answer <id>` in `answers_vowel.txt` or `answers_longest_seq.txt`. It prints `PASS`, `FAIL` or `NO ANSWER` for each test, then a summary.

If a program crashes, the test shows `FAIL` with the error message. The exit code is 1 if any test fails, 0 otherwise.

Expected output (takes about 2 seconds):

```
PASS      bst.py: 200 runs of 300 random add/delete/find calls match a Python set
PASS      bst.py --seed 1: demonstration ran, output in bst_output.txt
PASS      vowel_input1.txt: 6
PASS      vowel_input2.txt: 8
PASS      vowel_input3.txt: 0
PASS      vowel_input4.txt: 193050000
PASS      longest_seq1.txt: 4
PASS      longest_seq2.txt: 7
PASS      longest_seq3.txt: 10
PASS      longest_seq4.txt: 39
PASS      longest_seq5.txt: 192
PASS      longest_seq6.txt: 1

12 passed, 0 failed, 0 without an answer
```

Every expected answer in `answers_vowel.txt` and `answers_longest_seq.txt` comes from the results listed in the assignment.

### Adding a test

1. Save a new input file with the next number, for example `longest_seq7.txt`.
2. Add its expected answer to the answer file, for example `answer 7: 5` in `answers_longest_seq.txt`.

`run_tests.py` finds new input files automatically. An input without an answer line is still run, and reported as `NO ANSWER` with its result.

## Problem 1: Binary search tree

### The two ADTs

**`Node`** holds one value and two links: `left` to the subtree of smaller values and `right` to the subtree of larger values.

**`BST`** holds the `root` node and the number of nodes, `size`. For every node, all values in its left subtree are smaller and all values in its right subtree are larger. Duplicates are not stored.

| Method | What it does | Returns |
|---|---|---|
| `add_node(value)` | Starts at the root and goes left for a smaller value and right for a larger one, until it reaches an empty link. The new node goes there. | `True` if added, `False` if the value was already in the tree |
| `find_node(value)` | Follows the same path down from the root. | the node holding the value, or `None` |
| `delete_node(value)` | Finds the node and removes it in one of three ways, described below. | `True` if deleted, `False` if the value was not in the tree |
| `print_tree()` | Prints the tree sideways, then the values in order. | – |

Each of `add_node`, `find_node` and `delete_node` follows one path from the root down, so it takes **O(h)** time, where h is the height of the tree. For random input h is about log n. If values are added in sorted order, the tree becomes a chain and h = n.

### Deleting a node

| Case | What happens |
|---|---|
| **Leaf** (no children) | The parent's link to it becomes `None`. |
| **One child** | The child takes the deleted node's place. |
| **Two children** | Copy in the **in-order successor**, the smallest value in the right subtree, then delete the successor from the right subtree. The successor has no left child, so removing it is one of the two simpler cases. |

`_delete(node, value)` is recursive and **returns the new root of the subtree** it was given. The caller stores that result in the link it came from:

```python
node.left, deleted = self._delete(node.left, value)
```

This is how a parent's link gets updated without each node needing a link back to its parent. When the root itself is deleted, `delete_node` stores the result in `self.root`.

### Printing the tree

`print_tree()` draws the tree **sideways**. The root is at the left edge. Each node's right (larger) subtree is drawn **above** it and its left (smaller) subtree **below** it. `/--` marks a right child, `\--` a left child, and `|` continues the line from a child back to its parent. Turn the output 90° clockwise to see the usual top-down picture.

This is the initial tree from `python bst.py --seed 2`, printed and drawn top-down:

```
Tree with 8 nodes, height 5:                          94
        /-- 856                                      /  \
        |   |   /-- 829                            87    370
        |   \-- 754                                     /   \
        |       \-- 686                               174    856
    /-- 370                                                  /
    |   \-- 174                                            754
94                                                        /   \
    \-- 87                                              686   829
In-order: 87 94 174 370 686 754 829 856
```

The `In-order` line lists the values smallest to largest. It is sorted after every operation exactly when the tree is still a valid BST.

### Example run: `python bst.py --seed 2`

The input set is `94 87 370 856 174 754 829 686`. Here is part of the output, the two-children delete and the root delete:

```
delete_node(754)  ->  deleted a node with two children
Tree with 8 nodes, height 5:
            /-- 883
        /-- 856
        |   \-- 829
        |       \-- 686
    /-- 370
    |   \-- 319
94
    \-- 87
In-order: 87 94 319 370 686 829 856 883

delete_node(94)  ->  deleted the root
Tree with 7 nodes, height 5:
            /-- 883
        /-- 856
        |   \-- 829
        |       \-- 686
    /-- 370
319
    \-- 87
In-order: 87 319 370 686 829 856 883
```

- **Deleting 754.** It has children 686 and 829. Its successor, the smallest value in its right subtree, is 829. So 829 moves into 754's place and keeps 686 as its left child.
- **Deleting the root 94.** Its successor is the smallest value in the right subtree: 370 → 319, with nothing further left. So 319 becomes the new root.

The search part of the same run:

```
find_node(856)  ->  found
find_node(686)  ->  found
find_node(883)  ->  found
find_node(745)  ->  not found
find_node(888)  ->  not found
find_node(525)  ->  not found
```

**How the search values are chosen.** A random number between 1 and 1000 is rarely in a tree of at most 50 values. To be sure of both kinds of case, the positive cases are random picks from the values in the tree. The negative cases are random numbers between 1 and 1000 that are not in it.

**When a delete case is skipped.** If the random tree has no node of some kind, for example no node with two children, that delete case is skipped with a message saying so. This is rare: it happens in 1 of the first 139 seeds.

## Problem 2: Vowel combinations

### Algorithm (dynamic programming)

The Morse codes of the vowels are:

| A | E | I | O | U |
|---|---|---|---|---|
| `.-` | `.` | `..` | `---` | `..-` |

Let `ways[k]` be the number of vowel sequences that spell exactly the first k symbols. The last vowel in such a sequence covers the final 1, 2 or 3 of those symbols. So:

```
ways[0] = 1                                         (the empty sequence)
ways[k] = sum of ways[k - len(code)]  for every vowel code that matches
                                      the symbols just before position k
```

The answer is `ways[n]`. Each position tries 5 codes, so the algorithm takes **O(n)** time and memory.

### Worked example: `vowel_input1.txt` = `...-..`

| k | first k symbols | codes ending at position k | ways[k] |
|---|---|---|---|
| 0 | (none) | – | 1 |
| 1 | `.` | E → ways[0] = 1 | 1 |
| 2 | `..` | E → ways[1] = 1, I → ways[0] = 1 | 2 |
| 3 | `...` | E → ways[2] = 2, I → ways[1] = 1 | 3 |
| 4 | `...-` | A → ways[2] = 2, U → ways[1] = 1 | 3 |
| 5 | `...-.` | E → ways[4] = 3 | 3 |
| 6 | `...-..` | E → ways[5] = 3, I → ways[4] = 3 | **6** |

The 6 sequences are EEAEE, EEAI, EUEE, EUI, IAEE and IAI.

### Why the other answers come out as they do

- **`vowel_input3.txt` gives 0.** Its 14th symbol is a dash that follows `.-`. A dash can only be covered by A (`.-`), U (`..-`) or O (`---`), and none of them fits there, so `ways[14] = 0` and every later count stays 0.
- **`vowel_input4.txt` gives 193,050,000.** Listing that many sequences one by one would take far too long. The DP only adds numbers, 100 positions × 5 codes, and finishes instantly. Python integers have no size limit, so even much longer inputs give exact counts.

### Code

- **`count_vowel_sequences(symbols)`** fills `ways` as above. `symbols[start:k] == code` checks whether a vowel code ends at position k.
- **`read_symbols(path)`** reads n and returns the first n symbols, ignoring spaces and line breaks.
- **`main()`** prints the two output lines for every file named on the command line, after expanding any `*` wildcard.

## Problem 3: Longest alternating sequence

### The rules

X takes its elements alternately from A and B, and may start with either. Its values increase. Every element must come from a **later position** than the element before it. For example, `{1, 4, 7}` with 1 = a₁ and 4 = b₁ is not valid, because b₁ is not after a₁. `longest_seq6.txt` depends on this rule: every pair of elements that would increase breaks it, so the answer is 1.

### Algorithm (dynamic programming)

```
len_a[t] = length of the longest valid X that ends with a_t
         = 1 + max( len_b[q] : q < t and b_q < a_t )        (1 if there is no such q)
len_b[t] = 1 + max( len_a[p] : p < t and a_p < b_t )
answer   = the largest len_a or len_b
```

Positions t = 1, 2, 3, ... are processed in order. At each position, `len_a[t]` and `len_b[t]` are **both computed before either is stored**, so a_t and b_t, which share a position, can never follow each other.

Worked example from the assignment, A = {1, 7, 2} and B = {4, 8, 3, 9}:

| t | a_t | len_a[t] | b_t | len_b[t] |
|---|---|---|---|---|
| 1 | 1 | 1 | 4 | 1 (a₁ is at the same position, so it cannot come before b₁) |
| 2 | 7 | 2 (4, 7) | 8 | 2 (1, 8) |
| 3 | 2 | 1 (no earlier b smaller than 2) | 3 | 2 (1, 3) |
| 4 | – | – | 9 | **3** (4, 7, 9) |

The answer is 3, from X = {4, 7, 9}, the same as the assignment.

### Making it fast: a Fenwick tree

Computed directly, each `max(...)` scans every earlier position, which is O(n²) in total. On `longest_seq5.txt` (10,000 + 10,000 values) that took **25 seconds**.

The program instead keeps two **Fenwick trees** (binary indexed trees), `ends_in_a` and `ends_in_b`. They hold the sequences found so far that end in A and in B, indexed by the **rank** of their last value (its position in the sorted list of all values). The question "longest sequence ending in B with last value < a_t" becomes one call, `ends_in_b.best(rank[a_t] - 1)`, which takes O(log n) time. Storing a new sequence with `update` is O(log n) too.

**Complexity:** O((i + j) log(i + j)) time and O(i + j) memory. On `longest_seq5.txt` the DP finishes in **under 0.1 seconds** and gives the same answer, 192.

Because only ranks are used, the values can be any integers, including 0 (which appears in `longest_seq3.txt`) and negative numbers.

### Code

- **`PrefixMax`** is the Fenwick tree. It stores `(length, position)` pairs, so the largest pair is the longest sequence and also records where it ends.
- **`longest_alternating(a, b)`** runs the DP. `prev_a` and `prev_b` record the position of the previous element. Walking back from the end of the longest sequence, switching arrays at each step, rebuilds X for `--show`.
- **`read_arrays(path)`** reads the two sizes, then takes that many values for A and then for B.
- **`main()`** prints the output for every file named on the command line, and X itself when `--show` is given.

## Interesting aspects

- **Returning the new subtree root (Problem 1).** `_delete` returns the root of the subtree it changed, and the caller stores it in its own `left`, `right` or `root` link. This handles all three delete cases, including deleting the root, without parent links or special cases.
- **Testing a BST through its in-order list (Problem 1).** A binary tree is a valid BST exactly when its in-order list is sorted. `run_tests.py` uses this to check the whole tree after every one of 60,000 random calls.
- **Counting without listing (Problem 2).** The DP counts 193,050,000 sequences for `vowel_input4.txt` by adding numbers at 100 positions, without building any of the sequences.
- **One rule decides `longest_seq6.txt` (Problem 3).** The "later position" rule is enforced by computing a_t and b_t before storing either. Without it, `longest_seq6.txt` would give 2 instead of 1. For example, b₂ = 32 could be followed by a₂ = 52, which is at the same position.
- **More than 200 times faster with a Fenwick tree (Problem 3).** On the 10,000 + 10,000 input, the direct O(n²) DP takes 25 seconds. The Fenwick tree version takes under 0.1 seconds.
- **The same commands in every shell.** The programs take file names as arguments and expand `*` wildcards themselves, so `python longest_seq.py longest_seq*.txt` works in PowerShell and Command Prompt as well as bash.
- **Tested against brute force.** Besides the sample inputs, the programs were checked with slow but simple methods, and all results matched:
  - **Vowels:** 3,000 random dot/dash strings, compared with listing every vowel string.
  - **Longest sequence:** 3,000 small random arrays, compared with an exhaustive search of all alternating sequences and with the direct O(n²) DP. The sequence printed by `--show` was checked against every rule for all six input files.
  - **BST:** 300 rounds of 300 random calls, compared with a Python `set`.
