#!/usr/bin/env python3
"""Recipes with ingredients, categories and a manager that can scale and search."""
import argparse
from dataclasses import dataclass, field

@dataclass
class Ingredient:
    name: str
    quantity: float
    unit: str = ""

    def scaled(self, factor: float) -> "Ingredient":
        return Ingredient(self.name, self.quantity * factor, self.unit)

    def __str__(self):
        return " ".join(part for part in (f"{self.quantity:g}", self.unit, self.name) if part)

@dataclass
class Recipe:
    name: str
    category: str
    servings: int
    ingredients: list = field(default_factory=list)
    steps: list = field(default_factory=list)

    def add(self, ingredient: Ingredient) -> None:
        self.ingredients.append(ingredient)

    def scaled(self, servings: int) -> "Recipe":
        if servings <= 0:
            raise ValueError("servings must be positive")
        factor = servings / self.servings
        return Recipe(self.name, self.category, servings,
                      [i.scaled(factor) for i in self.ingredients], list(self.steps))

    def __str__(self):
        lines = [f"{self.name} ({self.category}, serves {self.servings})"]
        lines += [f"  - {ingredient}" for ingredient in self.ingredients]
        lines += [f"  {index}. {step}" for index, step in enumerate(self.steps, 1)]
        return "\n".join(lines)

class RecipeManager:
    def __init__(self):
        self.recipes = {}

    def add(self, recipe: Recipe) -> None:
        if recipe.name in self.recipes:
            raise ValueError(f"recipe '{recipe.name}' already exists")
        self.recipes[recipe.name] = recipe

    def by_category(self, category: str):
        return [r for r in self.recipes.values() if r.category.lower() == category.lower()]

    def with_ingredient(self, ingredient: str):
        needle = ingredient.lower()
        return [r for r in self.recipes.values()
                if any(needle in item.name.lower() for item in r.ingredients)]

    def grocery_list(self, names, servings_map=None):
        servings_map = servings_map or {}
        totals = {}
        for name in names:
            recipe = self.recipes.get(name)
            if not recipe:
                raise ValueError(f"unknown recipe '{name}'")
            scaled = recipe.scaled(servings_map.get(name, recipe.servings))
            for ingredient in scaled.ingredients:
                key = (ingredient.name.lower(), ingredient.unit)
                totals[key] = totals.get(key, 0) + ingredient.quantity
        return [" ".join(part for part in (f"{quantity:g}", unit, name) if part)
                for (name, unit), quantity in sorted(totals.items())]

def demo() -> None:
    manager = RecipeManager()
    pancakes = Recipe("Pancakes", "breakfast", 4,
                      [Ingredient("flour", 200, "g"), Ingredient("milk", 300, "ml"),
                       Ingredient("eggs", 2), Ingredient("sugar", 2, "tbsp")],
                      ["Whisk the dry ingredients.", "Add milk and eggs.", "Cook on a hot griddle."])
    curry = Recipe("Chicken Curry", "main course", 6,
                   [Ingredient("chicken", 800, "g"), Ingredient("coconut milk", 400, "ml"),
                    Ingredient("curry paste", 3, "tbsp")],
                   ["Brown the chicken.", "Add paste and coconut milk.", "Simmer 25 minutes."])
    manager.add(pancakes); manager.add(curry)
    print(manager.recipes["Pancakes"].scaled(8))
    print("breakfast recipes:", [r.name for r in manager.by_category("breakfast")])
    print("recipes with chicken:", [r.name for r in manager.with_ingredient("chicken")])
    print("grocery list:", "; ".join(manager.grocery_list(["Pancakes", "Chicken Curry"], {"Pancakes": 8})))

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--demo", action="store_true")
    parser.parse_args()
    demo()

if __name__ == "__main__":
    main()
