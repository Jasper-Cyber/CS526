# CS526 – HelloWorld Assignment Write-Up

## Purpose

The purpose of this assignment is to confirm that a working Python
development environment is set up correctly and that basic
command-line I/O works end-to-end. The program itself is
intentionally simple: it reads a text file containing an arbitrary
number of lines from standard input and echoes those lines back to
standard output, unchanged. Getting this trivial pipeline working
end-to-end (editor/IDE → interpreter → shell → redirection) is a
prerequisite for all later, more complex assignments in the course.

## Environment — Python Version

- **Language:** Python 3
- **Version used:** Python 3.13.3 (any Python 3.6+ interpreter will run
  this code, since it uses only the standard library — `sys` — and no
  version-specific syntax)
- **Dependencies:** None. Only the built-in `sys` module is imported;
  no `pip install` or virtual environment is required.
- **Verify your interpreter** before running the program in my Windows system Git Bash terminal:
  ```
  python --version
  ```
  If running in a linux terminal, you may need to use
  python3 --version

## Implementation Explanation

The program is a single file, `helloworld.py`. It does the following:

1. Imports the `sys` module, which exposes the process's standard
   input/output streams as `sys.stdin` and `sys.stdout`.
2. Opens a `try` block and iterates over `sys.stdin` line by line
   using a `for` loop.
3. For each line read, it calls `print(line, end="")`, writing the
   line to standard output immediately.
4. Wraps the loop in exception handling so that if the input stream
   contains invalid text data, or if an OS-level error occurs while
   reading, the program prints a clear message to standard error and
   exits with a non-zero status code (rather than crashing with a raw
   traceback).

```python
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
```

## How Standard Input Works

Standard input (`stdin`) is one of three standard streams every
process gets when it starts (the other two being `stdout` and
`stderr`). By default, `stdin` is connected to the keyboard, so a
program that reads from it will wait for the user to type. However,
the shell lets you **redirect** `stdin` so that it instead reads from
a file, using the `<` operator: 

```
python helloworld.py < myfile.txt
```

Here, the shell opens `myfile.txt`, connects its contents to the
program's `stdin` file descriptor, and the Python program is
completely unaware of the difference — from its point of view, it is
simply reading characters from `sys.stdin` as they come, whether
they originate from a keyboard or a file.

In Python, `sys.stdin` behaves like an iterable text-mode file
object, which is what allows the `for line in sys.stdin:` construct
to work. It can recoganize the file content if it is text content, no 
matter what extentions the file has.

After "<" operator, the file name should be exactly the same to the file
name in the file system, including the extension. For example, 
`myfile.txt` need be input for the file myfile.txt, while `world` should
be input for the file world. 

## How Multiple Lines / EOF Are Handled

Iterating over `sys.stdin` with a `for` loop automatically handles
files of any length — one line, ten lines, or ten thousand lines —
without any special-casing:

- Each iteration of the loop yields exactly one line, including its
  trailing `\n` newline character (except possibly the very last line
  of the file, if the file does not end with a newline).
- Because `print(line, end="")` suppresses the extra newline that
  `print()` normally adds, the line is printed exactly as it appeared
  in the input, preserving the original line breaks instead of
  doubling them.
- The loop terminates automatically when it reaches **EOF
  (End-Of-File)** — Python's file-iteration protocol raises
  `StopIteration` internally once there is no more data to read, and
  the `for` loop exits cleanly. No manual EOF check is needed.

## Input-File Assumptions and Error Handling

**Assumptions:**
- The input is a plain text file (UTF-8 or ASCII encoded).
- Lines are separated by standard newline characters.
- The file is provided via shell redirection (`<`), not as a
  command-line argument.

**Error handling:**
- `UnicodeDecodeError` — raised if `stdin` contains bytes that cannot
  be decoded as text (e.g., a binary file was redirected by mistake).
  The program prints a descriptive message to `stderr` and exits with
  status code `1`.
- `OSError` — a broader I/O error category (e.g., a pipe closed
  unexpectedly). The program prints the specific error message to
  `stderr` and exits with status code `1`.
- Using `sys.exit(1)` on failure follows the standard Unix convention
  that a non-zero exit code signals failure to the calling shell or
  script, while a normal, successful run exits with code `0`
  implicitly.

## How to Set the Folder/Current Directory

Before running the program, navigate your terminal to the directory
containing both `helloworld.py` and the input file (`myfile`):

```
cd path/to/your/project/folder
```

You can confirm you're in the right place with:

```
pwd        # macOS/Linux — prints current directory
cd         # Windows Command Prompt — prints current directory with no arguments
```

and:

```
ls         # macOS/Linux — lists files in the current directory
dir        # Windows
```

Both `helloworld.py` and `myfile` should appear in that listing.

## Command to Run the Program

From within the project directory:
```
For windows system:
python helloworld.py < myfile.txt

For linux system:
python3 helloworld.py < myfile.txt
```

(On some Windows setups, the interpreter may be invoked as `python`
instead of `python3` — check with `python3 --version` or
`python --version` first.)

## Sample Input and Output

**myfile (contents):**
```
Hello from David Mellor
```

**Command:**
```
Windows:
python helloworld.py < myfile.txt

Linux:
python3 helloworld.py < myfile.txt
```
**Output:**
```
Hello from David Mellor
```
**world (multi-line example)**

```
Hello from David Mellor
The world is wide, the sky is bright,
Mountains rise in morning light.
Rivers wander, oceans flow,
Seeds take root, and flowers grow.

Different paths, yet one shared ground,
Many voices, one world around.
We learn, we build, we dream, we see—
A changing world, endlessly.
```

**Command:**
```
Windows:
python helloworld.py < world

Linux:
python3 helloworld.py < world
```
Ran and passed on Git Bash, Python 3.13.3 .

The output matches the input exactly, line for line, confirming that
standard input redirection, line-by-line reading, and standard output
are all functioning correctly in the environment.