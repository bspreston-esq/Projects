#!/usr/bin/env python3
"""Flower shop: flower stock, bouquets, orders and restock alerts."""
import argparse
from dataclasses import dataclass, field

@dataclass
class Flower:
    name: str
    price: float
    stock: int = 0
    restock_level: int = 5

    def take(self, count: int) -> None:
        if count < 0:
            raise ValueError("count cannot be negative")
        if count > self.stock:
            raise ValueError(f"only {self.stock} {self.name} left")
        self.stock -= count

    @property
    def needs_restock(self) -> bool:
        return self.stock <= self.restock_level

@dataclass
class Bouquet:
    name: str
    composition: dict = field(default_factory=dict)  # flower name -> count
    labour: float = 5.0

    def price(self, catalogue) -> float:
        return self.labour + sum(catalogue[name].price * count for name, count in self.composition.items())

class FlowerShop:
    def __init__(self, name: str):
        self.name = name
        self.catalogue = {}
        self.orders = []

    def add_flower(self, flower: Flower) -> None:
        self.catalogue[flower.name] = flower

    def restock(self, name: str, count: int) -> None:
        if name not in self.catalogue or count < 0:
            raise ValueError("unknown flower or negative count")
        self.catalogue[name].stock += count

    def sell(self, bouquet: Bouquet, customer: str) -> dict:
        for name, count in bouquet.composition.items():
            if name not in self.catalogue:
                raise ValueError(f"unknown flower '{name}'")
        for name, count in bouquet.composition.items():
            self.catalogue[name].take(count)
        order = {"customer": customer, "bouquet": bouquet.name,
                 "total": bouquet.price(self.catalogue)}
        self.orders.append(order)
        return order

    def revenue(self) -> float:
        return sum(order["total"] for order in self.orders)

    def restock_needed(self):
        return [flower.name for flower in self.catalogue.values() if flower.needs_restock]

def demo() -> None:
    shop = FlowerShop("Petal & Twig")
    for flower in (Flower("rose", 2.50, 40), Flower("tulip", 1.80, 4),
                   Flower("lily", 3.20, 12), Flower("daisy", 1.20, 30)):
        shop.add_flower(flower)
    bouquet = Bouquet("Spring Mix", {"rose": 6, "tulip": 4, "daisy": 5})
    order = shop.sell(bouquet, "Ada")
    print(f"order for {order['customer']}: {order['bouquet']} = ${order['total']:.2f}")
    print("restock needed:", shop.restock_needed())
    shop.restock("tulip", 20)
    print("after restock, tulips:", shop.catalogue["tulip"].stock)
    print(f"revenue: ${shop.revenue():.2f}")

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--demo", action="store_true")
    parser.parse_args()
    demo()

if __name__ == "__main__":
    main()
