#!/usr/bin/env python3
"""Person class and a family tree that prints generations and ancestor paths."""
import argparse
from dataclasses import dataclass, field

@dataclass
class Person:
    name: str
    born: str = ""
    died: str = ""
    parents: list = field(default_factory=list)
    children: list = field(default_factory=list)

    def add_child(self, child: "Person") -> None:
        if child not in self.children:
            self.children.append(child)
        if self not in child.parents:
            child.parents.append(self)

    def lifespan(self) -> str:
        if self.died:
            return f"{self.born}-{self.died}"
        return f"b. {self.born}" if self.born else ""

class FamilyTree:
    def __init__(self, root: Person):
        self.root = root
        self.people = {}

    def add(self, person: Person) -> None:
        self.people[person.name] = person

    def ancestors(self, person: Person):
        seen, stack, result = set(), [person], []
        while stack:
            current = stack.pop()
            for parent in current.parents:
                if parent.name not in seen:
                    seen.add(parent.name); result.append(parent); stack.append(parent)
        return result

    def relationship(self, a: Person, b: Person) -> str:
        if a is b:
            return "same person"
        if any(child is b for child in a.children):
            return "parent"
        if any(child is a for child in b.children):
            return "child"
        if any(p is q for p in a.parents for q in b.parents):
            return "sibling"
        a_anc = {p.name for p in self.ancestors(a)}
        b_anc = {p.name for p in self.ancestors(b)}
        if b.name in a_anc:
            return "descendant"
        if a.name in b_anc:
            return "ancestor"
        return "unrelated"

    def render(self) -> str:
        lines = []

        def walk(person, depth=0):
            marker = "  " * depth + ("└─ " if depth else "")
            lines.append(f"{marker}{person.name} {person.lifespan()}".rstrip())
            for child in sorted(person.children, key=lambda p: p.born or ""):
                walk(child, depth + 1)

        walk(self.root)
        return "\n".join(lines)

def demo() -> None:
    tree = FamilyTree(Person("Ada Sr.", "1930", "2005"))
    for person in (tree.root,
                   Person("Grace", "1955"), Person("Alan", "1957"),
                   Person("Katherine", "1980"), Person("Tim", "1983"),
                   Person("Ada Jr.", "2010")):
        tree.add(person)
    tree.root.add_child(tree.people["Grace"])
    tree.root.add_child(tree.people["Alan"])
    tree.people["Grace"].add_child(tree.people["Katherine"])
    tree.people["Grace"].add_child(tree.people["Tim"])
    tree.people["Katherine"].add_child(tree.people["Ada Jr."])
    print(tree.render())
    print("Katherine -> Ada Sr.:", tree.relationship(tree.people["Katherine"], tree.root))
    print("Grace and Alan:", tree.relationship(tree.people["Grace"], tree.people["Alan"]))
    print("ancestors of Ada Jr.:", ", ".join(p.name for p in tree.ancestors(tree.people["Ada Jr."])))

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--demo", action="store_true")
    parser.parse_args()
    demo()

if __name__ == "__main__":
    main()
