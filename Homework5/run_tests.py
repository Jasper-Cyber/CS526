"""Test all three problems: the BST against a Python set, Problems 2 and 3 against the answer files.

Usage: python run_tests.py
"""
import glob
import os
import random
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.dont_write_bytecode = True   # do not leave a __pycache__ folder behind
import bst  # noqa: E402  (needs HERE on the import path first)

# (program, input glob, input prefix, output prefix, answer file, regex that finds the answer)
SUITES = [
    ("vowel_combinations.py", "vowel_input[0-9]*.txt", "vowel_input", "vowel_output",
     "answers_vowel.txt", r"The Number of Vowel combinations is:\s+(\d+)"),
    ("longest_seq.py", "longest_seq[0-9]*.txt", "longest_seq", "longest_output",
     "answers_longest_seq.txt", r"Longest Sequence: (\d+)"),
]


def check_bst(runs=200, operations=300):
    """Compare the BST with a Python set over random add, delete and find calls.

    Values come from 1..60, so adding a value that is already there and
    deleting or finding a missing value happen often. After every call the
    in-order list must equal the sorted set: a binary tree is a valid BST
    exactly when its in-order list is sorted. Returns an error message or None.
    """
    rng = random.Random(1)
    for trial in range(runs):
        tree, reference = bst.BST(), set()
        for _ in range(operations):
            value = rng.randint(1, 60)
            action = rng.choice(["add", "delete", "find"])
            if action == "add":
                ok = tree.add_node(value) == (value not in reference)
                reference.add(value)
            elif action == "delete":
                ok = tree.delete_node(value) == (value in reference)
                reference.discard(value)
            else:
                ok = (tree.find_node(value) is not None) == (value in reference)
            if not ok or tree.in_order() != sorted(reference) or tree.size != len(reference):
                return f"run {trial}: wrong result after {action}({value})"
    return None


def read_answers(path):
    """Map test id to expected answer, from lines like "answer 1: 6". Other lines are ignored."""
    with open(path, encoding="utf-8") as f:
        return dict(re.findall(r"^answer\s*(\w+):\s*(\S+)", f.read(), re.MULTILINE))


def find_test_ids(pattern, prefix):
    """Return the ids of the input files matching pattern, in numeric order (1, 2, ..., 10)."""
    names = [os.path.basename(path) for path in glob.glob(os.path.join(HERE, pattern))]
    ids = [name[len(prefix):-len(".txt")] for name in names]
    return sorted(ids, key=lambda test_id: (len(test_id), test_id))


def run(args):
    """Run a Python program from this folder; return (exit code, output, last error line).

    check=False: a crash must not stop the test run, so the exit code is returned
    and reported as a FAIL instead.
    """
    result = subprocess.run([sys.executable] + args, check=False,
                            capture_output=True, text=True, cwd=HERE)
    error = result.stderr.strip().splitlines()
    return result.returncode, result.stdout, error[-1] if error else ""


def main():
    passed = failed = missing = 0

    def report(ok, text):
        nonlocal passed, failed
        print(f"{'PASS' if ok else 'FAIL':9} {text}")
        if ok:
            passed += 1
        else:
            failed += 1

    # Problem 1 has no input files: test the BST directly, then run the demonstration.
    problem = check_bst()
    report(problem is None,
           "bst.py: 200 runs of 300 random add/delete/find calls match a Python set"
           + (f" -- {problem}" if problem else ""))
    code, output, error = run(["bst.py", "--seed", "1"])
    with open(os.path.join(HERE, "bst_output.txt"), "w", encoding="utf-8", newline="\n") as f:
        f.write(output)
    complete = all(text in output for text in ("Initial tree", "->  found", "->  not found"))
    report(code == 0 and complete, "bst.py --seed 1: demonstration ran, output in bst_output.txt"
           + (f" -- CRASHED: {error}" if code else ""))

    # Problems 2 and 3: run every input file and compare with the answer file.
    for program, pattern, in_prefix, out_prefix, answer_file, answer_regex in SUITES:
        answers = read_answers(os.path.join(HERE, answer_file))
        for test_id in find_test_ids(pattern, in_prefix):
            name = f"{in_prefix}{test_id}.txt"
            code, output, error = run([program, name])
            with open(os.path.join(HERE, f"{out_prefix}{test_id}.txt"), "w",
                      encoding="utf-8", newline="\n") as f:
                f.write(output)

            match = re.search(answer_regex, output)
            if match:
                got = match.group(1)
            else:
                got = "CRASHED: " + error if code else "no answer printed"
            header_ok = output.startswith(f"File Input: {name}\n")
            expected = answers.get(test_id)
            if expected is None:
                print(f"NO ANSWER {name}: got {got}")
                missing += 1
            elif got == expected and header_ok:
                report(True, f"{name}: {got}")
            elif not header_ok and got == expected:
                report(False, f"{name}: first line is not 'File Input: {name}'")
            else:
                report(False, f"{name}: got {got}, expected {expected}")

    print(f"\n{passed} passed, {failed} failed, {missing} without an answer")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
