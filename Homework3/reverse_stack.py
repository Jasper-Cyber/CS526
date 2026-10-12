"""Problem 3: reverse a stack in place, recursively, for three implementations.

Usage: python3 reverse_stack.py
"""


class ArrayStack:
    """Stack backed by a Python list; the end of the list is the top."""

    def __init__(self):
        self._data = []

    def push(self, value):
        self._data.append(value)

    def pop(self):
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._data.pop()

    def peek(self):
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self._data[-1]

    def is_empty(self):
        return len(self._data) == 0

    def reverse(self):
        self._reverse(0, len(self._data) - 1)

    def _reverse(self, lo, hi):
        """Swap the outermost pair, then recurse on the inner range."""
        if lo >= hi:
            return
        self._data[lo], self._data[hi] = self._data[hi], self._data[lo]
        self._reverse(lo + 1, hi - 1)

    def to_list(self):
        """Values from bottom to top."""
        return list(self._data)


class _SNode:
    def __init__(self, value, next_node=None):
        self.value = value
        self.next = next_node


class SinglyLinkedStack:
    """Stack backed by a singly linked list; head is the top."""

    def __init__(self):
        self._head = None

    def push(self, value):
        self._head = _SNode(value, self._head)

    def pop(self):
        if self.is_empty():
            raise IndexError("pop from empty stack")
        node = self._head
        self._head = node.next
        return node.value

    def peek(self):
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self._head.value

    def is_empty(self):
        return self._head is None

    def reverse(self):
        self._head = self._reverse(self._head, None)

    def _reverse(self, node, prev):
        """Point node back at prev, then continue with the rest of the list.

        Returns the new head (the old last node).
        """
        if node is None:
            return prev
        rest = node.next
        node.next = prev
        return self._reverse(rest, node)

    def to_list(self):
        """Values from bottom to top (head is the top, so reverse the walk)."""
        values = []
        node = self._head
        while node is not None:
            values.append(node.value)
            node = node.next
        values.reverse()
        return values


class _DNode:
    def __init__(self, value, prev_node=None, next_node=None):
        self.value = value
        self.prev = prev_node
        self.next = next_node


class DoublyLinkedStack:
    """Stack backed by a doubly linked list; head is the bottom, tail is the top."""

    def __init__(self):
        self._head = None
        self._tail = None

    def push(self, value):
        node = _DNode(value, self._tail, None)
        if self._tail is None:
            self._head = node
        else:
            self._tail.next = node
        self._tail = node

    def pop(self):
        if self.is_empty():
            raise IndexError("pop from empty stack")
        node = self._tail
        self._tail = node.prev
        if self._tail is None:
            self._head = None
        else:
            self._tail.next = None
        return node.value

    def peek(self):
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self._tail.value

    def is_empty(self):
        return self._tail is None

    def reverse(self):
        self._swap_links(self._head)
        self._head, self._tail = self._tail, self._head

    def _swap_links(self, node):
        """Swap prev and next on node, then on every node after it."""
        if node is None:
            return
        rest = node.next
        node.prev, node.next = node.next, node.prev
        self._swap_links(rest)

    def to_list(self):
        """Values from bottom (head) to top (tail)."""
        values = []
        node = self._head
        while node is not None:
            values.append(node.value)
            node = node.next
        return values


def format_stack(stack):
    return ", ".join(str(v) for v in stack.to_list())


def main():
    implementations = [
        ("Array stack", ArrayStack()),
        ("Singly linked list stack", SinglyLinkedStack()),
        ("Doubly linked list stack", DoublyLinkedStack()),
    ]
    for i, (name, stack) in enumerate(implementations):
        for n in range(1, 11):
            stack.push(n)
        if i > 0:
            print()
        print(name)
        print("Before: " + format_stack(stack))
        stack.reverse()
        print("After:  " + format_stack(stack))


if __name__ == "__main__":
    main()
