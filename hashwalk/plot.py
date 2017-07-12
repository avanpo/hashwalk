from scipy.stats import binom
import logging
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


def plot_scores(scores):
    logger = logging.getLogger("hashwalk.plot")
    
    n = len(scores) - 1
    samples = sum(scores)

    logger.info("Generating svg for %d samples..." % samples)
    k = np.arange(0, n + 1)
    pmf = binom.pmf(k, n, 0.5)
    scaled_pmf = [x * samples for x in pmf]

    plt.xlabel("Hamming distance")
    plt.ylabel("Hashes found")
    plt.axis([0, n, 0, 0.08 * samples])

    #print(scores)
    #print(scaled_pmf)

    plt.bar(k, scores)
    plt.plot(k, scaled_pmf, "b-")

    plt.savefig("test.svg")
    logger.info("Done.")
