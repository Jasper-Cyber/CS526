CS526 Homework 5
Jia Chen
================================================================================

CONTENTS

  1. Files
  2. How to run (all problems)
  3. Problem 1 - Binary search tree            bst.py
  4. Problem 2 - Vowel combinations            vowel_combinations.py
  5. Problem 3 - Longest alternating sequence  longest_seq.py
  6. Testing                                   run_tests.py


================================================================================
1. FILES
================================================================================

  bst.py                       Problem 1 program
  vowel_combinations.py        Problem 2 program
  longest_seq.py               Problem 3 program
  run_tests.py                 tests all three problems (section 6)
  readme.txt                   this file
  README.md                    the same information, formatted for GitHub

  vowel_input1.txt - 4.txt     Problem 2 inputs
  longest_seq1.txt - 6.txt     Problem 3 inputs
  answers_vowel.txt            expected answers for run_tests.py
  answers_longest_seq.txt
  bst_output.txt               outputs written by run_tests.py
  vowel_output<id>.txt
  longest_output<id>.txt


================================================================================
2. HOW TO RUN (ALL PROBLEMS)
================================================================================

Requirements: Python 3.6 or newer. Only the Python standard library is used,
so there is nothing to install. Check the version with:

    python --version

Step 1. Open a terminal window and go to the Homework5 folder:

    cd path/to/CS526/Homework5

Step 2. Run the commands below. They work the same in every terminal: Windows
PowerShell, Windows Command Prompt, Git Bash, macOS and Linux. On macOS and
Linux, type python3 instead of python if python is not found.

    python bst.py
    python vowel_combinations.py vowel_input*.txt
    python longest_seq.py longest_seq*.txt
    python run_tests.py

A "*" in a file name runs every matching input file in one go. bash expands
it before Python starts; PowerShell and Command Prompt do not, so the programs
expand it themselves. Single files work too, for example:

    python vowel_combinations.py vowel_input1.txt


================================================================================
3. PROBLEM 1 - BINARY SEARCH TREE  (bst.py)
================================================================================

How to run
----------
    python bst.py               a new random demonstration on every run
    python bst.py --seed 2      repeat the demonstration with seed 2

The first output line shows the seed, so any run can be repeated exactly.

The output shows, in order:
  1. the input set: 5 to 50 random numbers between 1 and 1000,
  2. the initial tree,
  3. add_node three times with new values and once with a value already in
     the tree, printing the tree after each call,
  4. delete_node on a leaf, a node with one child, a node with two children,
     the root, and a value that is not in the tree, printing the tree after
     each call,
  5. find_node on 3 values in the tree (positive cases) and 3 random values
     that are not in the tree (negative cases).

The ADTs
--------
Node   holds one value and two links: left (subtree of smaller values) and
       right (subtree of larger values).

BST    holds the root node and the number of nodes (size). For every node,
       all values in its left subtree are smaller and all values in its
       right subtree are larger. Duplicates are not stored.

  add_node(value)     Start at the root; go left for a smaller value and
                      right for a larger one until an empty link is
                      reached, and put the new node there. Returns False if
                      the value is already in the tree.
  find_node(value)    Follow the same path. Returns the node, or None.
  delete_node(value)  Find the node and remove it (see below). Returns False
                      if the value is not in the tree.
  print_tree()        Print the tree sideways, then the values in order.

add_node, find_node and delete_node follow one path down from the root, so
each takes O(h) time, where h is the height of the tree: about log n for
random input, and n if the values are added in sorted order.

Deleting a node
---------------
  Leaf (no children)  The parent's link to it becomes None.
  One child           The child takes the deleted node's place.
  Two children        Copy in the in-order successor (the smallest value in
                      the right subtree), then delete the successor from the
                      right subtree. The successor has no left child, so
                      removing it is one of the two simpler cases.

_delete(node, value) is recursive and returns the new root of the subtree it
was given. The caller stores that result in the link it came from:

    node.left, deleted = self._delete(node.left, value)

This updates the parent's link without needing links from children back to
their parents. When the root itself is deleted, delete_node stores the
result in self.root.

Reading the printed tree
------------------------
The root is at the left edge. Each node's right (larger) subtree is drawn
ABOVE it and its left (smaller) subtree BELOW it. "/--" marks a right child,
"\--" a left child, and "|" continues the line from a child to its parent.
Turn the output 90 degrees clockwise to see the usual top-down picture.

