"""Problem 1: report whether each input line is a palindrome.

Usage: python3 palindrome.py < palendrom/palendrome_0.txt
"""
import sys


def is_palindrome(text):
    """Return True if text reads the same forwards and backwards.

    Single spaces between characters are ignored ("g e e k" == "geek").
    Case matters ("Aa" is not a palindrome).
    """
    chars = text.replace(" ", "")
    return chars == chars[::-1]


def main():
    count = 0
    for line in sys.stdin:
        line = line.rstrip("\r\n")
        if not line:
            continue
        result = is_palindrome(line)
        if result:
            count += 1
        print(result)
    print(count)


if __name__ == "__main__":
    main()
