#!/usr/bin/env python3
"""Convert values between temperature, length, mass, volume, speed and time units."""
import argparse

# Each table maps unit -> factor to the category's base unit.
LINEAR_UNITS = {
    "length": {"m": 1.0, "km": 1000.0, "cm": 0.01, "mm": 0.001,
               "in": 0.0254, "ft": 0.3048, "yd": 0.9144, "mi": 1609.344},
    "mass": {"kg": 1.0, "g": 0.001, "mg": 1e-6, "lb": 0.45359237,
             "oz": 0.028349523125, "t": 1000.0, "st": 6.35029318},
    "volume": {"l": 1.0, "ml": 0.001, "m3": 1000.0, "gal": 3.785411784,
               "qt": 0.946352946, "pt": 0.473176473, "cup": 0.2365882365,
               "floz": 0.0295735295625},
    "speed": {"m/s": 1.0, "km/h": 0.2777777778, "mph": 0.44704, "kn": 0.5144444444},
    "time": {"s": 1.0, "min": 60.0, "h": 3600.0, "day": 86400.0, "week": 604800.0},
    "data": {"B": 1.0, "KB": 1024.0, "MB": 1024.0**2, "GB": 1024.0**3,
             "TB": 1024.0**4, "bit": 0.125},
}

def convert_linear(category: str, value: float, source: str, target: str) -> float:
    table = LINEAR_UNITS[category]
    if source not in table or target not in table:
        raise ValueError(f"unknown unit for {category}; choose from {', '.join(sorted(table))}")
    return value * table[source] / table[target]

def convert_temperature(value: float, source: str, target: str) -> float:
    if source == target:
        return value
    # Normalise to Celsius first.
    if source == "C":
        celsius = value
    elif source == "F":
        celsius = (value - 32) * 5 / 9
    elif source == "K":
        celsius = value - 273.15
    elif source == "R":
        celsius = (value - 491.67) * 5 / 9
    else:
        raise ValueError("temperature units are C, F, K and R")
    if target == "C":
        return celsius
    if target == "F":
        return celsius * 9 / 5 + 32
    if target == "K":
        return celsius + 273.15
    if target == "R":
        return (celsius + 273.15) * 9 / 5
    raise ValueError("temperature units are C, F, K and R")

def convert(category: str, value: float, source: str, target: str) -> float:
    category = category.lower()
    if category == "temperature":
        return convert_temperature(value, source, target)
    if category not in LINEAR_UNITS:
        raise ValueError(f"unknown category '{category}'")
    return convert_linear(category, value, source, target)

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--category", choices=["temperature", *LINEAR_UNITS])
    parser.add_argument("--value", type=float)
    parser.add_argument("--from", dest="source")
    parser.add_argument("--to", dest="target")
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()

    if args.demo:
        samples = [("temperature", 100, "C", "F"), ("temperature", 32, "F", "C"),
                   ("length", 26.2, "mi", "km"), ("mass", 175, "lb", "kg"),
                   ("volume", 2, "gal", "l"), ("speed", 60, "mph", "km/h"),
                   ("data", 1.5, "GB", "MB")]
        for cat, val, src, dst in samples:
            print(f"{val:g} {src} = {convert(cat, val, src, dst):.4g} {dst}  ({cat})")
        return

    if args.category and args.value is not None and args.source and args.target:
        try:
            print(f"{args.value:g} {args.source} = {convert(args.category, args.value, args.source, args.target):.6g} {args.target}")
        except ValueError as exc:
            print(f"Error: {exc}")
        return

    category = input("Category (temperature/length/mass/volume/speed/time/data): ").strip()
    value = float(input("Value: "))
    source = input("From unit: ").strip()
    target = input("To unit: ").strip()
    try:
        print(f"{value:g} {source} = {convert(category, value, source, target):.6g} {target}")
    except ValueError as exc:
        print(f"Error: {exc}")

if __name__ == "__main__":
    main()
