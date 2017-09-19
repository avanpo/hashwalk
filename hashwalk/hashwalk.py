import logging
import time

import fitness
import local_search
import plot
import utils

logger = logging.getLogger("hashwalk")
logger.setLevel(logging.INFO)
consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.DEBUG)
logger.addHandler(consoleHandler)

target = b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"

start_time = time.time()

#search = local_search.Hiker(target, fitness.md5, steps=1000000)
#search.run()

#search = local_search.SimulatedAnnealing(target, fitness.md5, epoch_len=1000)
#search.set_uniq()
#search.run()

search = local_search.GeneticAlgorithm(target, fitness.md5, population_size=1000)
search.set_uniq()
search.run(generations=100)

elapsed_time = time.time() - start_time
logger.info("Completed run in %d seconds." % elapsed_time)

mean = utils.compute_mean(search)
sigma = utils.compute_sigma(search, mean)

print("Mean: %.3f, standard deviation: %.3f." % (mean, sigma))

plot.plot_scores(search)
