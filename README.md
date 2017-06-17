# Hashwalk

Hashwalk is an exercise in futility. It attempts to mount a preimage attack on a hash function by applying local search. We define the objective function of a byte string by the hamming distance between its hash and the target value. Naturally, a cryptographic hash function's range should exhibit no patterns whatsoever. This property, also known as the avalanche effect, should mean that a local search heuristic performs no better than randomly generating byte strings and hashing them.
