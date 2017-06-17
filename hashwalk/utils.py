def print_bin(s):
    for c in s:
        print("%s " % bin(c)[2:].zfill(8), end="")
    print()
