import random
from collections import Counter
import numpy as np


def ticket_score(ticket, frequency):

    score = 0

    for n in ticket:
        score += frequency.get(n, 0)

    return score


def generate_random_ticket(min_num=1, max_num=45, pick=6):

    return sorted(random.sample(range(min_num, max_num + 1), pick))


def monte_carlo_optimizer(freq, iterations=5000):

    best_ticket = None
    best_score = -1

    tickets = []

    for _ in range(iterations):

        ticket = generate_random_ticket()

        score = ticket_score(ticket, freq)

        tickets.append((ticket, score))

        if score > best_score:

            best_score = score
            best_ticket = ticket

    tickets.sort(key=lambda x: x[1], reverse=True)

    top_tickets = tickets[:10]

    return best_ticket, top_tickets