"""Problem 1: binary search tree with add, delete, find and print.

Usage: python bst.py              (a new random demonstration on every run)
       python bst.py --seed 7     (repeat the demonstration with seed 7)

The demonstration builds a tree from a random set of 5 to 50 numbers between
1 and 1000, adds and deletes values (printing the tree after every add and
delete), then searches for values that are and are not in the tree.
"""
import random
import sys


class Node:
    """Node ADT: one value and links to its left and right children."""

    def __init__(self, value):
        self.value = value
        self.left = None      # subtree with smaller values
        self.right = None     # subtree with larger values


class BST:
    """Binary search tree ADT.

    For every node, all values in its left subtree are smaller and all values in
    its right subtree are larger. Duplicates are not stored. add_node, find_node
    and delete_node follow a single path down from the root, so each takes O(h)
    time, where h is the height of the tree: about log n for random input and n
    in the worst case (values added in sorted order).
    """

    def __init__(self):
        self.root = None
        self.size = 0

    def add_node(self, value):
        """Insert value. Return False (and change nothing) if it is already in the tree."""
        if self.root is None:
            self.root = Node(value)
            self.size += 1
            return True
        node = self.root
        while True:
            if value == node.value:
                return False
            if value < node.value:
                if node.left is None:
                    node.left = Node(value)
                    break
                node = node.left
            else:
                if node.right is None:
                    node.right = Node(value)
                    break
                node = node.right
        self.size += 1
        return True

    def find_node(self, value):
        """Return the node that holds value, or None if value is not in the tree."""
        node = self.root
        while node is not None and node.value != value:
            node = node.left if value < node.value else node.right
        return node

    def delete_node(self, value):
        """Remove value. Return False (and change nothing) if it is not in the tree."""
        self.root, deleted = self._delete(self.root, value)
        if deleted:
            self.size -= 1
        return deleted

    def _delete(self, node, value):
        """Delete value from the subtree rooted at node.

        Returns the new root of that subtree and whether a node was deleted. The
        caller stores the returned root in the link it came from, which is how a
        parent's left or right link gets updated.
        """
        if node is None:
            return None, False
        if value < node.value:
            node.left, deleted = self._delete(node.left, value)
            return node, deleted
        if value > node.value:
            node.right, deleted = self._delete(node.right, value)
            return node, deleted

        # node holds value.
        if node.left is None:         # no children, or only a right child
            return node.right, True
        if node.right is None:        # only a left child
            return node.left, True
        # Two children: copy in the in-order successor (the smallest value in the
        # right subtree), then delete that successor from the right subtree.
        successor = node.right
        while successor.left is not None:
            successor = successor.left
        node.value = successor.value
        node.right, _ = self._delete(node.right, successor.value)
        return node, True

    def in_order(self):
        """Return all values in sorted order (left subtree, node, right subtree)."""
        values = []
        self._in_order(self.root, values)
        return values

    def _in_order(self, node, values):
        if node is not None:
            self._in_order(node.left, values)
            values.append(node.value)
            self._in_order(node.right, values)

    def height(self):
        """Return the number of nodes on the longest path from the root to a leaf."""
        return self._height(self.root)

    def _height(self, node):
        if node is None:
            return 0
        return 1 + max(self._height(node.left), self._height(node.right))

    def print_tree(self):
        """Print the tree sideways, then its values in order.

        The root is at the left edge. Each node's right (larger) subtree is drawn
        above it and its left (smaller) subtree below it, so turning the output
        90 degrees clockwise shows the usual top-down picture.
        """
        if self.root is None:
            print("(empty tree)")
            return
        print(f"Tree with {self.size} nodes, height {self.height()}:")
        lines = []
        self._draw(self.root, "", "", lines)
        for line in lines:
            print(line)
        print("In-order: " + " ".join(map(str, self.in_order())))

    def _draw(self, node, prefix, connector, lines):
        """Add the lines for the subtree at node to lines.

        connector is "/-- " for a right child, "\\-- " for a left child and ""
        for the root. A "|" is drawn where the line from a child to its parent
        passes the rows of the child's own subtree.
        """
        if node.right is not None:
            extra = "|   " if connector == "\\-- " else "    "
            self._draw(node.right, prefix + extra, "/-- ", lines)
        lines.append(prefix + connector + str(node.value))
        if node.left is not None:
            extra = "|   " if connector == "/-- " else "    "
            self._draw(node.left, prefix + extra, "\\-- ", lines)

    def nodes_with_children(self, count):
        """Return the values of the nodes that have exactly count children (0, 1 or 2)."""
        found = []
        self._collect(self.root, count, found)
        return found

    def _collect(self, node, count, found):
        if node is not None:
            children = (node.left is not None) + (node.right is not None)
            if children == count:
                found.append(node.value)
            self._collect(node.left, count, found)
            self._collect(node.right, count, found)


