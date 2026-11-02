# Fetch Current Weather

**Category:** Web

## Problem

Get the current weather for a given zip/postal code. Optional: Try locating the user automatically.

## Solution

Uses Open-Meteo (no API key): geocodes a city name through their geocoding endpoint, then requests current temperature, apparent temperature, humidity, wind and WMO weather code, translating the code to a human description. Coordinates can be passed directly. The demo runs against a local JSON stub.

## How to run

Requires Python 3.8+ and no third-party packages.

```bash
python3 main.py --city Amsterdam
python3 main.py --latlon 40.7128 -74.0060
python3 main.py --demo
```

## Example

```text
Amsterdam, Netherlands: 11.4 C (feels like 9.8 C), 82% humidity, 14.2 km/h wind, slight rain
```
