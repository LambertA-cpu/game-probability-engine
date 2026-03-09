
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
import random
import numpy as np
import matplotlib.pyplot as plt

from lotto.scraper import scrape_lotto_results
from lotto.generator import number_frequency, generate_weighted_numbers
from lotto.optimizer import monte_carlo_optimizer

st.set_page_config(page_title="Advanced Kelly Engine", layout="wide")

# ---------- Kelly ----------
def kelly_fraction(probability: float, odds: float) -> float:
    b = odds - 1
    q = 1 - probability
    numerator = (b * probability) - q
    denominator = b
    if denominator == 0:
        return 0
    return max(numerator / denominator, 0)

def monte_carlo_simulation(
    bankroll,
    probability,
    odds,
    fraction,
    n_bets=100,
    simulations=1000
):
    results = []

    for _ in range(simulations):
        current_bankroll = bankroll

        for _ in range(n_bets):
            bet_size = current_bankroll * fraction

            if np.random.rand() < probability:
                current_bankroll += bet_size * (odds - 1)
            else:
                current_bankroll -= bet_size

            if current_bankroll <= 0:
                current_bankroll = 0
                break

        results.append(current_bankroll)

    return results

# ---------- Expected Value ----------
def expected_value(probability: float, odds: float):
    return (probability * (odds - 1)) - (1 - probability)

# ---------- Simulate Path ----------
def simulate_path(bankroll, probability, odds, kelly_fraction, trials):
    path = [bankroll]

    for _ in range(trials):
        stake = bankroll * kelly_fraction
        win = random.random() < probability

        if win:
            bankroll += stake * (odds - 1)
        else:
            bankroll -= stake

        if bankroll <= 0:
            path.append(0)
            return path

        path.append(bankroll)

    return path

# ---------- Risk of Ruin ----------
def calculate_risk_of_ruin(bankroll, probability, odds, kelly_fraction, trials, simulations=300):
    ruined = 0
    for _ in range(simulations):
        final = simulate_path(bankroll, probability, odds, kelly_fraction, trials)[-1]
        if final <= bankroll * 0.1:
            ruined += 1
    return ruined / simulations

# ---------- Max Drawdown ----------
def max_drawdown(path):
    peak = path[0]
    max_dd = 0

    for value in path:
        if value > peak:
            peak = value
        drawdown = (peak - value) / peak
        if drawdown > max_dd:
            max_dd = drawdown

    return max_dd

# ---------- Volatility ----------
def volatility(path):
    returns = np.diff(path) / path[:-1]
    return np.std(returns)

# ---------- Multi-Bet Simulation ----------
def simulate_multi_bet_round(
    bankroll,
    probabilities,
    odds_list,
    fractions,
    rounds
):
    path = [bankroll]

    for _ in range(rounds):
        total_change = 0

        for p, odds, f in zip(probabilities, odds_list, fractions):
            stake = bankroll * f

            if np.random.rand() < p:
                total_change += stake * (odds - 1)
            else:
                total_change -= stake

        bankroll += total_change

        if bankroll <= 0:
            path.append(0)
            return path

        path.append(bankroll)

    return path

# ---------- UI ----------
st.set_page_config(page_title="Advanced Kelly Engine", layout="wide")
st.title("📊 Full vs Half Kelly – Advanced Bankroll Analytics")

st.sidebar.header("Bet Parameters")

probability = st.sidebar.slider("Win Probability", 0.0, 1.0, 0.55)
odds = st.sidebar.number_input("Decimal Odds", min_value=1.01, value=2.0)
bankroll = st.sidebar.number_input("Starting Bankroll", min_value=1.0, value=1000.0)
trials = st.sidebar.slider("Bets per Simulation", 10, 500, 100)

# ---------- Multi-Bet ----------

st.sidebar.markdown("### Multi-Bet Setup")

p1 = st.sidebar.slider("Bet 1 Probability", 0.0, 1.0, 0.55)
o1 = st.sidebar.number_input("Bet 1 Odds", min_value=1.01, value=2.0)

p2 = st.sidebar.slider("Bet 2 Probability", 0.0, 1.0, 0.53)
o2 = st.sidebar.number_input("Bet 2 Odds", min_value=1.01, value=2.1)

p3 = st.sidebar.slider("Bet 3 Probability", 0.0, 1.0, 0.52)
o3 = st.sidebar.number_input("Bet 3 Odds", min_value=1.01, value=1.9)

f1 = kelly_fraction(p1, o1)
f2 = kelly_fraction(p2, o2)
f3 = kelly_fraction(p3, o3)

fractions = np.array([f1, f2, f3])
total_fraction = np.sum(fractions)

if total_fraction > 1:
    fractions = fractions / total_fraction
    scaled = True
else:
    scaled = False

multi_path = simulate_multi_bet_round(
    bankroll,
    [p1, p2, p3],
    [o1, o2, o3],
    fractions,
    trials
)
if scaled:
    st.warning("Fractions scaled to avoid over-leverage.")

