import sys

try:
    for line in sys.stdin:
        print(line, end="")
except UnicodeDecodeError:
    print(
        "Error: The input contains invalid text data.",
        file=sys.stderr
    )
    sys.exit(1)
except OSError as e:
    print(f"Error reading input: {e}", file=sys.stderr)
    sys.exit(1)