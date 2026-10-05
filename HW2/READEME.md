# CS526 Homework 2 Write-Up
### Jia Chen

* Python 3.13.3, standard library only. All files live in the same folder:

HW2/
├── problem2.py
├── problem2_driver.py
├── problem2Resources/
│   ├── problem2_basic.txt
│   └── problem2_errors.txt
├── problem3.py
|   problem4_*.txt
└── problem4.py


### Problem 1 
* What is the advantage of using a tail pointer in a linked list?
A tail pointer keeps a direct reference to the last node in a linked list, instead of forcing to walk from the head every time you need to reach the end. 

* Main advantages

- O(1) insertion at the end
Without a tail pointer, appending a new node requires traversing the entire list from head to find the last node — O(n). With a tail pointer, this process can be proceed in O(1) insertion by using "tail.next = newNode
tail = newNode "
- Efficient queue implementation
Many queues are implemented as linked lists where you enqueue at the tail and dequeue at the head. A tail pointer makes enqueue O(1) (paired with head making dequeue O(1) too) — without it, enqueue would be O(n), making the whole queue inefficient for large data.
- Useful for building/concatenating lists
If you're merging two linked lists (list1 + list2), having tail for list1 lets you do: "list1.tail.next = list2.head "  in O(1), rather than traversing list1 just to find where to attach list2.
- Doubly linked list traversal from the end
If your list is also doubly linked, having tail lets you traverse backward (end → start) immediately, without needing to walk forward first just to locate the end.

### Problem 2 – Singly Linked List and Driver
1. Introduction

The assignment asks for a Node class and a SinglyLinkedList class that supports create, read, update, delete, and print operations (Part A), plus a driver program that reads directives from standard input and applies them to a list (Part B).

problem2.py implements Node (value, next) and SinglyLinkedList (head, tail, count) with append, prepend, insert, get, find, __len__, update, delete, delete_at, and print_list.
problem2_driver.py reads one directive per line, calls the matching method, prints results for get, find, len, and delete_at, warns on bad lines, and finishes by printing Final list: ....
2. Algorithm

The list. The list stores a head reference, a tail reference, and a node count. An empty list has head = tail = None and count = 0.

append uses the tail pointer: tail.next = new; tail = new. This is O(1) instead of the O(n) walk needed without a tail. An empty list is a special case in which the new node becomes both head and tail.
prepend sets new.next = head; head = new (O(1)), and also sets tail when the list was empty.
insert(i, v) delegates to prepend for i == 0 and to append for i == count. Otherwise it walks to node i-1 and relinks: new.next = prev.next; prev.next = new.
get, update, insert, and delete_at share one private helper, _node_at(i), which checks the range and walks i steps from the head.
find walks the list comparing values and returns the index of the first match, or -1.
delete(v) walks while tracking the previous node, then bypasses the match with prev.next = cur.next (or moves head when the match is the first node). If the deleted node was the tail, tail moves back to prev.
delete_at(i) does the same relink by position and returns the removed value.
print_list joins the values with " -> ", or prints (empty).

The driver. For each stdin line:

Strip it. Skip it if it is blank or starts with #.
Split it into tokens. tokens[0] is the directive and the rest are arguments.
Validate in a fixed order. First check that the directive is in a table of known directives, then check that the argument count matches the table, then check that index arguments are whole numbers.
Call the method. IndexError from the list is caught and reported as "index out of range", and a False return from delete is reported as "value not found".

Every failure prints a Warning: line N: ... message and the loop continues.

3. Interesting (design choices, edge cases, trade-offs)
Table-driven validation. A dictionary maps each directive to its argument count, so "unknown directive" and "wrong number of arguments" are handled in one place and not in ten separate if branches.
Index vs. value parsing. Indices use int() with no fallback, so get abc is rejected. Values try int() and fall back to a string, so append 12 stores the number 12 and find 12 can match it.
Range rules differ by method. get, update, and delete_at accept 0 <= i < count, while insert accepts 0 <= i <= count because inserting at count means appending.
Edge cases handled. Empty list, one-node list, deleting the head, deleting the tail, and deleting the only node (which must reset both head and tail).
Trade-off. Keeping count makes len() O(1) but requires every method to update it correctly. delete_at of the last node is still O(n) because a singly linked list has no prev link.
Warnings go to standard output, as the spec says to "print" them. Sending them to standard error would keep them out of piped output.
4. How to run

Run from the HW2 folder, with problem2.py next to the driver (the driver imports it):
In Linux:
python3 problem2_driver.py < problem2Resources/problem2_basic.txt
python3 problem2_driver.py < problem2Resources/problem2_errors.txt
python3 problem2.py
In Windows:
python problem2_driver.py < problem2Resources/problem2_basic.txt
python problem2_driver.py < problem2Resources/problem2_errors.txt
python problem2.py


(On Windows Git Bash, use python if python3 is not found.)

Expected output for problem2_basic.txt:

get(2) = 3
Final list: 8 -> 12 -> 5 -> 7

