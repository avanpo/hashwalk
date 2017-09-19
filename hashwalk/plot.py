from scipy.stats import binom
import logging
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


def plot_scores(search):
    logger = logging.getLogger("hashwalk.plot")
    
    n = len(search.scores) - 1
    samples = sum(search.scores)

    logger.info("Generating svg for %d samples..." % samples)
    k = np.arange(0, n + 1)
    pmf = binom.pmf(k, n, 0.5)
    scaled_pmf = [x * samples for x in pmf]

    plt.xlabel("Hamming distance", family='monospace')
    plt.ylabel("Hashes found", family='monospace')
    plt.axis([0, n, 0, 0.08 * samples])

    #print(search.scores)
    #print(scaled_pmf)

    plt.bar(k, search.scores, zorder=1)
    plt.plot(k, scaled_pmf, '-', antialiased=True, color='#ff3300', linewidth=1, zorder=2)

    plt.suptitle(search.name + " search results", family='monospace')

    plt.savefig("test.svg")
    logger.info("Done.")
