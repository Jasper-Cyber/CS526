# CS526 Homework 3
### Jia Chen
## Introduction

This homework has four problems. Every program is written in Python 3. Problems 1, 2 and 4 read their input from standard input.

| Problem | Program | What it does |
|---|---|---|
| 1. Palindromes | `palindrome.py` | Reads one string per line and prints `True` or `False` for each, then the number of palindromes. Spaces between characters are ignored and case matters. |
| 2. Unique substrings | `unique_substrings.py` | Reads one string, uses recursion to find every unique non-empty substring, and prints them in alphabetical order followed by the count. |
| 3. Stack reversal | `reverse_stack.py` | Implements a stack three ways (array, singly linked list, doubly linked list), pushes 1 through 10 onto each, and reverses each one in place with recursion. Prints each stack before and after. |
| 4. Ghostbusters | `ghostbusters.py` | Reads n Ghostbuster/ghost pairs and decides whether all streams can fire at once without any two crossing. |

`run_tests.py` runs Problems 1, 2 and 4 on every test input, writes the output files, and compares them with the expected answers.

### Folder layout

```
Homework3/
├── palindrome.py
├── unique_substrings.py
├── reverse_stack.py
├── ghostbusters.py
├── run_tests.py
├── palendrom/          palendrome_<id>.txt (input), palendrome_ans_<id>.txt (expected),
│                       palendrome_output_<id>.txt (generated)
├── uniquesubstrings/   unique_substrings_input_<id>.txt, _ans_<id>.txt, _output_<id>.txt
└── ghostbusters/       ghostbusters_input_<id>.txt, _ans_<id>.txt, _output_<id>.txt
```

## Algorithm

### Problem 1: Palindromes

For each line, the program removes the line ending and the spaces between characters, so `"g e e k"` becomes `"geek"`. The string is a palindrome when it equals its reverse, `chars == chars[::-1]`. A counter records how many lines were `True` and is printed last.

### Problem 2: Unique substrings (recursion)

A substring is defined by a start index and an end index. In place of a nested `for` loop, the program uses two recursive functions that share one `set`.

- `collect_substrings(text, start, found)` is the outer recursion and moves the start index.
  - Base case: `start >= len(text)`.
  - Otherwise it collects every substring beginning at `start`, then calls itself with `start + 1`.
- `collect_from(text, start, end, found)` is the inner recursion and moves the end index.
  - Base case: `end > len(text)`.
  - Otherwise it adds `text[start:end]` to the set, then calls itself with `end + 1`.

For `abcab`, the calls produce:

```
start=0: a, ab, abc, abca, abcab
start=1: b, bc, bca, bcab
start=2: c, ca, cab
start=3: a, ab        (already in the set)
start=4: b            (already in the set)
```

The set removes duplicates. `sorted()` puts the substrings in alphabetical order for printing, and the length of the sorted list is the count (12 for `abcab`).

### Problem 3: Stack reversal (linked lists and recursion)

All three classes support `push`, `pop`, `peek` and `is_empty`. Each has a `reverse()` method that changes the same object, uses recursion, and contains no loops.

**Array stack.** A Python list where the end of the list is the top.
`_reverse(lo, hi)` swaps the outermost pair `data[lo]` and `data[hi]`, then recurses on `(lo + 1, hi - 1)`. It stops when `lo >= hi`.

```
[1, 2, 3, 4, 5]  ->  swap 0,4  ->  [5, 2, 3, 4, 1]  ->  swap 1,3  ->  [5, 4, 3, 2, 1]
```

**Singly linked list stack.** Each `_SNode` has `value` and `next`. `_head` is the top of the stack, so `push` and `pop` are O(1):

```python
self._head = _SNode(value, self._head)   # push: new node points at the old top
```

`_reverse(node, prev)` turns the links around one node at a time:

1. Save `rest = node.next`, because the next step overwrites that link.
2. Set `node.next = prev`, pointing the node backwards.
3. Recurse on `(rest, node)`.
4. When `node` is `None`, return `prev`. That is the old last node, which becomes the new `_head`.

```
3 -> 2 -> 1 -> None     becomes     1 -> 2 -> 3 -> None
```

**Doubly linked list stack.** Each `_DNode` has `value`, `prev` and `next`. The stack keeps `_head` (bottom) and `_tail` (top).

- `push` creates a node whose `prev` is the old tail, links `old_tail.next` to the new node, and moves `_tail` to it. On an empty stack, the new node becomes both `_head` and `_tail`.
- `pop` moves `_tail` back to `_tail.prev`.

`_swap_links(node)` saves `node.next`, swaps the node's `prev` and `next`, and recurses on the saved node. After every node has been processed, `reverse()` swaps `_head` and `_tail`.

```
None <- 1 <-> 2 <-> 3 -> None     becomes     None <- 3 <-> 2 <-> 1 -> None
```

In both linked lists, no nodes are created or copied during reversal. The existing nodes are relinked.

### Problem 4: Ghostbusters

A stream is an **infinite** line. Two infinite lines in a plane always intersect unless they are parallel and on different lines. Lines that coincide count as crossing. So:

> All ghosts are eliminated **exactly when every stream has the same direction and no two streams lie on the same line.**

The positions of the Ghostbusters and ghosts along each line, and how the pairs are matched, do not affect the answer. Only the lines matter.

Each stream is turned into a key `(direction, offset)` using integer arithmetic only:

1. **Direction.** Compute `dx = gx - bx`, `dy = gy - by` and divide both by `gcd(dx, dy)`. Then fix the sign so that `dx > 0`, or `dy > 0` when `dx == 0`. Parallel streams always get an identical direction. For example, `(2, 2)`, `(5, 5)` and `(-1, -1)` all become `(1, 1)`, and every vertical stream becomes `(0, 1)`.
2. **Offset.** Compute `dy * x - dx * y` using the Ghostbuster's point. This value is the same at every point on the line and is different for each separate parallel line.

