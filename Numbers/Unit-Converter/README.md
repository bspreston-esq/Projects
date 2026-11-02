# Unit Converter (temp, currency, volume, mass and more)

**Category:** Numbers

## Problem

Converts various units between one another. The user enters the type of unit being entered, the type of unit they want to convert to and then the value. The program will then make the conversion.

## Solution

Conversion tables express every linear unit as a factor of its category base unit, so any pair converts through a single division. Temperature is handled separately because its scales have offsets, normalising to Celsius first. Categories: temperature, length, mass, volume, speed, time and data.

## How to run

Requires Python 3.8+ and no third-party packages.

```bash
python3 main.py --category length --value 26.2 --from mi --to km
python3 main.py            # interactive prompts
python3 main.py --demo
```

## Example

```text
100 C = 212 F  (temperature)
32 F = 0 C  (temperature)
26.2 mi = 42.16 km  (length)
175 lb = 79.38 kg  (mass)
2 gal = 7.571 l  (volume)
60 mph = 96.56 km/h  (speed)
1.5 GB = 1536 MB  (data)
```