def heading(text):
    print()
    print("=" * 70)
    print(text)
    print("=" * 70)


def demo(seed):
    """Run the demonstration required by the assignment, using the given random seed."""
    rng = random.Random(seed)
    print(f"Random seed: {seed}  (run  python bst.py --seed {seed}  to repeat this run)")

    size = rng.randint(5, 50)
    input_set = rng.sample(range(1, 1001), size)
    heading(f"Input set: {size} random numbers between 1 and 1000")
    for start in range(0, size, 15):
        print(" ".join(f"{value:4}" for value in input_set[start:start + 15]))

    tree = BST()
    for value in input_set:
        tree.add_node(value)
    heading("Initial tree")
    tree.print_tree()

    # add_node: three new values, then one value that is already in the tree.
    for _ in range(3):
        value = rng.choice([v for v in range(1, 1001) if tree.find_node(v) is None])
        tree.add_node(value)
        heading(f"add_node({value})  ->  added")
        tree.print_tree()
    value = rng.choice(tree.in_order())
    tree.add_node(value)
    heading(f"add_node({value})  ->  already in the tree, nothing added")
    tree.print_tree()

    # delete_node: one example of each case, then a value that is not in the tree.
    cases = [
        ("a leaf (no children)", lambda: tree.nodes_with_children(0)),
        ("a node with one child", lambda: tree.nodes_with_children(1)),
        ("a node with two children", lambda: [v for v in tree.nodes_with_children(2)
                                              if v != tree.root.value]),
        ("the root", lambda: [tree.root.value] if tree.root else []),
    ]
    for description, choices in cases:
        options = choices()
        if not options:
            heading(f"delete_node: skipped deleting {description}, this tree has none")
            continue
        value = rng.choice(options)
        tree.delete_node(value)
        heading(f"delete_node({value})  ->  deleted {description}")
        tree.print_tree()
    value = rng.choice([v for v in range(1, 1001) if tree.find_node(v) is None])
    tree.delete_node(value)
    heading(f"delete_node({value})  ->  not in the tree, nothing deleted")
    tree.print_tree()

    # find_node: three numbers taken from the tree, three random numbers that are not in it.
    heading("find_node: 3 positive cases (in the tree), 3 negative cases (not in the tree)")
    targets = [rng.choice(tree.in_order()) for _ in range(3)]
    not_in_tree = [v for v in range(1, 1001) if tree.find_node(v) is None]
    targets += [rng.choice(not_in_tree) for _ in range(3)]
    for value in targets:
        result = "found" if tree.find_node(value) is not None else "not found"
        print(f"find_node({value})  ->  {result}")


def main():
    args = sys.argv[1:]
    if not args:
        seed = random.randrange(1_000_000)
    elif len(args) == 2 and args[0] == "--seed" and args[1].lstrip("-").isdigit():
        seed = int(args[1])
    else:
        print("Usage: python bst.py [--seed N]")
        sys.exit(2)
    demo(seed)


if __name__ == "__main__":
    main()
