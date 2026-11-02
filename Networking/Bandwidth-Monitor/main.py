#!/usr/bin/env python3
"""Track per-interface upload and download totals and rates from /proc/net/dev."""
import argparse
import time

INTERFACE_FILE = "/proc/net/dev"

def read_totals(path=INTERFACE_FILE):
    """Return {interface: (rx_bytes, tx_bytes)}."""
    totals = {}
    with open(path) as fh:
        lines = fh.readlines()[2:]
    for line in lines:
        name, _, data = line.partition(":")
        fields = data.split()
        if len(fields) >= 8:
            totals[name.strip()] = (int(fields[0]), int(fields[8]))
    return totals

def humanize(bytes_per_second: float) -> str:
    units = ["B/s", "KB/s", "MB/s", "GB/s"]
    value = bytes_per_second
    for unit in units:
        if value < 1024 or unit == units[-1]:
            return f"{value:.1f} {unit}"
        value /= 1024
    return f"{value:.1f} GB/s"

def sample(interval: float, path=INTERFACE_FILE):
    """Return (elapsed, {iface: (rx_rate, tx_rate)}, session_totals)."""
    first = read_totals(path)
    start = time.monotonic()
    time.sleep(interval)
    elapsed = time.monotonic() - start
    second = read_totals(path)
    rates = {}
    for name in second:
        if name in first and name != "lo":
            rx = (second[name][0] - first[name][0]) / elapsed
            tx = (second[name][1] - first[name][1]) / elapsed
            rates[name] = (rx, tx)
    totals = {name: (values[0], values[1]) for name, values in second.items() if name != "lo"}
    return elapsed, rates, totals

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--interval", type=float, default=1.0)
    parser.add_argument("--count", type=int, default=5)
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()

    if args.demo:
        elapsed, rates, totals = sample(0.5)
        print(f"sample window: {elapsed:.2f}s")
        for name, (rx, tx) in sorted(rates.items()):
            print(f"{name:<12} down {humanize(rx):>10}  up {humanize(tx):>10}")
        total_rx = sum(value[0] for value in totals.values())
        total_tx = sum(value[1] for value in totals.values())
        print(f"session totals: down {total_rx/1024/1024:.1f} MB, up {total_tx/1024/1024:.1f} MB")
        return

    for _ in range(args.count):
        elapsed, rates, totals = sample(args.interval)
        print(time.strftime("%H:%M:%S"), f"({elapsed:.2f}s)")
        for name, (rx, tx) in sorted(rates.items()):
            print(f"  {name:<12} down {humanize(rx):>10}  up {humanize(tx):>10}")

if __name__ == "__main__":
    main()
