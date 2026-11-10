"""Problem 2: a binary min-heap built from linked nodes.

Usage: python linked_heap.py < heap/heap_input1.txt                (bash, Command Prompt)
       Get-Content heap/heap_input1.txt | python linked_heap.py    (PowerShell)
       python linked_heap.py heap/heap_input1.txt                   (any shell)
       python linked_heap.py heap/heap_input*.txt                   (several files)
       python linked_heap.py --demo heap/heap_input7.txt            (also try every other method)

Input:  one list of values, for example [8, 3, 5, 1].
Output: the input values, then the heap drawn after each insert, in the order given.
"""
import ast
import glob
import sys


class Node:
    """One heap node: a value and links to its left child, right child and parent."""

    __slots__ = ("value", "left", "right", "parent")

    def __init__(self, value, parent=None):
        self.value = value
        self.left = None
        self.right = None
        self.parent = parent


class MinHeap:
    """Binary min-heap stored as a tree of linked Nodes (no list or array).

    Two rules hold after every method call:
      - heap order:     every node's value is <= the values of its children,
                        so the smallest value is at the root;
      - complete shape: every level is full except possibly the last, which is
                        filled from the left.

    Positions are numbered 1, 2, 3, ... in level order. The binary digits of a
    position after the leading 1 are the path from the root (0 = left,
    1 = right), so the node at any position, including the next free one, is
    reached in O(log n) steps. Example: position 6 = 110 -> right, then left.
    """

    def __init__(self):
        self.root = None
        self._size = 0

    # ----- the required methods --------------------------------------------

    def insert(self, value):
        """Add value at the next free position, then move it up. O(log n)."""
        self._size += 1
        if self.root is None:
            self.root = Node(value)
            return
        parent = self._node_at(self._size // 2)       # the parent of position n is n // 2
        node = Node(value, parent)
        if self._size % 2 == 0:                       # even positions are left children
            parent.left = node
        else:
            parent.right = node
        self._sift_up(node)

    def peek(self):
        """Return the smallest value without removing it. O(1)."""
        if self.root is None:
            raise IndexError("peek from an empty heap")
        return self.root.value

    def extract_min(self):
        """Remove and return the smallest value. O(log n)."""
        if self.root is None:
            raise IndexError("extract_min from an empty heap")
        smallest = self.root.value
        self._remove(self.root)
        return smallest

    def delete(self, value):
        """Remove one copy of value. Return True if it was removed, False if it was not in the heap.

        Finding the value takes O(n) in the worst case, because a heap is not
        ordered left to right. Subtrees whose root is larger than value are
        skipped. Removing the node once found takes O(log n).
        """
        node = self._find(self.root, value)
        if node is None:
            return False
        self._remove(node)
        return True

    def build(self, values):
        """Replace the heap's contents with values, all at once, in O(n) time.

        The nodes are linked in level order and each subtree is made into a heap
        bottom-up: both child subtrees first, then the subtree's root is sifted
        down. Most nodes are near the bottom and move only a few levels, so the
        total work is O(n), less than the O(n log n) of n separate inserts.
        """
        values = list(values)          # only read while the nodes are created
        self._size = len(values)
        self.root = self._build_subtree(values, 1, None)

    def heap_sort(self):
        """Return the values in increasing order, leaving the heap unchanged. O(n log n).

        A copy of the tree is emptied with extract_min; the heap itself is not touched.
        """
        copy = type(self)()
        copy.root = self._copy_subtree(self.root, None)
        copy._size = self._size
        result = []
        while not copy.is_empty():
            result.append(copy.extract_min())
        return result

    def is_empty(self):
        return self.root is None

    def __len__(self):
        return self._size

    def print_heap(self):
        """Draw the tree with the root at the top and a / or \\ above each child."""
        print("\n".join(self.draw()))

    # ----- helpers ---------------------------------------------------------

    def _node_at(self, position):
        """Return the node at a level-order position (1 = root), in O(log n) steps.

        Read the binary digits of position after the leading 1, from left to right:
        0 means go to the left child, 1 means go to the right child.
        """
        node = self.root
        for shift in range(position.bit_length() - 2, -1, -1):
            node = node.right if (position >> shift) & 1 else node.left
        return node

    def _sift_up(self, node):
        """Move node's value up while it is strictly smaller than its parent's value."""
        while node.parent is not None and node.value < node.parent.value:
            node.value, node.parent.value = node.parent.value, node.value
            node = node.parent

    def _sift_down(self, node):
        """Move node's value down while a child is strictly smaller (the smaller child, left on a tie)."""
        while True:
            smallest = node
            if node.left is not None and node.left.value < smallest.value:
                smallest = node.left
            if node.right is not None and node.right.value < smallest.value:
                smallest = node.right
            if smallest is node:
                return
            node.value, smallest.value = smallest.value, node.value
            node = smallest

    def _remove(self, node):
        """Remove node's value, keeping both rules.

        The last node (position n) is the only one that can go without breaking
        the complete shape. Unlink it and move its value into node. That value
        may be too small or too large for node's position, so it is sifted up or down.
        """
        last = self._node_at(self._size)
        parent = last.parent
        if parent is None:
            self.root = None
        elif parent.left is last:
            parent.left = None
        else:
            parent.right = None
        last.parent = None
        self._size -= 1
        if node is not last:
            node.value = last.value
            if node.parent is not None and node.value < node.parent.value:
                self._sift_up(node)
            else:
                self._sift_down(node)

    def _find(self, node, value):
        """Return a node holding value in node's subtree, or None.

        Every value in a subtree is >= its root, so a subtree whose root is
        larger than value cannot contain value and is skipped.
        """
        if node is None or value < node.value:
            return None
        if node.value == value:
            return node
        return self._find(node.left, value) or self._find(node.right, value)

    def _build_subtree(self, values, position, parent):
        """Link the nodes for position and its descendants; return the subtree root, now a heap."""
        if position > len(values):
            return None
        node = Node(values[position - 1], parent)
        node.left = self._build_subtree(values, 2 * position, node)
        node.right = self._build_subtree(values, 2 * position + 1, node)
        self._sift_down(node)          # both child subtrees are heaps already
        return node

    def _copy_subtree(self, node, parent):
        if node is None:
            return None
        copy = Node(node.value, parent)
        copy.left = self._copy_subtree(node.left, copy)
        copy.right = self._copy_subtree(node.right, copy)
        return copy

    def draw(self):
        """Return the lines of the drawing printed by print_heap.

        Each level gets a line of values, and between two levels a line of / and \\.
        The bottom level has one slot every `unit` columns (4 when no value is
        wider than 3 characters), and every level above has slots twice as far
        apart, so each parent sits exactly halfway between its two children's
        slots. Every value is centred on its slot, and each / or \\ is drawn halfway
        between a parent and its child. The picture is then shifted so it starts
        2 columns from the left edge.
        """
        if self.root is None:
            return ["(empty heap)"]
        levels = self._size.bit_length()
        unit = 4 * ((self._widest(self.root) + 4) // 4)   # a multiple of 4 wider than every value
        rows = [[] for _ in range(2 * levels - 1)]         # (column, text) pieces, left to right
        self._place(self.root, 0, 0, levels, unit, rows)
        shift = 2 - min(column for row in rows for column, _ in row)
        lines = []
        for row in rows:
            line = ""
            for column, text in row:
                line += " " * (column + shift - len(line)) + text
            lines.append(line)
        return lines

    def _place(self, node, depth, index, levels, unit, rows):
        """Add node (the index-th node of its level, from 0) and its subtree to rows.

        A preorder walk reaches the nodes of each level from left to right, so
        every row is built in column order.
        """
        height = levels - 1 - depth                        # levels below this node
        center = (unit // 2) * 2 ** height * (2 * index + 1)
        label = str(node.value)
        rows[2 * depth].append((center - len(label) // 2, label))
        if height > 0:
            slant = (unit // 4) * 2 ** (height - 1)        # halfway to a child's center
            if node.left is not None:
                rows[2 * depth + 1].append((center - slant, "/"))
                self._place(node.left, depth + 1, 2 * index, levels, unit, rows)
            if node.right is not None:
                rows[2 * depth + 1].append((center + slant, "\\"))
                self._place(node.right, depth + 1, 2 * index + 1, levels, unit, rows)

    def _widest(self, node):
        if node is None:
            return 0
        return max(len(str(node.value)), self._widest(node.left), self._widest(node.right))


# ----- reading input ------------------------------------------------------

def parse_values(text):
    """Return the list of numbers written in text, for example "[8, 3, 5, 1]"."""
    text = text.strip()
    try:
        values = ast.literal_eval(text)
    except (ValueError, SyntaxError):
        values = None
    if not isinstance(values, list) or not all(
            isinstance(value, (int, float)) and not isinstance(value, bool) for value in values):
        raise ValueError(f"the input is not a list of numbers such as [8, 3, 5, 1]: {text[:60]}")
    return values


def expand_wildcards(args):
    """Expand names such as heap/heap_input*.txt, which PowerShell and cmd pass on unexpanded.

    The matches come out in numeric order (input2 before input10): heap_sort on
    (length, name) pairs orders them, since sort() is not allowed.
    """
    paths = []
    for arg in args:
        matches = MinHeap()
        matches.build((len(match), match) for match in glob.glob(arg))
        ordered = [name for _, name in matches.heap_sort()]
        paths.extend(ordered or [arg])     # no match: keep the name, so the error message shows it
    return paths


def read_text(path, prompt):
    """Return the text of the file at path, or of standard input when path is None.

    Both are decoded as UTF-8, skipping the byte order mark some Windows editors
    put at the start of a file (standard input is read as bytes, because Windows
    would otherwise decode it with the local code page).
    """
    if path is None:
        if sys.stdin.isatty():
            print(f"{prompt}, then Ctrl+D (macOS/Linux) or Ctrl+Z and Enter (Windows):",
                  file=sys.stderr)
        return sys.stdin.buffer.read().decode("utf-8-sig", errors="replace")
    with open(path, encoding="utf-8-sig", errors="replace") as f:
        return f.read()


# ----- output -------------------------------------------------------------

def show_inserts(values):
    """The required output: the input values, then the heap after each insert."""
    print(f"Input values: {values}")
    heap = MinHeap()
    for value in values:
        heap.insert(value)
        print()
        print(f"After insert({value}):")
        heap.print_heap()


def show_other_methods(values):
    """--demo: try build, peek, len, is_empty, heap_sort, delete and extract_min on the same values."""
    print()
    print("=" * 60)
    print("The other methods, on the same values")
    print("=" * 60)
    heap = MinHeap()
    print(f"\nEmpty heap: len(heap) = {len(heap)}, is_empty() = {heap.is_empty()}")
    for method in (heap.peek, heap.extract_min):
        try:
            method()
        except IndexError as error:
            print(f"{method.__name__}() -> IndexError: {error}")
    if not values:
        return

    heap.build(values)
    print(f"\nbuild({values}):")
    heap.print_heap()
    print(f"len(heap) = {len(heap)}, is_empty() = {heap.is_empty()}, peek() = {heap.peek()}")
    before = heap.draw()
    print(f"\nheap_sort() -> {heap.heap_sort()}")
    print(f"heap unchanged after heap_sort(): {heap.draw() == before}")

    present = values[len(values) // 2]
    absent = max(values) + 1
    print(f"\ndelete({present}) -> {heap.delete(present)}")
    heap.print_heap()
    print(f"\ndelete({absent}) -> {heap.delete(absent)}")

    while not heap.is_empty():
        print(f"\nextract_min() -> {heap.extract_min()}")
        heap.print_heap()
    print(f"len(heap) = {len(heap)}, is_empty() = {heap.is_empty()}")


def main():
    args = sys.argv[1:]
    demo = "--demo" in args
    unknown = [arg for arg in args if arg.startswith("--") and arg != "--demo"]
    if unknown:
        print(f"Unknown option {unknown[0]}. Usage: python linked_heap.py [--demo] [input files ...]",
              file=sys.stderr)
        sys.exit(2)
    paths = expand_wildcards([arg for arg in args if arg != "--demo"]) or [None]
    status = 0
    for index, path in enumerate(paths):
        if len(paths) > 1:
            if index > 0:
                print()
            print(f"File Input: {path}")
        try:
            values = parse_values(read_text(path, "Type a list such as [8, 3, 5, 1]"))
        except (OSError, ValueError) as error:
            print(f"Error: {error}", file=sys.stderr)
            status = 1
            continue
        show_inserts(values)
        if demo:
            show_other_methods(values)
    sys.exit(status)


if __name__ == "__main__":
    main()
