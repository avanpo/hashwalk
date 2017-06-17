import logging
import math
import random

import fitness
import mutation

class SimulatedAnnealing:

    def __init__(self, alpha=0.95, temp=25.0, epoch_len=1000000):
        self.logger = logging.getLogger("hashwalk.SimulatedAnnealing")
        self.alpha = alpha
        self.temp = temp
        self.epoch_len = epoch_len

    def mutate(self, s):
        op = random.randint(0, 5)
        if op == 0:
            return mutation.insert(s)
        elif op == 1:
            return mutation.delete(s)
        else:
            return mutation.bit_flip(s)

    def is_accepted(self, score, curr):
        if score <= curr:
            self.logger.debug("  Accepting new sol: %d" % score)
            return True
        
        delta = curr - score
        p = math.e ** (float(delta) / self.temp)
        accept = random.random() < p

        if accept:
            self.logger.debug("  Accepting new sol: %d (delta=%02d for P=%.3f)" % (score, delta, p))
        else:
            self.logger.debug("  Rejecting sol: %d (delta=%02d for P=%.3f)" % (score, delta, p))

        return accept

    def run(self, target, s):
        best = fitness.md5(target, s)
        best_s = s

        curr = best

        while self.temp > 1.0:
            self.logger.debug("Epoch with temp=%.3f" % self.temp)
            for i in range(0, self.epoch_len):
                candidate = self.mutate(s)
                score = fitness.md5(target, candidate)

                if self.is_accepted(score, curr):
                    s = candidate
                    curr = score

                if score < best:
                    self.logger.info("Best solution found at %d, %s" % (score, s.hex()))
                    best = score

            self.temp *= self.alpha
