import math


def geometric_growth_rate(p: float, b: float, f: float):
    """
    p = probability of win
    b = profit per unit stake (e.g., 1 for even money)
    f = fraction of bankroll wagered

    Returns expected log growth rate per bet.
    """

    q = 1 - p

    # If f is invalid
    if f >= 1 or f <= -1:
        raise ValueError("f must be between -1 and 1")

    try:
        growth = (
            p * math.log(1 + f * b) +
            q * math.log(1 - f)
        )
    except ValueError:
        # log of negative number → ruin scenario
        return float("-inf")

    return growth

def growth_sweep(p: float, b: float, steps: int = 100):
    """
    Returns list of (f, growth_rate) pairs
    """

    results = []

    for i in range(1, steps):
        f = i / steps
        g = geometric_growth_rate(p, b, f)
        results.append((f, g))

    return results

import random


def simulate_growth(p: float, b: float, f: float, steps: int = 1000, initial: float = 1000):
    """
    Simulates geometric bankroll growth.
    """

    bankroll = initial
    path = [bankroll]

    for _ in range(steps):
        if random.random() < p:
            bankroll *= (1 + f * b)
        else:
            bankroll *= (1 - f)

        path.append(bankroll)

        if bankroll <= 0:
            break

    return path
