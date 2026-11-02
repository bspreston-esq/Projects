# Country from IP Lookup

**Category:** Networking

## Problem

Enter an IP address and find the country that IP is registered in. Optional: Find the IP automatically.

## Solution

Calls the free `ip-api.com` JSON endpoint with a urllib request and prints country, region, city and ISP. Private, loopback and documentation addresses short-circuit to "Private network" without a network call. The demo runs a local HTTP stub so the parsing path is testable offline.

## How to run

Requires Python 3.8+ and no third-party packages.

```bash
python3 main.py 8.8.8.8
python3 main.py 1.1.1.1 --json
python3 main.py --demo
```

## Example

```text
93.184.216.34: Amsterdam, North Holland, Netherlands (NL) via Example ISP
192.168.1.10: Private network
```
