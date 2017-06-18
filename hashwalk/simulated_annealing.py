import logging
import math
import random

import fitness
import mutation

class SimulatedAnnealing:

    def __init__(self, target, alpha=0.95, temp=25.0, epoch_len=1000000):
        self.logger = logging.getLogger("hashwalk.SimulatedAnnealing")
        self.target = target
        self.best_score = fitness.md5(target, target)
        self.best = target

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

    def is_accepted(self, score, curr_score):
        if score <= curr_score:
            self.logger.debug("  Accepting new sol: %d" % score)
            return True
        
        delta = curr_score - score
        p = math.e ** (float(delta) / self.temp)
        accept = random.random() < p

        if accept:
            self.logger.debug("  Accepting new sol: %d (delta=%02d for P=%.3f)" % (score, delta, p))
        else:
            self.logger.debug("  Rejecting sol: %d (delta=%02d for P=%.3f)" % (score, delta, p))

        return accept

    def run(self):
        curr_score = self.best_score
        curr = self.best

        while self.temp > 1.0:
            self.logger.debug("Epoch with temp=%.3f" % self.temp)
            for i in range(0, self.epoch_len):
                candidate = self.mutate(curr)
                score = fitness.md5(self.target, candidate)

                if self.is_accepted(score, curr_score):
                    curr_score = score
                    curr = candidate

                if score < self.best_score:
                    self.logger.info("Best solution found at %d, %s" % (score, candidate.hex()))
                    self.best_score = score
                    self.best = candidate

            self.temp *= self.alpha
