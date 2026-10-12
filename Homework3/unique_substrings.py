"""Problem 2: recursively find, print and count every unique substring.

Usage: python3 unique_substrings.py < uniquesubstrings/unique_substrings_input_0.txt
"""
import sys


def collect_from(text, start, end, found):
    """Add text[start:end], text[start:end+1], ... text[start:] to found."""
    if end > len(text):
        return
    found.add(text[start:end])
    collect_from(text, start, end + 1, found)


def collect_substrings(text, start, found):
    """Add every substring that begins at index start or later to found."""
    if start >= len(text):
        return
    collect_from(text, start, start + 1, found)
    collect_substrings(text, start + 1, found)


def unique_substrings(text):
    found = set()
    collect_substrings(text, 0, found)
    return sorted(found)


def main():
    text = sys.stdin.readline().rstrip("\r\n")
    substrings = unique_substrings(text)
    for s in substrings:
        print(s)
    print(len(substrings))


if __name__ == "__main__":
    main()
