"""Test all three problems: the assignment's rules, random tests, and every input file.

Usage: python run_tests.py

Each program reads every <folder>/<name>_input<id>.txt from standard input. Its
output is saved as <folder>/<name>_output<id>.txt next to the input, overwritten
on every run. The output is compared with a simple reference method, and its
summary with the "<problem>-<id>: ..." line in the folder's answer file.
"""
import ast
import bisect
import glob
import os
import random
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.dont_write_bytecode = True   # do not leave a __pycache__ folder behind
import linked_heap     # noqa: E402  (needs HERE on the import path first)
import merge_logs      # noqa: E402
import running_median  # noqa: E402

PROGRAMS = ["merge_logs.py", "linked_heap.py", "running_median.py"]
BANNED_MODULES = {"heapq", "bisect", "statistics", "queue"}


class RuleBroken(Exception):
    pass


# ----- the assignment's rules ---------------------------------------------

def find_banned_code(program):
    """Return the banned imports and calls in program: library heaps, priority queues, sorting, medians."""
    with open(os.path.join(HERE, program), encoding="utf-8") as f:
        tree = ast.parse(f.read())
    found = []
    for node in ast.walk(tree):
        modules = []
        if isinstance(node, ast.Import):
            modules = [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom):
            modules = [node.module or ""]
        found += [f"import {module} (line {node.lineno})"
                  for module in modules if module.split(".")[0] in BANNED_MODULES]
        if isinstance(node, ast.Call):
            func = node.func
            if isinstance(func, ast.Name) and func.id == "sorted":
                found.append(f"sorted() (line {node.lineno})")
            elif isinstance(func, ast.Attribute) and func.attr == "sort":
                found.append(f".sort() (line {node.lineno})")
    return found


# ----- Problem 1 ----------------------------------------------------------

class CheckedQueue(merge_logs.PriorityQueue):
    """The program's PriorityQueue, raising RuleBroken if it holds more than `limit`
    entries or two entries from the same register."""
    limit = 0

    def __init__(self):
        super().__init__()
        self.registers = set()

    def push(self, entry):
        register = entry[1]
        if register in self.registers:
            raise RuleBroken(f"two entries from register {register}")
        self.registers.add(register)
        super().push(entry)
        if len(self) > CheckedQueue.limit:
            raise RuleBroken(f"{len(self)} entries for {CheckedQueue.limit} registers")

    def pop(self):
        entry = super().pop()
        self.registers.discard(entry[1])
        return entry


def reference_merge(logs):
    return sorted((time, register) for register, log in enumerate(logs, start=1) for time in log)


def check_merge(runs=2000):
    """Compare merge_logs with sorted() on random logs and on every input file, watching the queue."""
    rng = random.Random(1)
    cases = []
    for _ in range(runs):
        k = rng.randint(0, 8)
        cases.append([sorted(rng.randint(0, 15) for _ in range(rng.randint(0, 8))) for _ in range(k)])
    for path in glob.glob(os.path.join(HERE, "merge", "merge_input*.txt")):
        with open(path, encoding="utf-8-sig") as f:
            cases.append(merge_logs.read_logs(f.read()))

    merge_logs.PriorityQueue = CheckedQueue
    try:
        for logs in cases:
            CheckedQueue.limit = len(logs)
            if merge_logs.merge_logs(logs) != reference_merge(logs):
                return f"wrong merge of {logs}"
    except RuleBroken as error:
        return f"queue rule broken: {error}"
    finally:
        merge_logs.PriorityQueue = CheckedQueue.__bases__[0]
    return None


def expected_merge_output(text):
    logs = [ast.literal_eval(line) for line in text.splitlines() if line.strip()]
    merged = reference_merge(logs)
    return f"Registers: {len(logs)}\nTotal sales: {len(merged)}\nMerged log: {merged}\n"


def summarize_merge(output):
    registers = re.search(r"^Registers: (\d+)$", output, re.MULTILINE)
    sales = re.search(r"^Total sales: (\d+)$", output, re.MULTILINE)
    log = re.search(r"^Merged log: (.*)$", output, re.MULTILINE)
    if not (registers and sales and log):
        return None
    merged = ast.literal_eval(log.group(1))
    first = str(merged[0]) if merged else "none"
    last = str(merged[-1]) if merged else "none"
    return f"{registers.group(1)} registers, {sales.group(1)} sales, first {first}, last {last}"


# ----- Problem 2 ----------------------------------------------------------

