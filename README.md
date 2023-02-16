# `snip_copy`

`snip_copy` creates copies of a file, snipping away portions of the original.

Our motivating use-case is to allow instructors to manage only a [rubric.py](test/ex_hw/rubric.py) copy of their assignment which contains student instructions, solutions to all problems and, grading criteria to be shared with TAs. Using `snip_copy` one can quickly create [solution.py](test/ex_hw/solution.py) and [student.py](test/ex_hw/student.py) versions of the same assignment from `rubric.py`.

## Installation

    pip install snip_copy

## Quick-start

Consider an example input file `input.txt`:

    this text will be left unmodified in all copies

    #! snip: a, b
    this text will be removed in copies a and b
    #! snip-end

    this text will (also) be left unmodified in all copies

Running `snip_copy` as:

```
    $ python3 -m snip_copy input.txt
```

generates two files, `a.txt` and `b.txt` where each has removed the snipped section.

## Jupyter Notebooks

You can add snip commands to jupyter notebook cells (code or markdown) to achieve similar behavior as well. For example, given input [rubric.ipynb](test/ex_hw/rubric.ipynb), running the following command:

```
    $ python3 -m snip_copy rubric.ipynb
```

generates [solution.ipynb](test/ex_hw/solution.ipynb) and [student.ipynb](test/ex_hw/student.ipynb).

## Notes:

- a copy is made for each item which appears in a comma separated list after any `snip` command in the entire document
- snip commands are removed in all copies created
- Each snip command line contains `#!`, which comments out the line, so it may live unobtrusively in python code. You can modify this string to produce similar behavior in another programming language:

```
    $ python3 -m snip_copy input.txt --cmd '// !'
```

- It can be cumbersome to type the full names of every output file with every `snip` command. Consider using `--split`:

```
    $ python3 -m snip_copy hw_rub.txt --split '_'
```

  which will "split" the input file name at the last occurrence of the given string. For example, if `hw_rub.txt` has the same contents as `input.txt` at the top, then the terminal command immediately above creates `hw_a.txt` and `hw_b.txt`.

- cells which do not include any snip commands are left unmodified in all copies
- if a cell's snip command would remove its entire contents, then we remove the cell entirely in the copy generated, rather than give a cell which is empty
- You can call `snip_copy` from within jupyter via a code containing: 
```
>>> #! snip: stud, sol
>>> !python3 -m snip_copy hw_rub.ipynb`
```
  which will make copies, removing this cell from each copy.