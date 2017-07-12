import logging
import math
import operator
import random
import sys

import operations
import utils


class LocalSearch:
    def __init__(self, target, fitness):
        self.target = target
        self._fitness = fitness
        self._uniq = False
        self.best_score = fitness(target, target)
        self.best = target

        self.scores = [0] * (128 + 1)

    def fitness(self, s):
        return self._fitness(self.target, s)

    def set_uniq(self):
        self._uniq = True
        self._hashset = set()

    def update(self, s, score):
        if not self._uniq:
            self.scores[score] += 1
        elif s not in self._hashset:
            self.scores[score] += 1
            self._hashset.add(s)

        if score < self.best_score:
            self.logger.info("Best solution found at %d, %s" % (score, utils.print_member(s)))
            self.best_score = score
            self.best = s

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
            curr_score = self.fitness(curr)

            self.update(curr, curr_score)


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
                score = self.fitness(candidate)

                self.update(candidate, score)

                if self.is_accepted(score, curr_score):
                    curr_score = score
                    curr = candidate
                    ops += 1

            self.logger.debug("Epoch ended with %.3f%% of ops accepted." % (100 * ops / float(self.epoch_len)))
            self.temp *= self.alpha


class GeneticAlgorithm(LocalSearch):
    def __init__(self, target, fitness, population_size=100):
        self.logger = logging.getLogger("hashwalk.local_search.GeneticAlgorithm")
        super().__init__(target, fitness)
        if population_size % 2 == 1:
            self.logger.error("The population size must be an even integer.")
            sys.exit(1)
        self.p_size = population_size
        self.generate_population()

    def generate_population(self):
        self.population = [None] * self.p_size
        for i in range(0, self.p_size):
            s = utils.generate_bytes()
            f = self.fitness(s)
            self.population[i] = (s, f)
            if f < self.best_score:
                self.best = s
                self.best_score = f

    def select_parents(self, p):
        """Select parents through tournament selection (s=2)."""
        random.shuffle(p)
        sp = [None] * self.p_size
        
        for i in range(0, self.p_size, 2):
            sp[i // 2] = p[i] if p[i][1] < p[i + 1][1] else p[i + 1]
        random.shuffle(p)
        for i in range(0, self.p_size, 2):
            sp[self.p_size // 2 + i // 2] = p[i] if p[i][1] < p[i + 1][1] else p[i + 1]

        return sp

    def generate_children(self, sp):
        """Generates children from selected parents."""
        c = [None] * self.p_size

        for i in range(0, self.p_size, 2):
            c1, c2 = operations.two_point_crossover(sp[i][0], sp[i + 1][0])
            c1 = self.mutate(c1) if random.randrange(2) == 0 else c1
            c2 = self.mutate(c2) if random.randrange(2) == 0 else c2
            c[i] = (c1, self.fitness(c1))
            c[i + 1] = (c2, self.fitness(c2))
            self.update(c[i][0], c[i][1])
            self.update(c[i + 1][0], c[i + 1][1])

        return c

    def select_generation(self, p, c):
        """Select new generation from parents and children."""
        p.sort(key=operator.itemgetter(1))
        c.sort(key=operator.itemgetter(1))
        g = [None] * self.p_size

        a, b = 0, 0
        for i in range(0, self.p_size):
            if p[a][1] < c[b][1]:
                g[i] = p[a]
                a += 1
            else:
                g[i] = c[b]
                b += 1

        self.logger.debug("Selected new generation with %d parents and %d children." % (a, b))
        return g

    def run(self, generations=100):
        for i in range(0, generations):
            #self.logger.debug("Population:")
            #self.logger.debug(utils.print_pop(self.population))
            sp = self.select_parents(self.population)
            #self.logger.debug("Selected parents:")
            #self.logger.debug(utils.print_pop(sp))
            c = self.generate_children(sp)
            #self.logger.debug("Generated children:")
            #self.logger.debug(utils.print_pop(c))

            self.population = self.select_generation(self.population, c)
            self.logger.debug("Fittest member with score %d, %s" % (self.population[0][1], utils.print_member(self.population[0][0])))
