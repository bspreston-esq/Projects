#!/usr/bin/env python3
"""A small immutable Complex class: addition, multiplication, negation, inversion."""
import argparse
from dataclasses import dataclass

@dataclass(frozen=True)
class Complex:
    real: float = 0.0
    imag: float = 0.0

    def __add__(self, other):
        if not isinstance(other, Complex):
            return NotImplemented
        return Complex(self.real + other.real, self.imag + other.imag)

    def __neg__(self):
        return Complex(-self.real, -self.imag)

    def __sub__(self, other):
        if not isinstance(other, Complex):
            return NotImplemented
        return self + (-other)

    def __mul__(self, other):
        if not isinstance(other, Complex):
            return NotImplemented
        return Complex(self.real * other.real - self.imag * other.imag,
                       self.real * other.imag + self.imag * other.real)

    def inverse(self):
        denominator = self.real ** 2 + self.imag ** 2
        if denominator == 0:
            raise ZeroDivisionError("cannot invert zero")
        return Complex(self.real / denominator, -self.imag / denominator)

    def __truediv__(self, other):
        if not isinstance(other, Complex):
            return NotImplemented
        return self * other.inverse()

    def __abs__(self):
        return (self.real ** 2 + self.imag ** 2) ** 0.5

    def __str__(self):
        sign = "+" if self.imag >= 0 else "-"
        return f"{self.real:g} {sign} {abs(self.imag):g}i"

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()

    a, b = Complex(3, 4), Complex(1, -2)
    if args.demo:
        print(f"a = {a}, b = {b}")
        print(f"a + b      = {a + b}")
        print(f"a * b      = {a * b}")
        print(f"-a         = {-a}")
        print(f"1 / a      = {a.inverse()}")
        print(f"a - b      = {a - b}   (derived: a + (-b))")
        print(f"a / b      = {a / b}   (derived: a * (1/b))")
        print(f"|a|        = {abs(a):g}")
        return

    def read(label):
        text = input(f"{label} (format: real imag): ").split()
        return Complex(float(text[0]), float(text[1]))

    a, b = read("a"), read("b")
    print(f"a + b = {a + b}")
    print(f"a * b = {a * b}")
    print(f"-a    = {-a}")
    print(f"1 / a = {a.inverse()}")

if __name__ == "__main__":
    main()
