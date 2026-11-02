#!/usr/bin/env python3
"""Track stock quotes for a list of symbols and show direction of movement."""
import argparse
import csv
import io
import time
import urllib.request

STOOQ_URL = "https://stooq.com/q/l/?s={symbols}&f=sd2t2ohlcv&h&e=csv"

def fetch_quotes(symbols):
    """Fetch latest quotes from Stooq; returns {symbol: price}."""
    query = ",".join(symbol.lower() + ("" if "." in symbol else ".us") for symbol in symbols)
    request = urllib.request.Request(STOOQ_URL.format(symbols=query),
                                     headers={"User-Agent": "quote-tracker/1.0"})
    with urllib.request.urlopen(request, timeout=15) as response:
        text = response.read().decode("utf-8", errors="replace")
    reader = csv.DictReader(io.StringIO(text))
    quotes = {}
    for row in reader:
        symbol = row.get("Symbol", "").upper().split(".")[0]
        close = row.get("Close")
        if symbol and close not in (None, "", "N/D"):
            quotes[symbol] = float(close)
    if not quotes:
        raise ValueError("no quotes returned (unknown symbol or market closed?)")
    return quotes

def direction(current, previous):
    if previous is None or current == previous:
        return "->", 0.0
    change = (current - previous) / previous * 100
    return ("^" if change > 0 else "v"), change

def render(quotes, previous):
    for symbol in sorted(quotes):
        arrow, change = direction(quotes[symbol], previous.get(symbol))
        print(f"{symbol:<6} {quotes[symbol]:>10,.2f}  {arrow} {change:+.2f}%")

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--symbols", default="AAPL,MSFT,GOOG")
    parser.add_argument("--interval", type=float, default=0, help="seconds between checks (0 = once)")
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()

    if args.demo:
        previous = {}
        for round_number, simulated in enumerate(
                ({"AAPL": 190.0, "MSFT": 410.5}, {"AAPL": 192.4, "MSFT": 407.1}), 1):
            print(f"check {round_number}:")
            render(simulated, previous)
            previous.update(simulated)
            time.sleep(0.2)
        return

    symbols = [s.strip().upper() for s in args.symbols.split(",") if s.strip()]
    previous = {}
    while True:
        try:
            quotes = fetch_quotes(symbols)
        except (OSError, ValueError) as exc:
            print(f"Error: {exc}")
            return
        render(quotes, previous)
        previous.update(quotes)
        if args.interval <= 0:
            break
        time.sleep(args.interval)

if __name__ == "__main__":
    main()
