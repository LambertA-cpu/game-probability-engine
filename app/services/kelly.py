def kelly_fraction(p: float, b: float) -> float:
    """
    Returns optimal Kelly fraction.

    p = probability of win
    b = profit per unit stake (net odds)

    Kelly formula:
    f* = (p(b+1) - 1) / b
    """

    if b <= 0:
        raise ValueError("b must be positive")

    numerator = p * (b + 1) - 1
    f_star = numerator / b

    return f_star

def safe_kelly_fraction(p: float, b: float) -> float:
    """
    Returns Kelly fraction but never negative.
    If edge is negative → return 0 (do not bet).
    """

    f_star = kelly_fraction(p, b)

    if f_star <= 0:
        return 0.0

    return f_star

def fractional_kelly(p: float, b: float, fraction: float = 0.5) -> float:
    """
    fraction = 0.5 → half Kelly
    fraction = 0.25 → quarter Kelly
    """

    base = safe_kelly_fraction(p, b)
    return base * fraction

