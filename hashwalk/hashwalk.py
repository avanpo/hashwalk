import logging
from simulated_annealing import SimulatedAnnealing

logger = logging.getLogger("hashwalk")
logger.setLevel(logging.INFO)
consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.DEBUG)
logger.addHandler(consoleHandler)

target = b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
start = b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"

local_search = SimulatedAnnealing(epoch_len=1000000)
local_search.run(target, start)
