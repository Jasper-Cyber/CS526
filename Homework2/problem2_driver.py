"""
Driver program for Problem 2.

Reads directives from standard input, one per line, and applies them
to a SinglyLinkedList. After processing every line, prints the
resulting list.

Usage:
    python3 problem2_driver.py < problem2Resources/problem2_basic.txt
"""

import sys

from problem2 import SinglyLinkedList


# Number of arguments each directive expects (not counting the
# directive name itself).
ARG_COUNTS = {
    "append": 1,
    "prepend": 1,
    "insert": 2,
    "get": 1,
    "find": 1,
    "len": 0,
    "update": 2,
    "delete": 1,
    "delete_at": 1,
    "print_list": 0,
}

# Which argument positions (0-based, within the directive's own args)
# must be whole numbers (indices).
INDEX_ARG_POSITIONS = {
    "insert": [0],
    "get": [0],
    "update": [0],
    "delete_at": [0],
}


def parse_value(token):
    """Convert a token to an int when possible, otherwise leave as str."""
    try:
        return int(token)
    except ValueError:
        return token


def parse_index(token):
    """Convert a token to an int index.

    Raises ValueError if the token is not a whole number.
    """
    return int(token)


def format_list(sll):
    """Return the arrow-joined string representation of the list."""
    if len(sll) == 0:
        return "(empty)"
    values = []
    node = sll.head
    while node is not None:
        values.append(str(node.value))
        node = node.next
    return " -> ".join(values)


def process_line(line_number, line, sll):
    """Parse and execute a single directive line.

    Prints a warning (to standard output) and returns without
    modifying the list if the line is invalid in any way.
    """
    stripped = line.strip()

    # Ignore blank lines and comments.
    if stripped == "" or stripped.startswith("#"):
        return

    tokens = stripped.split()
    directive = tokens[0]
    args = tokens[1:]

    if directive not in ARG_COUNTS:
        print(f"Warning: line {line_number}: unknown directive '{directive}'")
        return

    expected = ARG_COUNTS[directive]
    if len(args) != expected:
        print(
            f"Warning: line {line_number}: '{directive}' expects "
            f"{expected} argument(s), got {len(args)}"
        )
        return

    # Validate / convert any index-typed arguments up front.
    index_positions = INDEX_ARG_POSITIONS.get(directive, [])
    converted_args = list(args)
    for pos in index_positions:
        try:
            converted_args[pos] = parse_index(args[pos])
        except ValueError:
            print(
                f"Warning: line {line_number}: '{args[pos]}' is not a "
                f"whole number"
            )
            return

    try:
        if directive == "append":
            sll.append(parse_value(converted_args[0]))

        elif directive == "prepend":
            sll.prepend(parse_value(converted_args[0]))

        elif directive == "insert":
            index = converted_args[0]
            value = parse_value(converted_args[1])
            sll.insert(index, value)

        elif directive == "get":
            index = converted_args[0]
            value = sll.get(index)
            print(f"get({index}) = {value}")

        elif directive == "find":
            value = parse_value(converted_args[0])
            position = sll.find(value)
            print(f"find({value}) = {position}")

        elif directive == "len":
            print(f"len = {len(sll)}")

        elif directive == "update":
            index = converted_args[0]
            value = parse_value(converted_args[1])
            sll.update(index, value)

        elif directive == "delete":
            value = parse_value(converted_args[0])
            removed = sll.delete(value)
            if not removed:
                print(
                    f"Warning: line {line_number}: value '{value}' not "
                    f"found in list"
                )

        elif directive == "delete_at":
            index = converted_args[0]
            value = sll.delete_at(index)
            print(f"delete_at({index}) = {value}")

        elif directive == "print_list":
            sll.print_list()

    except IndexError:
        print(f"Warning: line {line_number}: index out of range")


def main():
    sll = SinglyLinkedList()

    for line_number, line in enumerate(sys.stdin, start=1):
        process_line(line_number, line, sll)

    print(f"Final list: {format_list(sll)}")


if __name__ == "__main__":
    main()
