def compare(a, b):
    ax, ay = a
    bx, by = b
    if ay < by:
        return -1
    elif ay > by:
        return 1
    elif ax < bx:
        return -1
    elif ax < bx:
        return 1
    else:
        return 0