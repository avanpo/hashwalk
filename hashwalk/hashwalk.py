import logging
import time

import fitness
import local_search

logger = logging.getLogger("hashwalk")
logger.setLevel(logging.INFO)
consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.DEBUG)
logger.addHandler(consoleHandler)

target = b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"

start_time = time.time()

search = local_search.GeneticAlgorithm(target, fitness.md5, population_size=500000)
search.run(generations=100)

elapsed_time = time.time() - start_time
logger.info("Completed run in %d seconds." % elapsed_time)
