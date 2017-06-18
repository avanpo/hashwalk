import logging
import math
import random

import fitness
import operations

class LocalSearch:
    def __init__(self, target, fitness):
        self.target = target
        self.fitness = fitness
        self.best_score = fitness(target, target)
        self.best = target

    def mutate(self, s):
        op = random.randint(0, 5)
        if op == 0:
            return operations.insert(s)
        elif op == 1:
            return operations.delete(s)
        else:
            return operations.bit_flip(s)

class Hiker(LocalSearch):
    def __init__(self, target, fitness, steps=10000000):
        self.logger = logging.getLogger("hashwalk.local_search.Hiker")
        super().__init__(target, fitness)
        self.steps = steps

    def run(self):
        curr_score = self.best_score
        curr = self.best

        for i in range(0, self.steps):
            curr = self.mutate(curr)
            curr_score = self.fitness(self.target, curr)

            if curr_score < self.best_score:
                self.logger.info("Best solution found at %d, %s" % (curr_score, curr.hex()))
                self.best_score = curr_score
                self.best = curr

class SimulatedAnnealing(LocalSearch):
    def __init__(self, target, fitness, alpha=0.95, temp=25.0, epoch_len=1000000):
        self.logger = logging.getLogger("hashwalk.local_search.SimulatedAnnealing")
        super().__init__(target, fitness)

        self.alpha = alpha
        self.temp = temp
        self.epoch_len = epoch_len

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
            ops = 0
            for i in range(0, self.epoch_len):
                candidate = self.mutate(curr)
                score = self.fitness(self.target, candidate)

                if self.is_accepted(score, curr_score):
                    curr_score = score
                    curr = candidate
                    ops += 1

                if score < self.best_score:
                    self.logger.info("Best solution found at %d, %s" % (score, candidate.hex()))
                    self.best_score = score
                    self.best = candidate

            self.logger.info("Epoch ended with %.3f%% of ops accepted." % (100 * ops / float(self.epoch_len)))
            self.temp *= self.alpha
