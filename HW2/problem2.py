class Node:
    """A single node in a singly linked list."""

    def __init__(self, value):
        self.value = value
        self.next = None


class SinglyLinkedList:
    """A singly linked list with head/tail references and a node count."""

    def __init__(self):
        self.head = None
        self.tail = None
        self.count = 0

    # ---------------------------------------------------------------
    # Create
    # ---------------------------------------------------------------

    def append(self, value):
        """Add a value to the end of the list."""
        new_node = Node(value)
        if self.head is None or self.tail is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self.count += 1

    def prepend(self, value):
        """Add a value to the front of the list."""
        new_node = Node(value)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head = new_node
        self.count += 1

    def insert(self, index, value):
        """Insert a value at the given position (0-based)."""
        if index < 0 or index > self.count:
            raise IndexError("insert index out of range")

        if index == 0:
            self.prepend(value)
            return
        if index == self.count:
            self.append(value)
            return

        new_node = Node(value)
        prev_node = self._node_at(index - 1)
        new_node.next = prev_node.next
        prev_node.next = new_node
        self.count += 1

    # ---------------------------------------------------------------
    # Read
    # ---------------------------------------------------------------

    def get(self, index):
        """Return the value at the given position."""
        return self._node_at(index).value

    def find(self, value):
        """Return the position of the first node holding value, or -1."""
        current = self.head
        index = 0
        while current is not None:
            if current.value == value:
                return index
            current = current.next
            index += 1
        return -1

    def __len__(self):
        """Return the number of nodes in the list."""
        return self.count

    # ---------------------------------------------------------------
    # Update
    # ---------------------------------------------------------------

    def update(self, index, value):
        """Replace the value at the given position."""
        node = self._node_at(index)
        node.value = value

    # ---------------------------------------------------------------
    # Delete
    # ---------------------------------------------------------------

    def delete(self, value):
        """Remove the first node holding value.

        Returns True if a node was removed, False otherwise.
        """
        prev_node = None
        current = self.head

        while current is not None:
            if current.value == value:
                if prev_node is None:
                    # Removing the head
                    self.head = current.next
                else:
                    prev_node.next = current.next

                if current is self.tail:
                    self.tail = prev_node

                self.count -= 1
                return True

            prev_node = current
            current = current.next

        return False

    def delete_at(self, index):
        """Remove the node at the given position and return its value."""
        if index < 0 or index >= self.count:
            raise IndexError("delete_at index out of range")

        if index == 0:
            removed_node = self.head
            self.head = removed_node.next
            if self.head is None:
                self.tail = None
        else:
            prev_node = self._node_at(index - 1)
            removed_node = prev_node.next
            prev_node.next = removed_node.next
            if removed_node is self.tail:
                self.tail = prev_node

        self.count -= 1
        return removed_node.value

    # ---------------------------------------------------------------
    # Print
    # ---------------------------------------------------------------

    def print_list(self):
        """Print the list from head to tail, e.g. 12 -> 3 -> 5 -> 2."""
        if self.head is None:
            print("(empty)")
            return

        values = []
        current = self.head
        while current is not None:
            values.append(str(current.value))
            current = current.next
        print(" -> ".join(values))

    # ---------------------------------------------------------------
    # Internal helper
    # ---------------------------------------------------------------

    def _node_at(self, index):
        """Return the Node object at the given position (0-based)."""
        if index < 0 or index >= self.count:
            raise IndexError("index out of range")

        current = self.head
        for _ in range(index):
            current = current.next
        return current


if __name__ == "__main__":
    # Simple manual demo / sanity check
    sll = SinglyLinkedList()
    sll.print_list()          # (empty)

    sll.append(3)
    sll.append(5)
    sll.append(2)
    sll.prepend(12)
    sll.print_list()          # 12 -> 3 -> 5 -> 2

    print("len:", len(sll))              # 4
    print("get(1):", sll.get(1))         # 3
    print("find(5):", sll.find(5))       # 2
    print("find(99):", sll.find(99))     # -1

    sll.insert(2, 99)
    sll.print_list()          # 12 -> 3 -> 99 -> 5 -> 2

    sll.update(0, 100)
    sll.print_list()          # 100 -> 3 -> 99 -> 5 -> 2

    print("delete(99):", sll.delete(99))       # True
    sll.print_list()          # 100 -> 3 -> 5 -> 2

    print("delete_at(0):", sll.delete_at(0))   # 100
    sll.print_list()          # 3 -> 5 -> 2

    print("delete(999):", sll.delete(999))     # False
