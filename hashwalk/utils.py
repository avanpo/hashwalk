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
        return " %08x" % int.from_bytes(s, "big")
    elif len(s) == 3:
        return "   %06x" % int.from_bytes(s, "big")
    elif len(s) == 2:
        return "     %04x" % int.from_bytes(s, "big")
    elif len(s) == 3:
        return "       %02x" % int.from_bytes(s, "big")
    else:
        return "     null"