def check_structure(heap):
    """Return what is wrong with the heap's links, heap order or complete shape, or None."""
    size = len(heap)
    if (heap.root is None) != (size == 0) or heap.is_empty() != (size == 0):
        return f"root, len() and is_empty() disagree (len = {size})"
    if heap.root is not None and heap.root.parent is not None:
        return "the root has a parent"
    count = 0
    stack = [(heap.root, 1)] if heap.root is not None else []
    while stack:
        node, position = stack.pop()
        count += 1
        if position > size:
            return f"a node at position {position}, but only {size} values (shape not complete)"
        for child, child_position in ((node.left, 2 * position), (node.right, 2 * position + 1)):
            if child is None:
                if child_position <= size:
                    return f"position {child_position} is empty (shape not complete)"
            elif child.parent is not node:
                return f"wrong parent link at position {child_position}"
            elif child.value < node.value:
                return f"heap order broken: {child.value} below {node.value}"
            else:
                stack.append((child, child_position))
    if count != size:
        return f"{count} nodes but len() = {size}"
    return None


def tree_snapshot(node):
    return None if node is None else (node.value, tree_snapshot(node.left), tree_snapshot(node.right))


def level_values(node):
    """The tree's values level by level: [[root], [left, right], ...]."""
    levels, current = [], [node] if node is not None else []
    while current:
        levels.append([n.value for n in current])
        current = [child for n in current for child in (n.left, n.right) if child is not None]
    return levels


