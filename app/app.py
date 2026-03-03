import streamlit as st
import pandas as pd
import random
import numpy as np

# ---------- Kelly ----------
def kelly_fraction(probability: float, odds: float) -> float:
    b = odds - 1
    q = 1 - probability
    numerator = (b * probability) - q
    denominator = b
    if denominator == 0:
        return 0
    return max(numerator / denominator, 0)

# ---------- Expected Value ----------
def expected_value(probability: float, odds: float):
    return (probability * (odds - 1)) - (1 - probability)

# ---------- Simulate One Path ----------
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
def calculate_risk_of_ruin(bankroll, probability, odds, kelly_fraction, trials, simulations=500):
    ruined = 0

    for _ in range(simulations):
        final = simulate_path(bankroll, probability, odds, kelly_fraction, trials)[-1]
        if final <= bankroll * 0.1:
            ruined += 1

    return ruined / simulations

# ---------- UI ----------
st.set_page_config(page_title="Kelly Comparison Engine", layout="wide")

st.title("📊 Full Kelly vs Half Kelly Engine")

st.sidebar.header("Bet Parameters")

probability = st.sidebar.slider("Win Probability", 0.0, 1.0, 0.55)
odds = st.sidebar.number_input("Decimal Odds", min_value=1.01, value=2.0)
bankroll = st.sidebar.number_input("Starting Bankroll", min_value=1.0, value=1000.0)
trials = st.sidebar.slider("Bets per Simulation", 10, 500, 100)

# Calculations
full_kelly = kelly_fraction(probability, odds)
half_kelly = full_kelly / 2
ev = expected_value(probability, odds)

# Risk
risk_full = calculate_risk_of_ruin(bankroll, probability, odds, full_kelly, trials)
risk_half = calculate_risk_of_ruin(bankroll, probability, odds, half_kelly, trials)

# Metrics Display
st.subheader("Core Metrics")

col1, col2, col3 = st.columns(3)
col1.metric("Expected Value", f"{ev:.4f}")
col2.metric("Full Kelly Fraction", f"{full_kelly:.4f}")
col3.metric("Half Kelly Fraction", f"{half_kelly:.4f}")

st.subheader("Risk of Ruin")

col4, col5 = st.columns(2)
col4.metric("Full Kelly Ruin Risk", f"{risk_full*100:.2f}%")
col5.metric("Half Kelly Ruin Risk", f"{risk_half*100:.2f}%")

# Simulation Paths
st.subheader("Monte Carlo Comparison (Single Path Example)")

full_path = simulate_path(bankroll, probability, odds, full_kelly, trials)
half_path = simulate_path(bankroll, probability, odds, half_kelly, trials)

df = pd.DataFrame({
    "Full Kelly": full_path,
    "Half Kelly": half_path
})

st.line_chart(df)

# Long Run Comparison
st.subheader("Average Final Bankroll (500 Simulations)")

def average_terminal(bankroll, prob, odds, kelly, trials, simulations=500):
    finals = []
    for _ in range(simulations):
        finals.append(simulate_path(bankroll, prob, odds, kelly, trials)[-1])
    return np.mean(finals)

avg_full = average_terminal(bankroll, probability, odds, full_kelly, trials)
avg_half = average_terminal(bankroll, probability, odds, half_kelly, trials)

col6, col7 = st.columns(2)
col6.metric("Avg Final (Full Kelly)", f"{avg_full:.2f}")
col7.metric("Avg Final (Half Kelly)", f"{avg_half:.2f}")