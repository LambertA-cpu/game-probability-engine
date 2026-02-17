EUROPEAN_NUMBERS = 37   # 0–36
AMERICAN_NUMBERS = 38   # 0, 00, 1–36

def roulette_probability(wheel_type: str, winning_outcomes: int):
    """
    wheel_type: 'european' or 'american'
    winning_outcomes: number of winning slots for the bet
    """

    if wheel_type.lower() == "european":
        total_slots = EUROPEAN_NUMBERS
    elif wheel_type.lower() == "american":
        total_slots = AMERICAN_NUMBERS
    else:
        raise ValueError("wheel_type must be 'european' or 'american'")

    return winning_outcomes / total_slots

ROULETTE_BETS = {
    "straight": {
        "winning_outcomes": 1,
        "payout": 35  # 35:1
    },
    "split": {
        "winning_outcomes": 2,
        "payout": 17  # 17:1
    },
    "street": {
        "winning_outcomes": 3,
        "payout": 11  # 11:1
    },
    "corner": {
        "winning_outcomes": 4,
        "payout": 8   # 8:1
    },
    "six_line": {
        "winning_outcomes": 6,
        "payout": 5   # 5:1
    },
    "column": {
        "winning_outcomes": 12,
        "payout": 2   # 2:1
    },
    "dozen": {
        "winning_outcomes": 12,
        "payout": 2   # 2:1
    },
    "red_black": {
        "winning_outcomes": 18,
        "payout": 1   # 1:1
    },
    "odd_even": {
        "winning_outcomes": 18,
        "payout": 1
    },
    "high_low": {
        "winning_outcomes": 18,
        "payout": 1
    }
}

def roulette_expected_value(wheel_type: str, bet_type: str, stake: float = 1.0):
    """
    Returns expected value per bet.
    stake: amount wagered
    """

    bet = ROULETTE_BETS.get(bet_type)

    if not bet:
        raise ValueError("Invalid bet type")

    probability = roulette_probability(
        wheel_type,
        bet["winning_outcomes"]
    )

    payout = bet["payout"]

    win_ev = probability * (payout * stake)
    lose_ev = (1 - probability) * (-stake)

    return win_ev + lose_ev

def roulette_house_edge(wheel_type: str, bet_type: str):
    """
    Returns house edge as a percentage.
    """

    ev = roulette_expected_value(wheel_type, bet_type, stake=1.0)

    return -ev * 100

import random


def roulette_simulation(wheel_type: str, bet_type: str, spins: int = 100000, stake: float = 1.0):
    """
    Simulates roulette spins and returns average profit per spin.
    """

    bet = ROULETTE_BETS.get(bet_type)

    if not bet:
        raise ValueError("Invalid bet type")

    if wheel_type.lower() == "european":
        total_slots = EUROPEAN_NUMBERS
    elif wheel_type.lower() == "american":
        total_slots = AMERICAN_NUMBERS
    else:
        raise ValueError("wheel_type must be 'european' or 'american'")

    winning_outcomes = bet["winning_outcomes"]
    payout = bet["payout"]

    total_profit = 0

    for _ in range(spins):
        spin_result = random.randint(1, total_slots)

        if spin_result <= winning_outcomes:
            total_profit += payout * stake
        else:
            total_profit -= stake

    return total_profit / spins

def simulate_bankroll(
    wheel_type: str,
    bet_type: str,
    initial_bankroll: float,
    stake: float,
    max_spins: int = 100000
):
    """
    Simulates a bankroll path until ruin or max_spins reached.
    Returns final bankroll and spins survived.
    """

    bet = ROULETTE_BETS.get(bet_type)

    if not bet:
        raise ValueError("Invalid bet type")

    if wheel_type.lower() == "european":
        total_slots = EUROPEAN_NUMBERS
    elif wheel_type.lower() == "american":
        total_slots = AMERICAN_NUMBERS
    else:
        raise ValueError("wheel_type must be 'european' or 'american'")

    winning_outcomes = bet["winning_outcomes"]
    payout = bet["payout"]

    bankroll = initial_bankroll
    spins = 0

    while bankroll > 0 and spins < max_spins:
        spins += 1

        spin_result = random.randint(1, total_slots)

        if spin_result <= winning_outcomes:
            bankroll += payout * stake
        else:
            bankroll -= stake

    return bankroll, spins

def estimate_ruin_probability(
    wheel_type: str,
    bet_type: str,
    initial_bankroll: float,
    stake: float,
    simulations: int = 1000,
    max_spins: int = 100000
):
    """
    Estimates probability of ruin via Monte Carlo.
    """

    ruin_count = 0

    for _ in range(simulations):
        final_bankroll, _ = simulate_bankroll(
            wheel_type,
            bet_type,
            initial_bankroll,
            stake,
            max_spins
        )

        if final_bankroll <= 0:
            ruin_count += 1

    return ruin_count / simulations

def estimate_time_to_ruin(
    wheel_type: str,
    bet_type: str,
    initial_bankroll: float,
    stake: float,
    simulations: int = 1000,
    max_spins: int = 100000
):
    """
    Returns average spins survived and list of survival times.
    """

    survival_times = []

    for _ in range(simulations):
        final_bankroll, spins = simulate_bankroll(
            wheel_type,
            bet_type,
            initial_bankroll,
            stake,
            max_spins
        )

        survival_times.append(spins)

    average_survival = sum(survival_times) / len(survival_times)

    return average_survival, survival_times

def compare_stakes(
    wheel_type: str,
    bet_type: str,
    initial_bankroll: float,
    stake_list: list,
    simulations: int = 500,
    max_spins: int = 100000
):
    """
    Compares ruin probability and average survival time for different stake sizes.
    """

    results = {}

    for stake in stake_list:
        ruin_prob = estimate_ruin_probability(
            wheel_type,
            bet_type,
            initial_bankroll,
            stake,
            simulations,
            max_spins
        )

        avg_time, _ = estimate_time_to_ruin(
            wheel_type,
            bet_type,
            initial_bankroll,
            stake,
            simulations,
            max_spins
        )

        results[stake] = {
            "ruin_probability": ruin_prob,
            "average_survival_spins": avg_time
        }

    return results
