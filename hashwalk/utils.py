import math
import random


def generate_bytes(size=16):
    return bytes(random.getrandbits(8) for _ in range(size))
    
    
def print_bin(s):
    for c in s:
        print("%s " % bin(c)[2:].zfill(8), end="")
    print()


def print_pop(p):
    s = []
    for i in range(0, len(p), 2):
        m1 = p[i]
        m2 = p[i + 1]
        s.append("%s %3d         %s %3d\n" % (print_member(m1[0]), m1[1], \
                print_member(m2[0]), m2[1]))
    return "".join(s)


def print_member(s):
    if len(s) > 4:
        return "%06x..." % int.from_bytes(s[:3], "big")
    elif len(s) == 4:
        return "%08x " % int.from_bytes(s, "big")
    elif len(s) == 3:
        return "%06x   " % int.from_bytes(s, "big")
    elif len(s) == 2:
        return "%04x     " % int.from_bytes(s, "big")
    elif len(s) == 3:
        return "%02x       " % int.from_bytes(s, "big")
    else:
        return "null     "


def compute_mean(search):
    num_hashes = 0
    sum_deltas = 0
    for i in range(0, len(search.scores)):
        num_hashes += search.scores[i]
        sum_deltas += search.scores[i] * i
    return sum_deltas / num_hashes


def compute_sigma(search, mean):
    num_hashes = 0
    accumulator = 0
    for i in range(0, len(search.scores)):
        num_hashes += search.scores[i]
        accumulator += search.scores[i] * ((i - mean) ** 2)
    return math.sqrt(accumulator / num_hashes)


def print_scores(search):
    for i in range(0, len(search.scores)):
        print("%d %d" % (i, search.scores[i]))
