#!/usr/bin/env python3
"""A turtle on a 20x20 floor, driven by commands, with ASCII and SVG output."""
import argparse
import math

GRID = 20

COMMANDS_HELP = """Commands:
  F n      move forward n cells (pen down draws)
  L deg / R deg   turn left/right (default 90)
  U / D    pen up / pen down
  HOME     return to centre facing east
  COLOR c  set stroke colour (SVG)
  REPEAT k [ commands ]   repeat a block k times
  # ...    comment
"""

class Turtle:
    def __init__(self, size=GRID):
        self.size = size
        self.x = size / 2
        self.y = size / 2
        self.heading = 0.0  # degrees, 0 = east, 90 = north
        self.pen = True
        self.colour = "#1f77b4"
        self.segments = []
        self.cells = set()

    def _step_line(self, x0, y0, x1, y1):
        steps = max(1, int(max(abs(x1 - x0), abs(y1 - y0)) * 4))
        for i in range(steps + 1):
            x = x0 + (x1 - x0) * i / steps
            y = y0 + (y1 - y0) * i / steps
            cell_x, cell_y = int(round(x)), int(round(y))
            if 0 <= cell_x < self.size and 0 <= cell_y < self.size:
                self.cells.add((cell_x, cell_y))

    def forward(self, distance: float):
        radians = math.radians(self.heading)
        nx = self.x + math.cos(radians) * distance
        ny = self.y + math.sin(radians) * distance
        if self.pen:
            self.segments.append((self.x, self.y, nx, ny, self.colour))
            self._step_line(self.x, self.y, nx, ny)
        self.x, self.y = nx, ny

    def turn(self, degrees: float):
        self.heading = (self.heading + degrees) % 360

    def home(self):
        self.x = self.y = self.size / 2
        self.heading = 0.0

    def ascii(self) -> str:
        rows = []
        for y in range(self.size - 1, -1, -1):
            row = "".join("*" if (x, y) in self.cells else "." for x in range(self.size))
            rows.append(row)
        return "\n".join(rows)

    def svg(self, scale=20) -> str:
        width = height = self.size * scale
        paths = "".join(
            f'<line x1="{x0*scale:.1f}" y1="{(self.size-y0)*scale:.1f}" '
            f'x2="{x1*scale:.1f}" y2="{(self.size-y1)*scale:.1f}" stroke="{colour}" stroke-width="2"/>'
            for x0, y0, x1, y1, colour in self.segments)
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
                f'viewBox="0 0 {width} {height}"><rect width="100%" height="100%" fill="#fafafa"/>'
                f'{paths}</svg>')

def run(commands, turtle=None):
    turtle = turtle or Turtle()
    tokens = commands.replace("[", " [ ").replace("]", " ] ").replace("\n", " ; ").split(";")
    for line in tokens:
        words = line.split()
        index = 0
        while index < len(words):
            command = words[index].upper()
            if command.startswith("#"):
                break
            if command == "F":
                turtle.forward(float(words[index + 1])); index += 2
            elif command == "L":
                turtle.turn(float(words[index + 1]) if index + 1 < len(words) and words[index + 1][0].isdigit() else 90)
                index += 2 if index + 1 < len(words) and words[index + 1][0].isdigit() else 1
            elif command == "R":
                turtle.turn(-(float(words[index + 1]) if index + 1 < len(words) and words[index + 1][0].isdigit() else 90))
                index += 2 if index + 1 < len(words) and words[index + 1][0].isdigit() else 1
            elif command == "U":
                turtle.pen = False; index += 1
            elif command == "D":
                turtle.pen = True; index += 1
            elif command == "HOME":
                turtle.home(); index += 1
            elif command == "COLOR":
                turtle.colour = words[index + 1]; index += 2
            elif command == "REPEAT":
                count = int(words[index + 1])
                start = index + 2
                depth, end = 1, start
                while end < len(words) and depth:
                    if words[end] == "[": depth += 1
                    elif words[end] == "]": depth -= 1
                    end += 1
                body = " ".join(words[start + 1:end - 1])
                for _ in range(count):
                    run(body, turtle)
                index = end
            else:
                index += 1
    return turtle

DEMO = """
REPEAT 4 [ F 5 R 90 ]
U
HOME
D
COLOR #d62728
F 8
"""

def demo() -> None:
    turtle = run(DEMO)
    print(turtle.ascii())
    print(f"position: ({turtle.x:.1f}, {turtle.y:.1f}) heading {turtle.heading:g} degrees")
    svg = turtle.svg()
    print(f"svg bytes: {len(svg)}, segments: {len(turtle.segments)}")

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, epilog=COMMANDS_HELP,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--file", help="command file")
    parser.add_argument("--commands", help="commands separated by ';'")
    parser.add_argument("--svg")
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()
    if args.demo or not (args.file or args.commands):
        demo(); return
    commands = open(args.file).read() if args.file else args.commands
    turtle = run(commands)
    print(turtle.ascii())
    if args.svg:
        open(args.svg, "w").write(turtle.svg())
        print("wrote", args.svg)

if __name__ == "__main__":
    main()
