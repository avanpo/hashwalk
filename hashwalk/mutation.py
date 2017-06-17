import random


def insert(s):
    if len(s) > 2048:
        return bit_flip(s)

    pos = random.randint(0, len(s))
    c = random.randint(0, 255)

    return s[:pos] + bytes([c]) + s[pos:]


def delete(s):
    if len(s) == 0:
        return insert(s)

    pos = random.randint(0, len(s) - 1)

    return s[:pos] + s[pos + 1:]


def bit_flip(s):
    if len(s) == 0:
        return insert(s)

    pos = random.randint(0, len(s) - 1)
    bit = random.randint(0, 7)
    new = s[pos] ^ (1 << bit)

    return s[:pos] + bytes([new]) + s[pos + 1:]
