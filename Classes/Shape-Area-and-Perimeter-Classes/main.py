#!/usr/bin/env python3
"""Abstract Shape with area/perimeter overrides for common shapes."""
import argparse
import math
from abc import ABC, abstractmethod

class Shape(ABC):
    name = "shape"

    @abstractmethod
    def area(self) -> float: ...

    @abstractmethod
    def perimeter(self) -> float: ...

    def __str__(self):
        return f"{self.name:<10} area={self.area():>10.3f}  perimeter={self.perimeter():>10.3f}"

class Circle(Shape):
    name = "circle"
    def __init__(self, radius): self.radius = radius
    def area(self): return math.pi * self.radius ** 2
    def perimeter(self): return 2 * math.pi * self.radius

class Rectangle(Shape):
    name = "rectangle"
    def __init__(self, width, height): self.width, self.height = width, height
    def area(self): return self.width * self.height
    def perimeter(self): return 2 * (self.width + self.height)

class Square(Rectangle):
    name = "square"
    def __init__(self, side): super().__init__(side, side)

class Triangle(Shape):
    name = "triangle"
    def __init__(self, a, b, c):
        if a + b <= c or a + c <= b or b + c <= a:
            raise ValueError("triangle inequality violated")
        self.a, self.b, self.c = a, b, c
    def area(self):
        s = self.perimeter() / 2
        return math.sqrt(s * (s - self.a) * (s - self.b) * (s - self.c))
    def perimeter(self): return self.a + self.b + self.c

class Diamond(Shape):
    """A rhombus defined by its two diagonals."""
    name = "diamond"
    def __init__(self, diagonal1, diagonal2):
        self.d1, self.d2 = diagonal1, diagonal2
    def area(self): return self.d1 * self.d2 / 2
    def perimeter(self): return 4 * math.hypot(self.d1 / 2, self.d2 / 2)

def demo() -> None:
    shapes = [Circle(3), Rectangle(4, 6), Square(5), Triangle(3, 4, 5), Diamond(6, 8)]
    for shape in shapes:
        print(shape)
    print(f"largest area: {max(shapes, key=lambda s: s.area()).name}")

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--demo", action="store_true")
    parser.parse_args()
    demo()

if __name__ == "__main__":
    main()
