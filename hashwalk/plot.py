from scipy.stats import binom
import logging
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


def plot_scores(n, scores):
    logger = logging.getLogger("hashwalk.plot")
    
    samples = sum(scores)
    logger.info("Generating svg for %d samples..." % samples)
    k = np.arange(0, n + 1)
    pmf = binom.pmf(k, n, 0.5)
    scaled_pmf = [x * samples for x in pmf]

    plt.xlabel("Hamming distance")
    plt.ylabel("Hashes found")
    plt.axis([0, 128, 0, 0.1 * samples])

    print(scores)
    print(scaled_pmf)

    plt.bar(k[:-1], scores)
    plt.plot(k, scaled_pmf, "b-")

    plt.savefig("test.svg")
    logger.info("Done.")
