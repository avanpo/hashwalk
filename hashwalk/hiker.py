import logging
import random

import fitness
import mutation

class Hiker:

    def __init__(self, target, steps=10000000):
        self.logger = logging.getLogger("hashwalk.Hiker")
        self.target = target
        self.best_score = fitness.md5(target, target)
        self.best = target
        self.steps = steps

    def mutate(self, s):
        op = random.randint(0, 5)
        if op == 0:
            return mutation.insert(s)
        elif op == 1:
            return mutation.delete(s)
        else:
            return mutation.bit_flip(s)

    def run(self):
        curr_score = self.best_score
        curr = self.best

        for i in range(0, self.steps):
            curr = self.mutate(curr)
            curr_score = fitness.md5(self.target, curr)

            if curr_score < self.best_score:
                self.logger.info("Best solution found at %d, %s" % (curr_score, curr.hex()))
                self.best_score = curr_score
                self.best = curr
