# Rens Vester
# 12958042

import collections


def opgave1(mylist):
    length = len(mylist)+1
    return len(list(filter(lambda i: i not in mylist, range(1, length)))) == 0


def opgave2(mylist):
    length = len(mylist)+1
    return (filter(lambda i: i not in mylist, range(1, length)))


def opgave3a(filename):
    newlist = []
    with open(filename) as f:
        while True:
            lines = f.readline()
            if not lines:
                break
            newlist.append(list(int(i) for i in lines.strip().split(' ')))
        f.close()
    return newlist


def opgave3b(mylist):
    while mylist != []:
        line = (mylist.pop(0))
        while line != []:
            print(line.pop(0), end=' ')
        print('')


def opgave3(filename):
    opgave3b(opgave3a(filename))


def sum_nested_it(mylist):
    done = False

    while not done:
        newlist = []
        done = True
        for member in mylist:
            if isinstance(member, collections.Iterable):
                newlist += member
                done = False
            else:
                newlist.append(member)
        mylist = newlist
    return sum(mylist)
