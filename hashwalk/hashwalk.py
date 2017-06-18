import logging
import time
from hiker import Hiker
from simulated_annealing import SimulatedAnnealing

logger = logging.getLogger("hashwalk")
logger.setLevel(logging.INFO)
consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.DEBUG)
logger.addHandler(consoleHandler)

target = b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"

start_time = time.time()

local_search = Hiker(target, steps=10000000)
local_search.run()

elapsed_time = time.time() - start_time
logger.info("Completed run in %d seconds." % elapsed_time)
