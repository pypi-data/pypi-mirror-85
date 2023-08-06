
from __future__ import print_function
from .terminalcolors import color, nocolor


def non_colourer(value, width):
    return str(value).ljust(width)


def true_false_colourer(value, width):
    strvalue = str(value).ljust(width)
    if not value:
        return color(5,2,2) + strvalue + nocolor()
    elif value is True:
        return color(2,5,2) + strvalue + nocolor()
    else:
        return color(5,5,5) + strvalue + nocolor()


def print_matrix(listoflists,
        header=None,
        separators=("  ", None),
        colourer=non_colourer):
    """
    Prints the given matrix, represented by list of lists, as a table.
    """
    columnlens = []
    rowlenmax = max(len(x) for x in listoflists)

    # calculate column widths based on matrix
    for i in range(rowlenmax):
        columnlens.append(max(
                len(str(x[i])) if i < len(x) else 0
                for x in listoflists))

    # check if headers need wider columns
    if header:
        for i, value in enumerate(header):
            if i < len(columnlens):
                columnlens[i] = max(columnlens[i], len(value))
            else:
                columnlens.append(len(value))

    # print matrix
    if header:
        parts = []
        for i, value in enumerate(header):
            parts.append(str(value).ljust(columnlens[i]))
        line = separators[0].join(parts)
        print(line)
        if separators[1]:
            print(separators[1] * ((len(line) - 1) // len(separators[1]) + 1))
    for row in listoflists:
        parts = []
        for i, slot in enumerate(row):
            parts.append(colourer(slot, columnlens[i]))
        print(separators[0].join(parts))
