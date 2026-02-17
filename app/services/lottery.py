import math
from scipy.stats import norm

def combinations(n: int, k: int) -> int:
    return math.comb(n, k)

def theoretical_probability(range_min: int, range_max: int, pick: int) -> float:
    total_numbers = range_max - range_min + 1
    if pick > total_numbers:
        raise ValueError("Pick count cannot exceed the range size")
    
    total_combinations = combinations(total_numbers, pick)
    return 1 / total_combinations

# def expected_value(probability: float, payout: float, cost: float)-> float:
#     return (probability * payout) - cost

from collections import Counter

def historical_frequency(df, range_min: int, range_max: int):
    counter = Counter()

    for draw in df["numbers"]:
        for number in draw:
            if range_min <= number <= range_max:
                counter[number] += 1

    return dict(counter)

def analyze_lottery(range_min: int, range_max: int, pick: int, df):
    theory_prob = theoretical_probability(range_min, range_max, pick)
    freq = historical_frequency(df, range_min, range_max)

    total_draws = len(df)

    stats = statistical_analysis(freq, total_draws, pick, range_min, range_max)

    return {
        "theoretical_probability": theory_prob,
        "total_draws": total_draws,
        "statistical_analysis": stats
    }



def calculate_deviation(freq_dict, expected_frequency):
    deviation = {}

    for number, observed in freq_dict.items():
        deviation[number] = observed - expected_frequency

    return deviation

def statistical_analysis(freq_dict, total_draws, pick, range_min, range_max):
    results = {}

    range_size = range_max - range_min + 1
    p = pick / range_size
    expected = total_draws * p
    std_dev = math.sqrt(total_draws * p * (1 - p))

    for number, observed in freq_dict.items():
        if std_dev == 0:
            z_score = 0
            p_value = 1
        else:
            z_score = (observed - expected) / std_dev
            p_value = 2 * (1 - norm.cdf(abs(z_score)))

        ci_lower = expected - 1.96 * std_dev
        ci_upper = expected + 1.96 * std_dev

        results[number] = {
            "observed": observed,
            "expected": expected,
            "z_score": z_score,
            "p_value": p_value,
            "confidence_interval_95": (ci_lower, ci_upper),
            "significant": p_value < 0.05
        }

    return results
 
def expected_value(prize_structure: dict, ticket_cost: float):
    """
    prize_structure format:
    {
        "jackpot": {"probability": 1e-6, "payout": 1000000},
        "match_5": {"probability": 1e-4, "payout": 5000},
        ...
    }
    """

    ev = 0

    for tier in prize_structure.values():
        ev += tier["probability"] * tier["payout"]

    return ev - ticket_cost
