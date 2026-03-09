from collections import Counter
import random

def number_frequency(df):

    counter = Counter()

    for nums in df["numbers"]:
        counter.update(nums)

    return counter


def generate_weighted_numbers(freq, pick=6):

    numbers = list(freq.keys())
    weights = list(freq.values())

    selected = random.choices(
        numbers,
        weights=weights,
        k=pick * 2
    )

    selected = list(set(selected))[:pick]

    return sorted(selected)