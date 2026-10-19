"""Run both programs on their input files, write *_output_* files, compare with the answer files.

Usage: python3 run_tests.py
"""
import glob
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

# (program, input glob, input prefix, output prefix, answer file, regex for the answer in the output)
SUITES = [
    ("smallestNumber.py", "fewest_[0-9]*.txt", "fewest_", "fewest_output_",
     "answers_fewest.txt", r"Answer: (-?\d+)"),
    ("rightTriangles.py", "rightangles_[0-9]*.txt", "rightangles_", "rightangles_output_",
     "answers_angles.txt", r"right triangles is: (\d+)"),
]


def read_answers(path):
    """Map test id to expected answer from lines like "answer1: 3" or "answer 1: 4"."""
    with open(path, encoding="utf-8") as f:
        return dict(re.findall(r"answer\s*(\w+):\s*(-?\d+)", f.read()))


def main():
    passed = failed = missing = 0
    for program, pattern, in_part, out_part, answer_file, answer_regex in SUITES:
        answers = read_answers(os.path.join(HERE, answer_file))
        for in_path in sorted(glob.glob(os.path.join(HERE, pattern))):
            name = os.path.basename(in_path)
            test_id = name[len(in_part):-len(".txt")]
            out_path = os.path.join(HERE, out_part + test_id + ".txt")

            with open(in_path, encoding="utf-8") as f:
                result = subprocess.run([sys.executable, os.path.join(HERE, program)],
                                        stdin=f, capture_output=True, text=True)
            with open(out_path, "w", encoding="utf-8", newline="\n") as f:
                f.write(result.stdout)

            match = re.search(answer_regex, result.stdout)
            got = match.group(1) if match else "no answer printed"
            expected = answers.get(test_id)
            if expected is None:
                print(f"NO ANSWER {name}: got {got}")
                missing += 1
            elif got == expected:
                print(f"PASS      {name}: {got}")
                passed += 1
            else:
                print(f"FAIL      {name}: got {got}, expected {expected}")
                failed += 1

    print(f"\n{passed} passed, {failed} failed, {missing} without an answer")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
