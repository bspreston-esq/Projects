#!/usr/bin/env python3
"""Run a regular expression against text and show every match."""
import argparse
import re

def run_regex(pattern: str, text: str, ignore_case: bool = False, group=None):
    flags = re.IGNORECASE if ignore_case else 0
    try:
        compiled = re.compile(pattern, flags)
    except re.error as exc:
        raise ValueError(f"invalid regular expression: {exc}") from exc
    matches = []
    for match in compiled.finditer(text):
        value = match.group(group) if group is not None else match.group(0)
        matches.append((match.start(), match.end(), value, match.groups()))
    return matches

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pattern", default=r"\b\w+@\w+\.\w+\b")
    parser.add_argument("--text")
    parser.add_argument("--file")
    parser.add_argument("--ignore-case", action="store_true")
    parser.add_argument("--group", type=int, help="show only this capture group")
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()

    if args.demo:
        sample = "Contact ada@example.com or grace@navy.mil; invalid: not-an-email"
        for pattern in (r"\b\w+@\w+\.\w+\b", r"(\w+)@(\w+)", r"([a-z"):
            print(f"pattern: {pattern}")
            try:
                matches = run_regex(pattern, sample)
            except ValueError as exc:
                print(f"  error: {exc}")
                continue
            for start, end, value, groups in matches:
                print(f"  [{start:>2}:{end:>2}] {value!r} groups={groups}")
            print(f"  {len(matches)} match(es)")
        return

    if args.file:
        with open(args.file, encoding="utf-8", errors="ignore") as fh:
            text = fh.read()
    else:
        text = args.text if args.text is not None else input("Text: ")
    try:
        matches = run_regex(args.pattern, text, args.ignore_case, args.group)
    except ValueError as exc:
        print(f"Error: {exc}")
        return
    for start, end, value, groups in matches:
        print(f"{start}:{end}  {value!r}  groups={groups}")
    print(f"{len(matches)} match(es)")

if __name__ == "__main__":
    main()
