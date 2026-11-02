#!/usr/bin/env python3
"""Product and Inventory classes for tracking stock and total value."""
import argparse
from dataclasses import dataclass, field

@dataclass
class Product:
    product_id: str
    name: str
    price: float
    quantity: int = 0

    def __post_init__(self):
        if self.price < 0 or self.quantity < 0:
            raise ValueError("price and quantity cannot be negative")

    @property
    def value(self) -> float:
        return self.price * self.quantity

    def __str__(self):
        return f"{self.product_id:<6} {self.name:<22} ${self.price:>8,.2f} x {self.quantity:>3} = ${self.value:>10,.2f}"

@dataclass
class Inventory:
    products: dict = field(default_factory=dict)

    def add_product(self, product: Product) -> None:
        if product.product_id in self.products:
            raise ValueError(f"product {product.product_id} already exists")
        self.products[product.product_id] = product

    def remove_product(self, product_id: str) -> Product:
        if product_id not in self.products:
            raise ValueError(f"unknown product {product_id}")
        return self.products.pop(product_id)

    def adjust(self, product_id: str, delta: int) -> None:
        product = self.products.get(product_id)
        if not product:
            raise ValueError(f"unknown product {product_id}")
        if product.quantity + delta < 0:
            raise ValueError("cannot reduce stock below zero")
        product.quantity += delta

    def total_value(self) -> float:
        return sum(product.value for product in self.products.values())

    def low_stock(self, threshold: int = 5):
        return [p for p in self.products.values() if p.quantity <= threshold]

    def report(self) -> str:
        lines = [product.__str__() for product in sorted(self.products.values(), key=lambda p: p.product_id)]
        lines.append(f"{'TOTAL':<46}${self.total_value():>12,.2f}")
        return "\n".join(lines)

def demo() -> None:
    inventory = Inventory()
    inventory.add_product(Product("P001", "Mechanical keyboard", 89.99, 12))
    inventory.add_product(Product("P002", "USB-C cable", 12.50, 40))
    inventory.add_product(Product("P003", "27-inch monitor", 249.00, 3))
    inventory.adjust("P001", -2)
    print(inventory.report())
    print("low stock:", ", ".join(f"{p.name} ({p.quantity})" for p in inventory.low_stock()))
    print(f"total inventory value: ${inventory.total_value():,.2f}")

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()
    if args.demo:
        demo()
        return
    inventory = Inventory()
    print("Commands: add ID NAME PRICE QTY | remove ID | adjust ID DELTA | list | value | quit")
    while True:
        raw = input("> ").strip()
        if not raw:
            continue
        parts = raw.split()
        command = parts[0].lower()
        try:
            if command == "add":
                inventory.add_product(Product(parts[1], " ".join(parts[2:-2]), float(parts[-2]), int(parts[-1])))
            elif command == "remove":
                inventory.remove_product(parts[1])
            elif command == "adjust":
                inventory.adjust(parts[1], int(parts[2]))
            elif command == "list":
                print(inventory.report())
            elif command == "value":
                print(f"${inventory.total_value():,.2f}")
            elif command in ("quit", "exit"):
                break
        except (IndexError, ValueError) as exc:
            print(f"Error: {exc}")

if __name__ == "__main__":
    main()
