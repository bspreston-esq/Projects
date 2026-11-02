# Get Atomic Time from Internet Clock

**Category:** Web

## Problem

This program will get the true atomic time from an atomic time clock on the Internet. Use any one of the atomic clocks returned by a simple Google search.

## Solution

Implements the NTP client protocol directly over UDP (48-byte request, transmit timestamp decoded from the reply and converted from the 1900 epoch), with an HTTP JSON fallback via worldtimeapi.org. Prints the network time, system time and the offset between them. The demo decodes a synthetic packet offline.

## How to run

Requires Python 3.8+ and no third-party packages.

```bash
python3 main.py
python3 main.py --http
python3 main.py --demo
```

## Example

```text
synthetic NTP packet -> 2026-11-02T12:34:56.500000+00:00
matches expected: True
system clock (UTC): 2026-11-02T18:58:12+00:00
```
