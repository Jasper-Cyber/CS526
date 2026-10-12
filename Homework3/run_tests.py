"""Run every program on its input files, write *_output_* files, compare with *_ans_*.

Usage: python3 run_tests.py
"""
import glob
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

# (program, folder, input glob, input name part, output name part, answer name part)
SUITES = [
    ("palindrome.py", "palendrom", "palendrome_[0-9]*.txt",
     "palendrome_", "palendrome_output_", "palendrome_ans_"),
    ("unique_substrings.py", "uniquesubstrings", "unique_substrings_input_*.txt",
     "unique_substrings_input_", "unique_substrings_output_", "unique_substrings_ans_"),
    ("ghostbusters.py", "ghostbusters", "ghostbusters_input_*.txt",
     "ghostbusters_input_", "ghostbusters_output_", "ghostbusters_ans_"),
]


def read_lines(path):
    with open(path, encoding="utf-8") as f:
        return f.read().splitlines()


def main():
    passed = failed = missing = 0
    for program, folder, pattern, in_part, out_part, ans_part in SUITES:
        for in_path in sorted(glob.glob(os.path.join(HERE, folder, pattern))):
            name = os.path.basename(in_path)
            out_path = os.path.join(HERE, folder, name.replace(in_part, out_part, 1))
            ans_path = os.path.join(HERE, folder, name.replace(in_part, ans_part, 1))

            with open(in_path, encoding="utf-8") as f:
                result = subprocess.run([sys.executable, os.path.join(HERE, program)],
                                        stdin=f, capture_output=True, text=True)
            with open(out_path, "w", encoding="utf-8", newline="\n") as f:
                f.write(result.stdout)

            label = f"{folder}/{name}"
            if not os.path.exists(ans_path):
                print(f"NO ANSWER {label}")
                missing += 1
            elif result.stdout.splitlines() == read_lines(ans_path):
                print(f"PASS      {label}")
                passed += 1
            else:
                print(f"FAIL      {label}")
                failed += 1

    print(f"\n{passed} passed, {failed} failed, {missing} without an answer file")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
