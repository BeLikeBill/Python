# Rens Vester (12958042)
# Mudi Al-Fageh (12386863)

import sys
import math
import copy

size = 9
a = 3
b = 3


def filetosudoku(filename):
    # turn file with numbers seperated by spaces and newlines into a sudoku
    newsudoku = []
    with open(filename) as f:
        while True:
            lines = f.readline()
            if not lines:
                break
            newsudoku.append(list(int(i) for i in lines.strip().split(' ')))
        f.close()
    global a, b, size
    size = len(newsudoku)
    b = int(math.sqrt(size))  # columns
    a = int(size / b)  # rows
    return newsudoku


def printsudoku(sudoku):
    for row in sudoku:
        for cell in row:
            print(cell, end=' ')
        print('')


def uniquelist(mylist):
    # check for duplicates and return free values
    if any(mylist.count(x) > 1 & x != 0 for x in mylist):
        sys.exit("Error: sudoku contains duplicates")
    return (list(filter(lambda i: i not in mylist, range(1, len(mylist)+1))))


def getsub(sudoku, i, j):
    # given transpose, returns free values of its subgrid
    sub = []
    i = (i//b)*b
    j = (j//a)*a
    for x in range(i, b+i):
        for y in range(j, a+j):
            sub.append(sudoku[x][y])
    return uniquelist(sub)


def uniquevalues(sudoku, i, j):
    # combines free values in sub, row and col to one list
    cols = []
    # to make list of column
    for x in range(size):
        cols.append(sudoku[x][j])
    subu = getsub(sudoku, i, j)
    vals = [val for val in uniquelist(cols)
            if (val in uniquelist(sudoku[i]) and val in subu)]
    return vals


def freecellssort(sudoku):
    # returns a list of free cells sorted by amount of free vals
    def Key(item):
        return len(item[2])

    cells = []
    for i in range(size):
        for j in range(size):
            if sudoku[i][j] == 0:
                cells.append((i, j, uniquevalues(sudoku, i, j)))
    return sorted(cells, key=Key, reverse=True)


def solvable(sudoku):
    # checks whether sudoku at current state is solvable
    freepos = False
    freeval = True
    for i in range(size):
        for j in range(size):
            if sudoku[i][j] == 0:
                if len(uniquevalues(sudoku, i, j)) < 1:
                    freeval = False
                freepos = True

    if not(freepos):
        for i in range(size):
            for j in range(size):
                if len(uniquevalues(sudoku, i, j)) > 0:
                    sys.exit("Sudoku wrong")

    return freeval & freepos


def solved(sudoku):
    # tests whether the sudoku is a solution
    for i in range(size):
        for j in range(size):
            if sudoku[i][j] == 0:
                return False
    return True


def DFS2(sudoku):
    # DepthFirstSearch alg that stores sudoku states on stack
    stack = [sudoku]
    while stack:
        sud = stack.pop()
        if solved(sud):
            return sud
        cells = freecellssort(sud)
        if cells:
            c = cells[-1]
            for val in c[2]:
                newsud = copy.deepcopy(sud)
                newsud[c[0]][c[1]] = val
                stack.append(newsud)
    return sud


def DFS3(sudoku):
    # DepthFirstSearch alg while taking into account amnt of free vals
    stack = []
    if not freecellssort(sudoku):  # check if sudoku valid
        solvable(sudoku)
    else:
        stack.append(freecellssort(sudoku).pop())

    while stack:
        if solved(sudoku):
            return sudoku  # solution was found
        opties = stack[-1]
        if opties[2]:
            val = opties[2].pop()
            sudoku[opties[0]][opties[1]] = val
            cells = freecellssort(sudoku)
            if cells:
                stack.append(cells[-1])
        else:
            sudoku[opties[0]][opties[1]] = 0
            stack.pop()
    return sudoku


if (len(sys.argv) > 1):
    printsudoku(DFS3(filetosudoku(sys.argv[1])))