`all_eliminated` goes through the streams once:

- If any direction differs from the first one, two streams are not parallel and must cross, so the answer is **not eliminated**.
- If an offset is already in the set of offsets seen, two streams are on the same line, so the answer is **not eliminated**.
- Otherwise the answer is **eliminated**.

This takes **O(n)** time and O(n) memory. With n = 1, the single stream crosses nothing, so the answer is eliminated.

Worked examples from the assignment:

| Input | Directions | Offsets | Result |
|---|---|---|---|
| (0,0)->(5,5), (3,0)->(0,3) | (1,1), (1,-1) | – | not parallel: **not eliminated** |
| (0,0)->(2,2), (3,0)->(5,2), (0,4)->(1,5) | all (1,1) | 0, 3, -4 | **eliminated** |
| (0,0)->(2,2), (5,5)->(7,7) | both (1,1) | 0, 0 | same line: **not eliminated** |
| (1,0)->(1,6), (4,2)->(4,-3) | both (0,1) | 1, 4 | **eliminated** |

## Interesting aspects

- **Exact integer geometry (Problem 4).** Comparing slopes `dy / dx` would divide by zero for vertical streams. Floating-point slopes could also differ by a rounding error when they should be equal. Reducing `(dx, dy)` by the gcd and fixing the sign gives an exact integer key, so equal lines always compare equal with `==`.
- **Infinite lines simplify Problem 4.** Because streams extend forever in both directions, line segments and their endpoints never have to be considered. Any two non-parallel streams cross, so the problem reduces to checking that all streams are parallel and distinct, and the algorithm needs one O(n) pass instead of checking every pair in O(n²).
- **Two recursive functions in place of nested loops (Problem 2).** A single recursion over every `(start, end)` pair would reach a depth of about n²/2. Splitting it into an outer recursion over `start` and an inner recursion over `end` keeps the maximum depth around n, so longer strings stay well under Python's recursion limit.
- **Different "top" in each linked list (Problem 3).** In the singly linked stack, the head must be the top. Popping from the tail would need an O(n) walk to find the node before it. In the doubly linked stack either end works in O(1), so the head is the bottom and the tail is the top. Walking from `_head` along `next` then lists the stack in the required bottom-to-top order. The reversal (swap every node's `prev`/`next`, then swap `_head`/`_tail`) would work with either layout.
- **Reversal is truly in place.** Each `reverse()` changes the same stack object. The array version swaps elements inside the existing list, and the linked versions only reassign links. After reversing, `peek`, `pop` and `is_empty` still behave correctly. After pushing 1, 2, 3 and reversing, `peek()` returns 1 and three pops return 1, 2, 3.
- **Robust input handling.** Line endings (`\n` and Windows `\r\n`) are stripped before processing. A leftover newline would otherwise change the palindrome result or add false substrings such as `"b\n"`. `ghostbusters.py` skips blank lines, so an extra empty line at the end of a file does not cause a crash.
- **Test runner tolerates missing answers.** If an input file has no matching answer file, `run_tests.py` still writes the output file and reports `NO ANSWER` instead of failing.

## How to run

Run these commands from the `Homework3` folder. On Windows, use `python` where these examples say `python3`.

### Problem 1: Palindromes

```
python3 palindrome.py < palendrom/palendrome_0.txt
```

Other inputs in `palendrom/` work the same way, for example `palendrome_2S.txt` or `palendrome_4L.txt`.

### Problem 2: Unique substrings

```
python3 unique_substrings.py < uniquesubstrings/unique_substrings_input_0.txt
```

### Problem 3: Stack reversal

This program needs no input file:

```
python3 reverse_stack.py
```

Expected output:

```
Array stack
Before: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
After:  10, 9, 8, 7, 6, 5, 4, 3, 2, 1

Singly linked list stack
Before: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
After:  10, 9, 8, 7, 6, 5, 4, 3, 2, 1

Doubly linked list stack
Before: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
After:  10, 9, 8, 7, 6, 5, 4, 3, 2, 1
```

### Problem 4: Ghostbusters

```
python3 ghostbusters.py < ghostbusters/ghostbusters_input_0.txt
```

### Saving output and comparing by hand

```
python3 palindrome.py < palendrom/palendrome_0.txt > palendrom/palendrome_output_0.txt
diff --strip-trailing-cr palendrom/palendrome_output_0.txt palendrom/palendrome_ans_0.txt
```

The answer files have no newline after their last line, so `diff` reports the last line as different (`\ No newline at end of file`) even when the text matches. `run_tests.py` compares line by line and ignores that difference.

### Running all the tests

```
python3 run_tests.py
```

For every input file of Problems 1, 2 and 4, `run_tests.py`:

1. runs the matching program with the file as standard input,
2. writes the program's output next to the input, as `<prefix>_output_<id>.txt`,
3. compares the output line by line with `<prefix>_ans_<id>.txt`, and
4. prints `PASS`, `FAIL`, or `NO ANSWER` when no answer file exists, followed by a summary.

The exit code is 1 if any test fails, 0 otherwise. Current result:

```
PASS      palendrom/palendrome_0.txt
PASS      palendrom/palendrome_0L.txt
...
PASS      uniquesubstrings/unique_substrings_input_0.txt
...
PASS      ghostbusters/ghostbusters_input_9.txt

29 passed, 0 failed, 0 without an answer file
```

To add a test, put a new input file and its answer file in the same folder, following the same naming pattern, for example `ghostbusters/ghostbusters_input_11.txt` and `ghostbusters/ghostbusters_ans_11.txt`. `run_tests.py` will pick them up automatically.