problem2_errors.txt exercises every warning path (unknown directive, wrong argument count, non-integer index, out-of-range index, deleting a missing value) and shows that valid lines after a bad line are still processed. Running python3 problem2.py directly runs a small built-in self-test of every list method.

### Problem3 - Climbing Stairs
1. Introduction

The assignment asks for a recursive function ways(n), with no loops, that counts the ways to climb n stairs taking 1, 2, or 3 steps per move, and for ways(3), ways(5), ways(10), plus answers to two questions. problem3.py implements ways and prints those three values.

2. Algorithm

Think about the first move. It is 1, 2, or 3 steps, and in each case a smaller staircase remains. The total is the sum of the three smaller problems:

ways(n) = ways(n-1) + ways(n-2) + ways(n-3)

Base cases: ways(0) = 1 (standing exactly at the top is one valid finish) and ways(n) = 0 for n < 0 (a move that overshoots is not a valid path).

Output:

ways(3) = 4
ways(5) = 13
ways(10) = 274

Check: ways(4) = 7, matching the example in the assignment.

a Base cases. ways(0) = 1 because a path that lands exactly on the top contributes one way to the sum above it. If it were 0, every successful path would vanish from the count. ways(n) = 0 for negative n because an overshoot is not a way to reach the top.

b 1 or 2 steps only. The recurrence becomes ways(n) = ways(n-1) + ways(n-2) with ways(0) = ways(1) = 1, which is the Fibonacci sequence (ways(n) is the (n+1)-th Fibonacci number).

3. Interesting
Trade-off: this plain recursion recomputes the same subproblems, so it takes exponential time (about O(3^n)). That is fine for n = 10, but for large n it would need memoization (caching results), which is not required here.
Two base cases are needed. Without the n < 0 case, the calls ways(n-2) and ways(n-3) would recurse past zero forever.
4. How to run
In Linux:
python3 problem3.py
In Windows:
python problem3.py

### Problem 4 Sorted Doubly Linked List

1. Introduction

The assignment asks for a Node class (value, prev, next) and a SortedDoublyLinkedList that always stays in ascending order and allows duplicates. It must support add, delete, exists, print_list, total, sum_middle_three, median, and count(value), using recursion to walk the list where it makes sense, plus a short driver. problem4.py implements all of this, and its main() driver reproduces the assignment's example.

2. Algorithm

Insertion keeps order. add(v) walks forward while current.value <= v and inserts before the first larger node. Where the walk stops decides the case:

Where the walk stops	Case	Action
List empty	First node	head = tail = new
Ran off the end	New largest	Link after tail, move tail
At head	New smallest	Link before head, move head
Otherwise	Middle	Update prev.next, new.prev, new.next, current.prev

Because add is the only way in, every other method can rely on the list being sorted.

Deletion. delete(v) walks the list. On a match it unlinks the node with a helper that patches prev.next (or head) and next.prev (or tail). If it reaches a value larger than v, it stops and returns False.

Recursive helpers. Each public method calls a private helper that handles one node and then recurses on node.next:

Method	Base case	Recursive step
total	None returns 0	node.value + total(node.next)
exists	None or node.value > v returns False	True on a match, else recurse
count(v)	None or node.value > v returns 0	1 + ... on a match, else recurse
print_list	None returns an empty list	[node.value] + collect(node.next)

Position-based methods. A recursive _node_at(node, remaining) fetches the value at a position. With mid = size // 2:

sum_middle_three raises ValueError if size < 3. For odd sizes it sums positions mid-1, mid, mid+1, and for even sizes mid-2, mid-1, mid.
median raises ValueError if the list is empty. For odd sizes it returns the value at mid, and for even sizes the average of the values at mid-1 and mid.
3. Interesting
Early stopping. Since the list is sorted, exists, count, and delete stop as soon as they pass a value larger than the target, and do not scan to the end.
Naming bug avoided. The size counter is called size, not count. An instance attribute named count would shadow the required count(value) method and cause TypeError: 'int' object is not callable.
Duplicates. add inserts a new value after existing equal values. The list stays sorted either way, and delete removes only one matching node, as the spec says.
Types. median returns an int for odd sizes (10) and a float for even sizes (9.0), matching the assignment's example.
Trade-off: recursion depth. The recursive helpers use one stack frame per node. Python's default recursion limit is about 1000, so total() on a 2000-node list raises RecursionError. This is acceptable for the assignment's list sizes, and an iterative loop would remove the limit at the cost of not following the recursion guidance.
Trade-off: add is O(n). It always walks from the head. A fast path using tail (when value >= tail.value) would make adding a new maximum O(1), but was not needed.
4. How to run
In Linux:
python3 problem4.py
python3 problem4.py < problem4_basic.txt
In Windows
python problem4.py
python problem4.py < problem4_basic.txt

The built-in driver builds the list from 10, 4, 29, 8, 2, 15, 41 and shows every method. run code in HW2 folder with txt file in it will use these txt files as input.



