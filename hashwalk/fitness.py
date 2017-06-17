from Crypto.Hash import MD5

NIBBLE_UP_BITS = [0, 1, 1, 2, 1, 2, 2, 3, 1, 2, 2, 3, 2, 3, 3, 4]


def md5(target, s):
    hasher = MD5.new()
    hasher.update(s)
    hash = hasher.digest()

    return hamming(hash, target)


def hamming(s1, s2):
    dist = 0
    for c1, c2 in zip(s1, s2):
        c = c1 ^ c2
        dist += NIBBLE_UP_BITS[c >> 4]
        dist += NIBBLE_UP_BITS[c & 0x0f]
    return dist
