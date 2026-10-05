"""
Problem 4 - Sorted Doubly Linked List

A doubly linked list that always keeps its values in ascending sorted
order. The caller never chooses a position - add(value) finds the
correct spot itself. Duplicate values are allowed.
"""
import sys

class Node:
    """A single node in a doubly linked list."""

    def __init__(self, value):
        self.value = value
        self.prev = None
        self.next = None


class SortedDoublyLinkedList:
    """A doubly linked list that maintains ascending sorted order."""

    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    # ---------------------------------------------------------------
    # Create
    # ---------------------------------------------------------------

    def add(self, value):
        """Insert value at its correct sorted position."""
        new_node = Node(value)

        if self.head is None:
            self.head = new_node
            self.tail = new_node
            self.size += 1
            return

        # Walk forward to the first node whose value is greater than
        # the new value; the new node is inserted just before it.
        # Nodes with value <= new value are skipped, so duplicates are
        # inserted after any existing equal values (order is still
        # correctly ascending either way).
        current = self.head
        while current is not None and current.value <= value:
            current = current.next

        if current is None:
            # New value is the largest - append at the tail.
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        elif current is self.head:
            # New value is the smallest - becomes the new head.
            new_node.next = current
            current.prev = new_node
            self.head = new_node
        else:
            # Insert between current.prev and current.
            prev_node = current.prev
            prev_node.next = new_node
            new_node.prev = prev_node
            new_node.next = current
            current.prev = new_node

        self.size += 1

    # ---------------------------------------------------------------
    # Delete
    # ---------------------------------------------------------------

    def delete(self, value):
        """Remove one node holding value.

        Returns True if a node was removed, False if value is not
        in the list.
        """
        current = self.head
        while current is not None:
            if current.value == value:
                self._unlink(current)
                self.size -= 1
                return True
            if current.value > value:
                # Sorted ascending - value can't appear further on.
                return False
            current = current.next
        return False

    def _unlink(self, node):
        """Remove node from the list, patching prev/next links."""
        if node.prev is not None:
            node.prev.next = node.next
        else:
            self.head = node.next

        if node.next is not None:
            node.next.prev = node.prev
        else:
            self.tail = node.prev

    # ---------------------------------------------------------------
    # Read
    # ---------------------------------------------------------------

    def exists(self, value):
        """Return True if value is in the list, else False."""
        return self._exists_helper(self.head, value)

    def _exists_helper(self, node, value):
        if node is None or node.value > value:
            # Sorted ascending: once we pass value, it can't appear.
            return False
        if node.value == value:
            return True
        return self._exists_helper(node.next, value)

    def count(self, value):
        """Return how many times value appears in the list."""
        return self._count_helper(self.head, value)

    def _count_helper(self, node, value):
        if node is None or node.value > value:
            # Sorted ascending: stop as soon as we pass value.
            return 0
        if node.value == value:
            return 1 + self._count_helper(node.next, value)
        return self._count_helper(node.next, value)

    def total(self):
        """Return the sum of all values in the list (0 if empty)."""
        return self._total_helper(self.head)

    def _total_helper(self, node):
        if node is None:
            return 0
        return node.value + self._total_helper(node.next)

    def sum_middle_three(self):
        """Return the sum of the three middle nodes.

        n = number of nodes, mid = n // 2 (positions counted from 0
        at the head):
            n odd:  nodes at mid-1, mid, mid+1
            n even: nodes at mid-2, mid-1, mid
        Raises ValueError if the list has fewer than 3 nodes.
        """
        n = self.size
        if n < 3:
            raise ValueError("list must have at least 3 nodes")

        mid = n // 2
        if n % 2 == 1:
            positions = (mid - 1, mid, mid + 1)
        else:
            positions = (mid - 2, mid - 1, mid)

        return sum(self._value_at(pos) for pos in positions)

    def median(self):
        """Return the median value of the list.

        n odd:  the value of the middle node
        n even: the average of the two middle values
        Raises ValueError if the list is empty.
        """
        n = self.size
        if n == 0:
            raise ValueError("list is empty")

        mid = n // 2
        if n % 2 == 1:
            return self._value_at(mid)
        return (self._value_at(mid - 1) + self._value_at(mid)) / 2

    def _value_at(self, index):
        """Return the value at the given position via recursion."""
        return self._node_at(self.head, index).value

    def _node_at(self, node, remaining):
        if remaining == 0:
            return node
        return self._node_at(node.next, remaining - 1)

    # ---------------------------------------------------------------
    # Print
    # ---------------------------------------------------------------

    def print_list(self):
        """Print the list from head to tail, e.g. 2 <-> 4 <-> 8 <-> 10."""
        if self.head is None:
            print("(empty)")
            return

        values = self._collect_values(self.head)
        print(" <-> ".join(str(v) for v in values))

    def _collect_values(self, node):
        if node is None:
            return []
        return [node.value] + self._collect_values(node.next)