Initial tree of  python bst.py --seed 2 , and the same tree top-down:

    Tree with 8 nodes, height 5:                  94
            /-- 856                              /  \
            |   |   /-- 829                    87    370
            |   \-- 754                             /   \
            |       \-- 686                       174    856
        /-- 370                                          /
        |   \-- 174                                    754
    94                                                /   \
        \-- 87                                      686   829
    In-order: 87 94 174 370 686 754 829 856

The In-order line lists the values from smallest to largest. It stays sorted
after every operation exactly when the tree is still a valid BST.

Example run: python bst.py --seed 2  (part of the output)
----------------------------------------------------------
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

    find_node(856)  ->  found
    find_node(686)  ->  found
    find_node(883)  ->  found
    find_node(745)  ->  not found
    find_node(888)  ->  not found
    find_node(525)  ->  not found

754 has two children, 686 and 829. Its successor (smallest value in its right
subtree) is 829, which moves into its place. For the root 94, the successor
is 370 -> 319, so 319 becomes the new root.

The search values: a random number between 1 and 1000 is rarely in a tree of
at most 50 values. To be sure of both kinds of case, the positive cases are
random picks from the values in the tree, and the negative cases are random
numbers between 1 and 1000 that are not in it.

If the random tree has no node of some kind (for example, no node with two
children), that delete case is skipped with a message saying so. This is
rare: it happens for 1 of the first 139 seeds.


================================================================================
4. PROBLEM 2 - VOWEL COMBINATIONS  (vowel_combinations.py)
================================================================================

How to run
----------
    python vowel_combinations.py vowel_input*.txt

Output:

    File Input: vowel_input1.txt
    The Number of Vowel combinations is:  6

    File Input: vowel_input2.txt
    The Number of Vowel combinations is:  8

    File Input: vowel_input3.txt
    The Number of Vowel combinations is:  0

    File Input: vowel_input4.txt
    The Number of Vowel combinations is:  193050000

All four match the expected results given in the assignment.

Algorithm (dynamic programming)
-------------------------------
Morse codes of the vowels:  A = .-   E = .   I = ..   O = ---   U = ..-

ways[k] is the number of vowel sequences that spell exactly the first k
symbols. The last vowel in such a sequence covers the final 1, 2 or 3 of
those symbols, so

    ways[0] = 1                                   (the empty sequence)
    ways[k] = sum of ways[k - len(code)]  for every vowel code that matches
                                          the symbols just before position k

The answer is ways[n]. Each position tries 5 codes: O(n) time and memory.

Worked example, vowel_input1.txt = ...-..

    k   first k symbols   codes ending at position k            ways[k]
    0   (none)            -                                      1
    1   .                 E -> ways[0] = 1                       1
    2   ..                E -> ways[1] = 1,  I -> ways[0] = 1    2
    3   ...               E -> ways[2] = 2,  I -> ways[1] = 1    3
    4   ...-              A -> ways[2] = 2,  U -> ways[1] = 1    3
    5   ...-.             E -> ways[4] = 3                       3
    6   ...-..            E -> ways[5] = 3,  I -> ways[4] = 3    6

The 6 sequences are EEAEE, EEAI, EUEE, EUI, IAEE and IAI.

vowel_input3.txt gives 0: its 14th symbol is a dash that follows ".-". A dash
can only be covered by A (.-), U (..-) or O (---), and none of them fits
there, so ways[14] = 0 and every later count stays 0.

vowel_input4.txt gives 193,050,000. Listing that many sequences would take far
too long; the DP only adds numbers (100 positions x 5 codes). Python integers
have no size limit, so longer inputs still give exact counts.

Explanation of the code
-----------------------
count_vowel_sequences(symbols)
    Fills ways as above. symbols[start:k] == code checks whether a vowel
    code ends at position k.
read_symbols(path)
    Reads n and returns the first n symbols, ignoring spaces and line breaks.
main()
    Prints the two output lines for every file named on the command line,
    after expanding any "*" wildcard.


================================================================================
5. PROBLEM 3 - LONGEST ALTERNATING SEQUENCE  (longest_seq.py)
================================================================================

How to run
----------
    python longest_seq.py longest_seq*.txt

Output (takes under a second, including the 10,000 + 10,000 input):

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

All six match the expected results given in the assignment.

Add --show to also print one longest sequence and where each element is from:

    python longest_seq.py longest_seq1.txt --show

    File Input: longest_seq1.txt
    Longest Sequence: 4
    X = 2 3 4 6
        from a_2, b_4, a_5, b_6

