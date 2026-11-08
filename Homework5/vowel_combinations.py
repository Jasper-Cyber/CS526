"""Problem 2: count the vowel-only letter sequences a string of dots and dashes can represent.

Usage: python vowel_combinations.py vowel_input1.txt [vowel_input2.txt ...]
       python vowel_combinations.py vowel_input*.txt

Input:  line 1 = n, line 2 = the n dots and dashes.
Output: File Input: vowel_input1.txt
        The Number of Vowel combinations is:  6
"""
import glob
import os
import sys

# Morse code of the five vowels.
VOWEL_CODES = {"A": ".-", "E": ".", "I": "..", "O": "---", "U": "..-"}


def count_vowel_sequences(symbols):
    """Return how many vowel sequences spell exactly the given dots and dashes.

    ways[k] is the number of vowel sequences that spell the first k symbols.
    The last vowel in such a sequence covers the final 1, 2 or 3 of those k
    symbols, so ways[k] is the sum of ways[k - len(code)] over every vowel code
    that matches the symbols just before position k. ways[0] = 1 counts the
    empty sequence. O(n) time and memory: 5 codes are tried at each position.
    """
    n = len(symbols)
    ways = [1] + [0] * n
    for k in range(1, n + 1):
        for code in VOWEL_CODES.values():
            start = k - len(code)
            if start >= 0 and symbols[start:k] == code:
                ways[k] += ways[start]
    return ways[n]


def read_symbols(path):
    """Return the first n dots and dashes from the file, ignoring spaces and line breaks."""
    with open(path, encoding="utf-8-sig") as f:
        tokens = f.read().split()
    n = int(tokens[0])
    return "".join(tokens[1:])[:n]


def expand_wildcards(args):
    """Expand names such as vowel_input*.txt, which PowerShell and cmd pass on unexpanded."""
    paths = []
    for arg in args:
        matches = sorted(glob.glob(arg), key=lambda path: (len(path), path))
        paths.extend(matches or [arg])
    return paths


def main():
    paths = expand_wildcards(sys.argv[1:])
    if not paths:
        print("Usage: python vowel_combinations.py vowel_input1.txt [more input files ...]")
        sys.exit(2)
    for index, path in enumerate(paths):
        if index > 0:
            print()
        print(f"File Input: {os.path.basename(path)}")
        print(f"The Number of Vowel combinations is:  {count_vowel_sequences(read_symbols(path))}")


if __name__ == "__main__":
    main()
