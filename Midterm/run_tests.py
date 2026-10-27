"""Run every program on all of its input files, write the output files, compare with the answer files.

Usage: python run_tests.py
"""
import glob
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

# (program, input prefix, output prefix, answer file)
SUITES = [
    ("snowfall.py", "snowfall_input", "snowfall_output", "answers_snowfall.txt"),
    ("pandemic.py", "pandemic_input", "pandemic_output", "answers_pandemic.txt"),
    ("puzzle_game.py", "puzzle_game_input", "puzzle_game_output", "answers_puzzle_game.txt"),
]


def read_answers(path):
    """Map test id to the expected last line of output, from lines like "answer 1: YES".

    Lines that do not start with "answer", such as # comments, are ignored.
    """
    answers = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            match = re.match(r"answer\s*(\w+):\s*(.*\S)", line)
            if match:
                answers[match.group(1)] = match.group(2)
    return answers


def find_test_ids(prefix):
    """Return the ids of all <prefix><id>.txt files, in numeric order (1, 2, ..., 10)."""
    paths = glob.glob(os.path.join(HERE, prefix + "*.txt"))
    ids = [os.path.basename(path)[len(prefix):-len(".txt")] for path in paths]
    return sorted(ids, key=lambda test_id: (len(test_id), test_id))


def run_program(program, in_path):
    """Run the program with the input file name as its argument; return (output, last line)."""
    result = subprocess.run([sys.executable, os.path.join(HERE, program), in_path],
                            capture_output=True, text=True)
    if result.returncode != 0:
        error = result.stderr.strip().splitlines()
        return result.stdout, "CRASHED: " + (error[-1] if error else "no error message")
    lines = result.stdout.strip().splitlines()
    return result.stdout, lines[-1] if lines else "(no output)"


def main():
    passed = failed = missing = 0
    for program, in_prefix, out_prefix, answer_file in SUITES:
        answers = read_answers(os.path.join(HERE, answer_file))
        for test_id in find_test_ids(in_prefix):
            in_name = f"{in_prefix}{test_id}.txt"
            output, got = run_program(program, os.path.join(HERE, in_name))
            with open(os.path.join(HERE, f"{out_prefix}{test_id}.txt"), "w",
                      encoding="utf-8", newline="\n") as f:
                f.write(output)

            expected = answers.get(test_id)
            if expected is None:
                print(f"NO ANSWER {in_name}: got {got}")
                missing += 1
            elif got == expected:
                print(f"PASS      {in_name}: {got}")
                passed += 1
            else:
                print(f"FAIL      {in_name}: got {got!r}, expected {expected!r}")
                failed += 1

    print(f"\n{passed} passed, {failed} failed, {missing} without an answer")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
