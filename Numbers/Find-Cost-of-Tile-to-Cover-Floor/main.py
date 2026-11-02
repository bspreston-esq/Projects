#!/usr/bin/env python3
"""Calculate the cost of tiling a rectangular floor."""
import argparse

def tile_cost(width: float, height: float, cost_per_unit: float, waste_percent: float = 0.0):
    """Return (area, area_with_waste, total_cost) for a W x H floor."""
    if width <= 0 or height <= 0:
        raise ValueError("width and height must be positive")
    if cost_per_unit < 0:
        raise ValueError("cost cannot be negative")
    if waste_percent < 0:
        raise ValueError("waste percentage cannot be negative")
    area = width * height
    area_with_waste = area * (1 + waste_percent / 100)
    return area, area_with_waste, area_with_waste * cost_per_unit

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--width", type=float)
    parser.add_argument("--height", type=float)
    parser.add_argument("--cost", type=float, help="cost per square unit")
    parser.add_argument("--waste", type=float, default=0.0, help="extra percent for cuts/breakage")
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()

    if args.demo:
        samples = [(12, 10, 4.25, 10), (5.5, 4, 9.99, 5), (20, 20, 2.00, 0)]
        for w, h, c, waste in samples:
            area, aw, total = tile_cost(w, h, c, waste)
            print(f"{w:g} x {h:g} @ {c:.2f}/sq unit, {waste:g}% waste: "
                  f"{aw:.2f} sq units -> ${total:,.2f}")
        return

    width = args.width if args.width is not None else float(input("Floor width: "))
    height = args.height if args.height is not None else float(input("Floor height: "))
    cost = args.cost if args.cost is not None else float(input("Cost per square unit: "))
    waste = args.waste if args.waste else float(input("Waste percentage (0 for none): ") or 0)
    try:
        area, aw, total = tile_cost(width, height, cost, waste)
        print(f"Area: {area:.2f} sq units")
        print(f"With {waste:g}% waste: {aw:.2f} sq units")
        print(f"Total cost: ${total:,.2f}")
    except ValueError as exc:
        print(f"Error: {exc}")

if __name__ == "__main__":
    main()
