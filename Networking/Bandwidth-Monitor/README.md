# Bandwidth Monitor

**Category:** Networking

## Problem

A small utility program that tracks how much data you have uploaded and downloaded from the net during the course of your current online session. See if you can find out what periods of the day you use more and less and generate a report or graph that shows it.

## Solution

Reads byte counters from `/proc/net/dev` (Linux), samples twice over a configurable window, and divides the deltas by the measured elapsed time to get per-interface rates. Also reports cumulative session totals, excluding loopback.

## How to run

Requires Python 3.8+ and no third-party packages.

```bash
python3 main.py --interval 2 --count 5
python3 main.py --demo
```

## Example

```text
sample window: 0.51s
eth0         down   12.4 KB/s  up    1.2 KB/s
wlan0        down    0.0 B/s   up    0.0 B/s
session totals: down 18432.6 MB, up 421.8 MB
```