def check_drawing(lines, levels):
    """Return a problem with a drawn tree, or None if every value is in its correct place.

    Row 2d must show level d's values in order. Each value must be left of its
    parent if it is a left child and right of it if it is a right child, with a
    / or \\ between them on the row in between.
    """
    if len(lines) != 2 * len(levels) - 1:
        return f"{len(lines)} lines for {len(levels)} levels"
    centers = []
    for depth, values in enumerate(levels):
        tokens = list(re.finditer(r"\S+", lines[2 * depth]))
        if [t.group() for t in tokens] != [str(v) for v in values]:
            return f"level {depth} shows {[t.group() for t in tokens]}, expected {values}"
        centers.append([(t.start() + t.end() - 1) / 2 for t in tokens])
    for depth in range(1, len(levels)):
        slashes = list(re.finditer(r"\S", lines[2 * depth - 1]))
        if len(slashes) != len(levels[depth]):
            return f"{len(slashes)} / or \\ above {len(levels[depth])} values on level {depth}"
        for j, slash in enumerate(slashes):
            parent, child = centers[depth - 1][j // 2], centers[depth][j]
            left = j % 2 == 0
            if slash.group() != ("/" if left else "\\") or not (
                    child < slash.start() < parent if left else parent < slash.start() < child):
                return f"value {levels[depth][j]} on level {depth} is not drawn as the " \
                       f"{'left' if left else 'right'} child of {levels[depth - 1][j // 2]}"
    return None


def check_heap(runs=100, operations=200):
    """Compare MinHeap with a sorted list over random calls of every method.

    Values come from 1..25, so duplicates, deleting a missing value and calls on
    an empty heap happen often. After every call the tree must have correct
    parent links, heap order and complete shape, and draw() must put each value
    in its place. Returns an error message or None.
    """
    rng = random.Random(1)
    actions = ["insert"] * 5 + ["extract_min", "peek", "delete", "heap_sort", "build"]
    for trial in range(runs):
        heap, reference = linked_heap.MinHeap(), []
        for _ in range(operations):
            action = rng.choice(actions)
            value = rng.randint(1, 25)
            call = f"{action}({value})" if action in ("insert", "delete") else f"{action}()"
            if action == "insert":
                heap.insert(value)
                bisect.insort(reference, value)
                ok = True
            elif action in ("extract_min", "peek"):
                try:
                    got = getattr(heap, action)()
                    ok = bool(reference) and got == reference[0]
                except IndexError:
                    ok = not reference
                if action == "extract_min" and reference:
                    reference.pop(0)
            elif action == "delete":
                ok = heap.delete(value) == (value in reference)
                if value in reference:
                    reference.remove(value)
            elif action == "heap_sort":
                before = tree_snapshot(heap.root)
                ok = heap.heap_sort() == reference and tree_snapshot(heap.root) == before
            else:
                values = [rng.randint(1, 25) for _ in range(rng.randint(0, 40))]
                call = f"build({values})"
                heap.build(values)
                reference = sorted(values)
                ok = True                      # checked by the length, structure and drawing checks below
            problem = None if ok else "wrong result"
            if not problem and len(heap) != len(reference):
                problem = f"len() = {len(heap)}, expected {len(reference)}"
            problem = problem or check_structure(heap)
            if not problem and heap.root is not None:
                problem = check_drawing(heap.draw(), level_values(heap.root))
            if problem:
                return f"run {trial}, {call}: {problem}"
    return None


def check_linked_storage():
    """Return a problem if the heap keeps its values in a list, tuple, dict or set instead of nodes."""
    if tuple(linked_heap.Node.__slots__) != ("value", "left", "right", "parent"):
        return f"Node has fields {linked_heap.Node.__slots__}"
    heap = linked_heap.MinHeap()
    heap.build(range(50, 0, -1))
    for value in range(20):
        heap.insert(value)
    heap.extract_min()
    heap.delete(30)
    containers = [name for name, value in vars(heap).items()
                  if isinstance(value, (list, tuple, dict, set))]
    return f"MinHeap stores {containers}" if containers else None


def check_heap_output(text, output):
    """Replay the inserts on an array heap (a value moves up only while strictly smaller
    than its parent) and check every tree drawn in the output against it."""
    values = ast.literal_eval(text.strip())
    blocks = output.rstrip("\n").split("\n\n")
    if blocks[0] != f"Input values: {values}":
        return f"first line is not 'Input values: {values}'"
    if len(blocks) != len(values) + 1:
        return f"{len(blocks) - 1} trees for {len(values)} inserts"
    array = []
    for value, block in zip(values, blocks[1:]):
        array.append(value)
        child = len(array) - 1
        while child > 0 and array[child] < array[(child - 1) // 2]:
            parent = (child - 1) // 2
            array[child], array[parent] = array[parent], array[child]
            child = parent
        header, *lines = block.split("\n")
        if header != f"After insert({value}):":
            return f"expected 'After insert({value}):', found '{header}'"
        levels = [array[2 ** d - 1:2 ** (d + 1) - 1] for d in range(len(array).bit_length())]
        problem = check_drawing(lines, levels)
        if problem:
            return f"after insert({value}): {problem}"
    return None


def summarize_heap(output):
    match = re.match(r"Input values: (.*)\n", output)
    if not match:
        return None
    values = ast.literal_eval(match.group(1))
    if not values:
        return "0 values, 0 levels, root none"
    tree = output.rstrip("\n").split("\n\n")[-1].split("\n")[1:]
    return f"{len(values)} values, {(len(tree) + 1) // 2} levels, root {tree[0].split()[0]}"


# ----- Problem 3 ----------------------------------------------------------

def reference_medians(sales):
    ordered, medians = [], []
    for amount in sales:
        bisect.insort(ordered, amount)
        n = len(ordered)
        medians.append(float(ordered[n // 2]) if n % 2 else (ordered[n // 2 - 1] + ordered[n // 2]) / 2)
    return medians


def check_median(runs=500):
    """Compare running_medians with a sorted-list median on random sales, and check after
    every sale that the two halves keep both invariants."""
    if running_median.MinHeap is not linked_heap.MinHeap:
        return "running_median.py does not use MinHeap from linked_heap.py"
    rng = random.Random(1)
    for trial in range(runs):
        sales = [rng.randint(-5, 20) for _ in range(rng.randint(0, 60))]
        if running_median.running_medians(sales) != reference_medians(sales):
            return f"run {trial}: wrong medians for {sales}"
        tracker = running_median.RunningMedian()
        for amount in sales:
            tracker.add(amount)
            lower, upper = tracker.lower, tracker.upper
            if not (isinstance(lower, linked_heap.MinHeap) and isinstance(upper, linked_heap.MinHeap)):
                return "the two halves are not MinHeaps"
            if not (len(lower) - len(upper) in (0, 1)):
                return f"run {trial}: halves of sizes {len(lower)} and {len(upper)}"
            if len(upper) and -lower.peek() > upper.peek():
                return (f"run {trial}: smaller half's largest {-lower.peek()} > "
                        f"larger half's smallest {upper.peek()}")
    return None


def expected_median_output(text):
    return f"{reference_medians(ast.literal_eval(text.strip()))}\n"


def summarize_median(output):
    try:
        medians = ast.literal_eval(output.strip())
    except (ValueError, SyntaxError):
        return None
    return f"{len(medians)} sales, final median {medians[-1] if medians else 'none'}"


# ----- running the programs -----------------------------------------------

# (problem, program, folder, input prefix, output prefix, answer file, summarize, check output)
SUITES = [
    (1, "merge_logs.py", "merge", "merge_input", "merge_output", "problem1_answers.txt",
     summarize_merge, lambda text, output: None if output == expected_merge_output(text)
     else "output differs from the sorted() reference"),
    (2, "linked_heap.py", "heap", "heap_input", "heap_output", "problem2_answers.txt",
     summarize_heap, check_heap_output),
    (3, "running_median.py", "median", "median_input", "median_output", "problem3_answers.txt",
     summarize_median, lambda text, output: None if output == expected_median_output(text)
     else "output differs from the sorted-list reference"),
]


def read_answers(path, problem):
    """Map test id to expected summary, from lines like "1-4: 0 registers, 0 sales, ..."."""
    with open(path, encoding="utf-8-sig") as f:
        return {test_id: text for number, test_id, text
                in re.findall(r"^(\d+)-(\w+):\s*(.*?)\s*$", f.read(), re.MULTILINE)
                if int(number) == problem}


def find_test_ids(folder, prefix):
    """Return the ids of the input files in folder, in numeric order (1, 2, ..., 10)."""
    names = [os.path.basename(path) for path in glob.glob(os.path.join(HERE, folder, f"{prefix}*.txt"))]
    ids = [name[len(prefix):-len(".txt")] for name in names]
    return sorted(ids, key=lambda test_id: (len(test_id), test_id))


def run(args, stdin_text=""):
    """Run a Python program from this folder; return (exit code, output, last error line).

    check=False: a crash must not stop the test run, so it is reported as a FAIL instead.
    """
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    result = subprocess.run([sys.executable, "-B"] + args, input=stdin_text, check=False,
                            capture_output=True, text=True, encoding="utf-8", cwd=HERE, env=env)
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

    # The rules: no library heap, priority queue, sorting or median code.
    banned = [f"{program}: {item}" for program in PROGRAMS for item in find_banned_code(program)]
    report(not banned, "rules: no heapq, queue, bisect, statistics, sorted() or .sort() in the programs"
           + (f" -- found {'; '.join(banned)}" if banned else ""))

    # Random tests against simple reference methods.
    for ok_text, check in [
        ("merge_logs.py: 2000 random merges and all input files match sorted(); "
         "queue never held more than k entries or two from one register", check_merge),
        ("linked_heap.py: 100 runs of 200 random calls of every method match a sorted list; "
         "links, heap order, complete shape and drawing correct after each call", check_heap),
        ("linked_heap.py: the heap is stored only in linked nodes (value, left, right, parent)",
         check_linked_storage),
        ("running_median.py: uses MinHeap from linked_heap.py; 500 random sale lists match a "
         "sorted-list median; both invariants hold after every sale", check_median),
    ]:
        try:
            problem = check()
        except Exception as crash:   # a crash in the program under test is a FAIL, not the end of the run
            problem = f"CRASHED: {type(crash).__name__}: {crash}"
        report(problem is None, ok_text + (f" -- {problem}" if problem else ""))

    # Problem 2's other methods, demonstrated on one input.
    code, output, error = run(["linked_heap.py", "--demo", os.path.join("heap", "heap_input7.txt")])
    with open(os.path.join(HERE, "heap", "heap_demo_output.txt"), "w", encoding="utf-8", newline="\n") as f:
        f.write(output)
    complete = all(text in output for text in ("IndexError", "heap unchanged after heap_sort(): True",
                                               "-> True", "-> False", "extract_min() ->"))
    report(code == 0 and complete, "linked_heap.py --demo heap/heap_input7.txt: every method shown, "
           "output in heap/heap_demo_output.txt" + (f" -- CRASHED: {error}" if code else ""))

    # Every input file, read from standard input as the assignment requires.
    for problem, program, folder, in_prefix, out_prefix, answer_file, summarize, check_output in SUITES:
        answers = read_answers(os.path.join(HERE, folder, answer_file), problem)
        test_ids = find_test_ids(folder, in_prefix)
        for test_id in test_ids:
            name = f"{folder}/{in_prefix}{test_id}.txt"
            with open(os.path.join(HERE, folder, f"{in_prefix}{test_id}.txt"), encoding="utf-8-sig") as f:
                text = f.read()
            code, output, error = run([program], text)
            with open(os.path.join(HERE, folder, f"{out_prefix}{test_id}.txt"), "w",
                      encoding="utf-8", newline="\n") as f:
                f.write(output)

            got = summarize(output) if code == 0 else None
            if got is None:
                got = f"CRASHED: {error}" if code else "output not in the expected format"
            expected = answers.get(f"{test_id}")
            mismatch = "crashed" if code else check_output(text, output)
            if expected is None:
                print(f"NO ANSWER {name}: got {got}" + (f" -- {mismatch}" if mismatch else ""))
                missing += 1
            elif got != expected:
                report(False, f"{name}: got {got}, expected {expected}")
            else:
                report(mismatch is None, f"{name}: {got}" + (f" -- {mismatch}" if mismatch else ""))
        for test_id in answers:
            if test_id not in test_ids:
                print(f"NO INPUT  {problem}-{test_id} in {folder}/{answer_file}: "
                      f"{folder}/{in_prefix}{test_id}.txt does not exist")
                missing += 1

    print(f"\n{passed} passed, {failed} failed, {missing} without an answer or an input file")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