The rules
---------
X takes its elements alternately from A and B (it may start with either), its
values increase, and every element comes from a LATER POSITION than the
element before it. {1, 4, 7} with 1 = a_1 and 4 = b_1 is not valid, because
b_1 is not after a_1.

Algorithm (dynamic programming)
-------------------------------
    len_a[t] = length of the longest valid X that ends with a_t
             = 1 + max( len_b[q] : q < t and b_q < a_t )    (1 if none)
    len_b[t] = 1 + max( len_a[p] : p < t and a_p < b_t )
    answer   = the largest len_a or len_b

Positions t = 1, 2, 3, ... are processed in order. At each position, len_a[t]
and len_b[t] are BOTH computed before either is stored, so a_t and b_t (same
position) can never follow each other. Without this rule, longest_seq6.txt
would give 2 instead of 1: b_2 = 32 could be followed by a_2 = 52.

Worked example from the assignment, A = {1, 7, 2}, B = {4, 8, 3, 9}:

    t   a_t   len_a[t]                 b_t   len_b[t]
    1   1     1                        4     1  (a_1 is at the same position)
    2   7     2  (4, 7)                8     2  (1, 8)
    3   2     1  (no earlier b < 2)    3     2  (1, 3)
    4   -     -                        9     3  (4, 7, 9)

The answer is 3, from X = {4, 7, 9}, the same as in the assignment.

Making it fast: a Fenwick tree
------------------------------
Computed directly, each max(...) scans all earlier positions: O(n^2) in total.
On longest_seq5.txt (10,000 + 10,000 values) that took 25 seconds.

Instead, two Fenwick trees (binary indexed trees), ends_in_a and ends_in_b,
hold the sequences found so far that end in A and in B, indexed by the RANK of
their last value (its position in the sorted list of all values). "Longest
sequence ending in B with last value < a_t" is then one call,
ends_in_b.best(rank[a_t] - 1), in O(log n) time. Storing a new sequence with
update() is O(log n) too.

Running time O((i + j) log(i + j)), memory O(i + j). On longest_seq5.txt the
DP finishes in under 0.1 seconds with the same answer, 192. Because only ranks
are used, the values can be any integers, including 0 (in longest_seq3.txt)
and negative numbers.

Explanation of the code
-----------------------
PrefixMax
    The Fenwick tree. It stores (length, position) pairs, so the largest pair
    is the longest sequence and also says where it ends.
longest_alternating(a, b)
    Runs the DP. prev_a and prev_b record the position of the previous
    element; walking back from the end of the longest sequence, switching
    arrays at each step, rebuilds X for --show.
read_arrays(path)
    Reads the two sizes, then takes that many values for A and then for B.
main()
    Prints the output for every file named on the command line, and X itself
    when --show is given.


================================================================================
6. TESTING  (run_tests.py)
================================================================================

    python run_tests.py

run_tests.py does three things:

  1. Problem 1 (no input files): it imports bst.py and runs 200 rounds of 300
     random add_node / delete_node / find_node calls, comparing every result
     with a Python set. After each call the tree's in-order list must equal
     the sorted set; a binary tree is a valid BST exactly when its in-order
     list is sorted. It then runs  python bst.py --seed 1  and saves the
     demonstration in bst_output.txt.
  2. Problems 2 and 3: it runs the program on every vowel_input<id>.txt and
     longest_seq<id>.txt (the same commands as above) and saves each output
     as vowel_output<id>.txt or longest_output<id>.txt.
  3. It checks that the first line is "File Input: <file name>" and that the
     answer matches "answer <id>" in answers_vowel.txt or
     answers_longest_seq.txt, then prints PASS, FAIL or NO ANSWER for each
     test and a summary. A crash is reported as FAIL with its error message.
     The exit code is 1 if any test fails, 0 otherwise.

Result (takes about 2 seconds):

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

All expected answers come from the results listed in the assignment. To add a
test, save the input as the next number (for example longest_seq7.txt) and add
a line such as "answer 7: 5" to the answer file. run_tests.py finds new input
files by itself.

Brute-force checks
------------------
Besides the sample inputs, each program was compared with a slow but simple
method on random inputs, and all results matched:

  - Vowels: 3,000 random dot/dash strings, compared with listing every vowel
    string.
  - Longest sequence: 3,000 small random arrays, compared with an exhaustive
    search of all alternating sequences and with the direct O(n^2) DP. The
    sequence printed by --show was checked against every rule for all six
    input files.
  - BST: 300 rounds of 300 random calls, compared with a Python set.