# =====================================================================
# Driver - reads directives from standard input, one per line
# =====================================================================

# Number of arguments each directive expects (not counting the
# directive name itself).
ARG_COUNTS = {
    "add": 1,
    "delete": 1,
    "exists": 1,
    "count": 1,
    "total": 0,
    "sum_middle_three": 0,
    "median": 0,
    "print_list": 0,
}


def parse_number(token):
    """Convert a token to an int, or a float if it has a decimal part.

    Raises ValueError if the token is not a number. Values must be
    numbers so they can be compared and summed.
    """
    try:
        return int(token)
    except ValueError:
        return float(token)


def format_list(sll):
    """Return the <-> joined string representation of the list."""
    if sll.head is None:
        return "(empty)"
    return " <-> ".join(str(v) for v in sll._collect_values(sll.head))


def process_line(line_number, line, sll):
    """Parse and execute a single directive line.

    Prints a warning and returns without modifying the list if the
    line is invalid in any way.
    """
    stripped = line.strip()

    # Ignore blank lines and comments.
    if stripped == "" or stripped.startswith("#"):
        return

    tokens = stripped.split()
    directive = tokens[0].lower()        # ADD, Add, add are all the same
    args = tokens[1:]

    if directive not in ARG_COUNTS:
        print(f"Warning: line {line_number}: unknown directive '{tokens[0]}'")
        return

    expected = ARG_COUNTS[directive]
    if len(args) != expected:
        print(
            f"Warning: line {line_number}: '{directive}' expects "
            f"{expected} argument(s), got {len(args)}"
        )
        return

    value = None
    if expected == 1:
        try:
            value = parse_number(args[0])
        except ValueError:
            print(f"Warning: line {line_number}: '{args[0]}' is not a number")
            return

    try:
        if directive == "add":
            sll.add(value)

        elif directive == "delete":
            print(f"delete({value}): {sll.delete(value)}")

        elif directive == "exists":
            print(f"exists({value}): {sll.exists(value)}")

        elif directive == "count":
            print(f"count({value}): {sll.count(value)}")

        elif directive == "total":
            print(f"total(): {sll.total()}")

        elif directive == "sum_middle_three":
            print(f"sum_middle_three(): {sll.sum_middle_three()}")

        elif directive == "median":
            print(f"median(): {sll.median()}")

        elif directive == "print_list":
            sll.print_list()

    except ValueError as error:          # too few nodes for median / middle three
        print(f"Warning: line {line_number}: {directive}: {error}")


def run_demo():
    """Built-in demo: the example from Problem 4.1."""
    sll = SortedDoublyLinkedList()

    print("Adding 10, 4, 29, 8, 2, 15, 41 ...")
    for value in (10, 4, 29, 8, 2, 15, 41):
        sll.add(value)
    sll.print_list()                                  # 2 <-> 4 <-> 8 <-> 10 <-> 15 <-> 29 <-> 41
    print("total():", sll.total())                    # 109
    print("sum_middle_three():", sll.sum_middle_three())  # 33 (8 + 10 + 15)
    print("median():", sll.median())                  # 10

    print("\ndelete(41):", sll.delete(41))
    sll.print_list()                                  # 2 <-> 4 <-> 8 <-> 10 <-> 15 <-> 29
    print("total():", sll.total())                    # 68
    print("sum_middle_three():", sll.sum_middle_three())  # 22 (4 + 8 + 10)
    print("median():", sll.median())                  # 9.0 ((8 + 10) / 2)

    print("\nadd(8)")
    sll.add(8)
    sll.print_list()                                  # 2 <-> 4 <-> 8 <-> 8 <-> 10 <-> 15 <-> 29
    print("count(8):", sll.count(8))                  # 2
    print("count(5):", sll.count(5))                  # 0
    print("exists(15):", sll.exists(15))              # True
    print("exists(5):", sll.exists(5))                # False


def main():
    if sys.stdin.isatty():               # no file given: use the built-in demo
        run_demo()
        return

    sll = SortedDoublyLinkedList()
    for line_number, line in enumerate(sys.stdin, start=1):
        process_line(line_number, line, sll)

    print(f"Final list: {format_list(sll)}")


if __name__ == "__main__":
    main()
