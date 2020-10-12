import numpy as np
from numpy.random import default_rng

import itertools

rng = default_rng()

sample = None
use_allocated_array = True


# Any more than 10^8 samples and it crashes because I don't have ~14 GiB of
# memory to spare for the calculation
# Cries in O(n) memory cost ;(
def estimate_pi(sample_size):
    sample = rng.random(sample_size) + rng.random(sample_size)*1j
    pi_over_4 = sample[np.abs(sample) < 1].size / sample.size
    pi = 4 * pi_over_4

    return pi


def get_inside_samples(sample_size):
    global sample  # Used to keep memory consumption slightly more constant

    sample = rng.random(sample_size) + rng.random(sample_size)*1j
    return sample[np.abs(sample) < 1].size


# Well actually this yields ~ e
def faster_estimate(sample_size):
    return 4 * np.count_nonzero(rng.random(sample_size) < np.sqrt(0.5)) / sample_size


# This method is much slower than the NumPy version, but it's memory cost is
# O(1) where n = samples
def iterative():
    inside = 0
    total = 0

    while True:
        total -= - 1  # Lol
        inside += abs(rng.random() + rng.random() * 1j) < 1
        yield 4 * inside / total


def combined_iterative(chunk_size):
    inside = 0
    total = 0

    while True:
        inside += get_inside_samples(chunk_size)
        total += chunk_size

        yield (4 * inside / total, total)


def test_iterative():
    exponent = 8
    generator = combined_iterative(10 ** exponent)

    for i in itertools.count():
        # last = 0
        # sample_size = 10 ** i

        # for v in range(sample_size - last):
        #     next(generator)

        pi, samples = next(generator)
        print('{0}*10^{2} samples: pi ~= {1}'.format(i, pi, exponent))

        # last = sample_size


if __name__ == '__main__':
    test_iterative()
