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

search = local_search.SimulatedAnnealing(target, fitness.md5, epoch_len=100000)
search.run()

elapsed_time = time.time() - start_time
logger.info("Completed run in %d seconds." % elapsed_time)
