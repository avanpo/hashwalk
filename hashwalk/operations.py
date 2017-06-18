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


def two_point_crossover(s1, s2):
    if len(s1) < 2 or len(s2) < 2:
        return s1, s2

    pos11 = random.randint(0, len(s1) - 1)
    pos12 = random.randint(0, len(s1) - 1)
    pos21 = random.randint(0, len(s2) - 1)
    pos22 = random.randint(0, len(s2) - 1)

    if pos11 > pos12:
        pos11, pos12 = pos12, pos11
    if pos21 > pos22:
        pos21, pos22 = pos22, pos21

    c1 = s1[:pos11] + s2[pos21:pos22] + s1[pos12:]
    c2 = s2[:pos21] + s1[pos11:pos12] + s2[pos22:]

    return c1, c2
