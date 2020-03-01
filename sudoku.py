# Rens Vester (12958042)
# Mudi Al-Fageh (12386863)

import sys
import math
import copy

# Initialize global variables to default sudoku size.
size = 9
a = 3
b = 3


def filetosudoku(filename):
    # Turns file with numbers seperated by spaces and newlines into a sudoku.
    with open(filename) as f:
        sudoku = [[int(x) for x in line.split()] for line in f]

    global a, b, size
    size = len(sudoku)
    b = int(math.sqrt(size))  # Columns
    a = int(size / b)  # Rows
    return sudoku


def printsudoku(sudoku):
    # Prints the sudoku to the screen.
    [print(*x) for x in sudoku]
    # for x in sudoku:
    #    print(*x)


def unique(mylist):
    # Check for duplicates and return free values for given list.
    if any(mylist.count(x) > 1 & x != 0 for x in mylist):
        sys.exit("Error: duplicate in row, column or subgrid")
    return (list(filter(lambda i: i not in mylist, range(1, len(mylist) + 1))))


def getsub(sudoku, i, j):
    # Given transpose, returns free values of its subgrid.
    i = (i//b)*b
    j = (j // a) * a
    return [sudoku[x][y] for x in range(i, b+i) for y in range(j, a+j)]


def uniquevalues(sudoku, i, j):
    # Combines free values in sub, row and col to one list, asssigning them to
    # x y and z assures they are all checked for duplicates.
    x = unique([sudoku[s][j] for s in range(size)])
    y = unique(sudoku[i])
    z = unique(getsub(sudoku, i, j))
    return [u for u in x if u in y and u in z]


def freecellssort(sudoku):
    # Returns a list of free cells sorted by amount of free vals.
    def Key(item):
        return len(item[2])

    cs = [(i, j, uniquevalues(sudoku, i, j)) for i in range(size)
          for j in range(size) if sudoku[i][j] == 0]

    # Sort by least free values first, makes finding solution generally faster.
    return sorted(cs, key=Key, reverse=True)


def solvable(sudoku):
    # Checks whether sudoku at current state is solvable and valid.
    return any(not uniquevalues(sudoku, i, j)
               for i in range(size)
               for j in range(size))


def filled(sudoku):
    # Tests whether the sudoku is filled.
    return all(sudoku[i][j] != 0 for i in range(size) for j in range(size))


def CopyDFS(sudoku):
    # DepthFirstSearch alg that stores sudoku states on stack
    stack = [sudoku]  # Start with first sudoku.
    while stack:
        sud = stack.pop()
        if filled(sud):
            return sud
        cells = freecellssort(sud)
        if cells:
            c = cells[-1]
            for val in c[2]:
                newsud = copy.deepcopy(sud)
                newsud[c[0]][c[1]] = val
                stack.append(newsud)
    return sud


def DFS(sudoku):
    # DepthFirstSearch alg whilst taking into account amnt of free vals.

    if filled(sudoku):    # Check if sudoku not already full.
        solvable(sudoku)  # Tests for duplicates and if solvable.
        return sudoku  # If valid solution, no search to be done.

    stack = [freecellssort(sudoku)[-1]]  # Initialize the stack for use.

    while stack:
        if filled(sudoku):
            return sudoku   # Solution is found, to standard output.
        opts = stack[-1]    # First options to be tested.
        if opts[2]:
            val = opts[2].pop()  # Pop option off, so it won't be tested again.
            sudoku[opts[0]][opts[1]] = val
            cells = freecellssort(sudoku)
            if cells:
                stack.append(cells[-1])
        else:
            sudoku[opts[0]][opts[1]] = 0
            stack.pop()

    return sudoku


if __name__ == "__main__":
    if (len(sys.argv) > 1):
        printsudoku(DFS(filetosudoku(sys.argv[1])))
