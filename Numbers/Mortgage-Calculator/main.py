#!/usr/bin/env python3
"""Fixed-term mortgage calculator with selectable compounding intervals."""
import argparse
import math

INTERVALS = {"monthly": 12, "weekly": 52, "daily": 365, "continuous": None}

def periodic_rate(annual_rate_percent: float, interval: str) -> float:
    """Effective rate for one payment period under the chosen compounding."""
    r = annual_rate_percent / 100.0
    if interval == "continuous":
        # Monthly payments while the balance compounds continuously.
        return math.exp(r / 12) - 1
    return r / INTERVALS[interval]

def payment(principal: float, annual_rate_percent: float, years: float, interval: str) -> float:
    """Level payment for each period."""
    if principal <= 0 or years <= 0:
        raise ValueError("principal and term must be positive")
    i = periodic_rate(annual_rate_percent, interval)
    n = int(round(years * (INTERVALS[interval] or 12)))
    if i == 0:
        return principal / n
    return principal * i / (1 - (1 + i) ** -n)

def payoff_periods(principal: float, annual_rate_percent: float, years: float,
                   interval: str, extra_per_period: float = 0.0) -> int:
    """Number of periods until the balance is cleared, including extra payments."""
    i = periodic_rate(annual_rate_percent, interval)
    n = int(round(years * (INTERVALS[interval] or 12)))
    base = payment(principal, annual_rate_percent, years, interval) + extra_per_period
    balance, periods = principal, 0
    while balance > 1e-9 and periods < 100000:
        interest = balance * i
        principal_paid = base - interest
        if principal_paid <= 0:
            return 10**6  # never pays off
        balance -= principal_paid
        periods += 1
    return periods

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--principal", type=float)
    parser.add_argument("--rate", type=float, help="annual interest rate, percent")
    parser.add_argument("--years", type=float)
    parser.add_argument("--interval", choices=sorted(INTERVALS), default="monthly")
    parser.add_argument("--extra", type=float, default=0.0, help="extra payment each period")
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()

    if args.demo:
        p, r, y = 300000.0, 6.5, 30.0
        print(f"Loan ${p:,.0f} at {r}% over {y:g} years")
        for interval in ("monthly", "weekly", "daily", "continuous"):
            pay = payment(p, r, y, interval)
            n = int(round(y * (INTERVALS[interval] or 12)))
            print(f"  {interval:<10} payment {pay:>10,.2f} x {n:<5} = {pay*n:>12,.2f} total")
        months = payoff_periods(p, r, y, "monthly", 250)
        print(f"With $250 extra monthly: paid off in {months} months ({months/12:.1f} years)")
        return

    principal = args.principal if args.principal is not None else float(input("Loan principal: "))
    rate = args.rate if args.rate is not None else float(input("Annual interest rate (%): "))
    years = args.years if args.years is not None else float(input("Term in years: "))
    try:
        pay = payment(principal, rate, years, args.interval)
        n = int(round(years * (INTERVALS[args.interval] or 12)))
        print(f"Payment: {pay:,.2f} per {args.interval.rstrip('ly')} period ({n} periods)")
        print(f"Total paid: {pay*n:,.2f}")
        print(f"Total interest: {pay*n - principal:,.2f}")
        if args.extra:
            periods = payoff_periods(principal, rate, years, args.interval, args.extra)
            print(f"With {args.extra:,.2f} extra: paid off in {periods} periods")
    except ValueError as exc:
        print(f"Error: {exc}")

if __name__ == "__main__":
    main()