st.subheader("Multi-Bet Portfolio")

st.metric("Total Capital Allocated", f"{total_fraction:.2f}")

df_multi = pd.DataFrame({
    "Multi-Bet Kelly": multi_path
})

st.line_chart(df_multi)

# Core Metrics
full_kelly = kelly_fraction(probability, odds)
half_kelly = full_kelly / 2
ev = expected_value(probability, odds)

# Simulation Paths
full_path = simulate_path(bankroll, probability, odds, full_kelly, trials)
half_path = simulate_path(bankroll, probability, odds, half_kelly, trials)

# Risk
risk_full = calculate_risk_of_ruin(bankroll, probability, odds, full_kelly, trials)
risk_half = calculate_risk_of_ruin(bankroll, probability, odds, half_kelly, trials)

# Drawdown
dd_full = max_drawdown(full_path)
dd_half = max_drawdown(half_path)

# Volatility
vol_full = volatility(full_path)
vol_half = volatility(half_path)

# ---------- Sharpe Ratio ----------
def sharpe_ratio(path):
    returns = np.diff(path) / path[:-1]
    if np.std(returns) == 0:
        return 0
    return np.mean(returns) / np.std(returns)

sharpe_full = sharpe_ratio(full_path)
sharpe_half = sharpe_ratio(half_path)

st.subheader("Risk-Adjusted Performance")

col10, col11 = st.columns(2)
col10.metric("Full Kelly Sharpe", f"{sharpe_full:.4f}")
col11.metric("Half Kelly Sharpe", f"{sharpe_half:.4f}")

# ---------- Display ----------
st.subheader("Core Metrics")

col1, col2, col3 = st.columns(3)
col1.metric("Expected Value", f"{ev:.4f}")
col2.metric("Full Kelly Fraction", f"{full_kelly:.4f}")
col3.metric("Half Kelly Fraction", f"{half_kelly:.4f}")

st.subheader("Risk Metrics")

col4, col5 = st.columns(2)
col4.metric("Full Kelly Ruin Risk", f"{risk_full*100:.2f}%")
col5.metric("Half Kelly Ruin Risk", f"{risk_half*100:.2f}%")

st.subheader("Drawdown & Volatility")

col6, col7 = st.columns(2)
col6.metric("Full Kelly Max Drawdown", f"{dd_full*100:.2f}%")
col7.metric("Half Kelly Max Drawdown", f"{dd_half*100:.2f}%")

col8, col9 = st.columns(2)
col8.metric("Full Kelly Volatility", f"{vol_full:.4f}")
col9.metric("Half Kelly Volatility", f"{vol_half:.4f}")

st.subheader("Growth Comparison")

df = pd.DataFrame({
    "Full Kelly": full_path,
    "Half Kelly": half_path
})

st.line_chart(df)

# ---------- next phase ----------
if st.button("Run Monte Carlo Simulation"):
    
    full_results = monte_carlo_simulation(
        bankroll,
        probability,
        odds,
        full_kelly
    )

    half_results = monte_carlo_simulation(
        bankroll,
        probability,
        odds,
        half_kelly
    )

    st.subheader("Simulation Results")

    fig, ax = plt.subplots()

    ax.hist(full_results, bins=50, alpha=0.5, label="Full Kelly")
    ax.hist(half_results, bins=50, alpha=0.5, label="Half Kelly")

    ax.set_xlabel("Final Bankroll")
    ax.set_ylabel("Frequency")
    ax.legend()

    st.pyplot(fig)

    st.write("Full Kelly Average Final Bankroll:", np.mean(full_results))
    st.write("Half Kelly Average Final Bankroll:", np.mean(half_results))

    st.write("Full Kelly Ruin Probability:",
             np.mean(np.array(full_results) == 0))

    st.write("Half Kelly Ruin Probability:",
             np.mean(np.array(half_results) == 0))

# ---------- Lottary generator ----------

st.markdown("---")
st.header("Kenya Lottery Number Generator")

if st.button("Load Latest Lotto Results"):

    df = scrape_lotto_results()

    st.write("Recent Draws")
    st.dataframe(df.head())

    freq = number_frequency(df)

    ticket = generate_weighted_numbers(freq)

    st.subheader("Generated Lotto Numbers")
    st.success(ticket)

    #----------Monte Carlo optimiser----------

    st.markdown("---")
st.header("Monte Carlo Lotto Optimizer")

iterations = st.slider(
    "Number of Simulation Tickets",
    1000,
    20000,
    5000
)

if st.button("Run Lotto Optimization"):

    df = scrape_lotto_results()

    freq = number_frequency(df)

    best_ticket, top_tickets = monte_carlo_optimizer(
        freq,
        iterations
    )

    st.subheader("Best Ticket Found")

    st.success(best_ticket)

    st.subheader("Top 10 Tickets")

    for t in top_tickets:
        st.write(t)