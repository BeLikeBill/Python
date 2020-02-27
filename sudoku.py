# Rens Vester (12958042)
# Mudi Al-Fageh (12386863)

import sys
import math


def filetosudoku(filename):
    newsudoku = []
    with open(filename) as f:
        while True:
            lines = f.readline()
            if not lines:
                break
            newsudoku.append(list(int(i) for i in lines.strip().split(' ')))
        f.close()
    global size, a, b
    size = len(newsudoku)
    b = int(math.sqrt(size))  # columns
    a = int(size / b)  # rows
    return newsudoku


def printsudoku(sudoku):
    for row in sudoku:
        for cell in row:
            print(cell, end=' ')
        print('')


def uniquelist(mylist):  # from individual.py exercise
    # check for duplicates
    if any(mylist.count(x) > 1 & x != 0 for x in mylist):
        sys.exit("Error: duplicate!")
    return (list(filter(lambda i: i not in mylist, range(1, len(mylist)+1))))


def getsub(sudoku, i, j):
    newlist = []
    i = (i//b)*b
    j = (j//a)*a
    for x in range(i, b+i):
        for y in range(j, a+j):
            newlist.append(sudoku[x][y])
    return uniquelist(newlist)


def uniquevalues(sudoku, i, j):
    cols = []
    # to make list of column
    for x in range(size):
        cols.append(sudoku[x][j])
    subu = getsub(sudoku, i, j)
    vals = [val for val in uniquelist(cols)
            if (val in uniquelist(sudoku[i]) and val in subu)]
    return vals


def freecells(sudoku):
    cells = []
    for i in range(size):
        for j in range(size):
            if sudoku[i][j] == 0:
                cells.append((i, j))
    return cells


def solvable(sudoku):
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
                    sys.exit("sudoku wrong")

    return freeval & freepos


# brute force
def bruteforce(sudoku):
    while solvable(sudoku):
        for i in range(size):
            for j in range(size):
                if (sudoku[i][j] == 0):
                    val = uniquevalues(sudoku, i, j)
                    if len(val) == 1:
                        sudoku[i][j] = val.pop(0)
    return sudoku


# brute force try 2
def prunetree(sudoku):
    while solvable(sudoku):
        for i in range(size):
            for j in range(size):
                if sudoku[i][j] == 0:
                    val = uniquevalues(sudoku, i, j)
                    sudoku[i][j] = val.pop(0)
    return sudoku


# depth first search
def DFS(sudoku):
    cells = freecells(sudoku)
    stack = []
    solved = False
    if cells == []:
        solved = True
    while not(solved):
        c = cells.pop()
        if cells == []:
            solved = True
        uniq = uniquevalues(sudoku, c[0], c[1]).pop()
        sudoku[c[0]][c[1]] = uniq
        stack.append((c[0], c[1], uniq))
        if not(solvable):
            stack.pop()
    return sudoku


if (len(sys.argv) > 1):
    printsudoku(DFS(filetosudoku(sys.argv[1])))
    # sud = filetosudoku(sys.argv[1])
    # print(freecells(sud))
