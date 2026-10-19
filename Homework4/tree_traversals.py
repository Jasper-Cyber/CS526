"""Problem 1: build the two trees from the assignment and print their traversals.

Usage: python3 tree_traversals.py
"""
from collections import deque


class TreeNode:
    """General tree node with an ordered list of children (Problem 1.1)."""

    def __init__(self, label, children=()):
        self.label = label
        self.children = list(children)


class BinaryNode:
    """Binary tree node with optional left and right children (Problem 1.2)."""

    def __init__(self, label, left=None, right=None):
        self.label = label
        self.left = left
        self.right = right


def preorder(node):
    """Visit the node, then each subtree from left to right."""
    order = [node.label]
    for child in node.children:
        order += preorder(child)
    return order


def postorder(node):
    """Visit each subtree from left to right, then the node."""
    order = []
    for child in node.children:
        order += postorder(child)
    return order + [node.label]


def breadth_first(root):
    """Visit the tree level by level, left to right, using a FIFO queue."""
    order = []
    queue = deque([root])
    while queue:
        node = queue.popleft()
        order.append(node.label)
        queue.extend(node.children)
    return order


def inorder(node):
    """Visit the left subtree, then the node, then the right subtree."""
    if node is None:
        return []
    return inorder(node.left) + [node.label] + inorder(node.right)


def main():
    # Problem 1.1: A -> B, C, D;  B -> E, F;  D -> G;  E -> H;  F -> I
    tree = TreeNode("A", [
        TreeNode("B", [TreeNode("E", [TreeNode("H")]),
                       TreeNode("F", [TreeNode("I")])]),
        TreeNode("C"),
        TreeNode("D", [TreeNode("G")]),
    ])

    # Problem 1.2: A(B, C);  B(D, E);  D(-, G);  C(-, F);  F(H, I)
    binary_tree = BinaryNode(
        "A",
        BinaryNode("B", BinaryNode("D", right=BinaryNode("G")), BinaryNode("E")),
        BinaryNode("C", right=BinaryNode("F", BinaryNode("H"), BinaryNode("I"))),
    )

    print("Problem 1.1")
    print("Preorder:      " + " ".join(preorder(tree)))
    print("Breadth-first: " + " ".join(breadth_first(tree)))
    print("Postorder:     " + " ".join(postorder(tree)))
    print()
    print("Problem 1.2")
    print("In-order:      " + " ".join(inorder(binary_tree)))


if __name__ == "__main__":
    main()
