#!/usr/bin/env python3
"""Count words in a string or file and summarize the most common ones."""
import argparse
import re
from collections import Counter

WORD_RE = re.compile(r"[A-Za-z0-9']+")

def summarize(text: str):
    words = WORD_RE.findall(text)
    lower = [word.lower() for word in words]
    counts = Counter(lower)
    return {
        "characters": len(text),
        "lines": text.count("\n") + (1 if text and not text.endswith("\n") else 0),
        "words": len(words),
        "unique_words": len(counts),
        "top": counts.most_common(5),
    }

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("text", nargs="?")
    parser.add_argument("--file", help="read from a text file")
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()

    if args.demo:
        sample = ("It was the best of times, it was the worst of times,\n"
                  "it was the age of wisdom, it was the age of foolishness.")
        info = summarize(sample)
        print(f"characters: {info['characters']}, lines: {info['lines']}, "
              f"words: {info['words']}, unique: {info['unique_words']}")
        print("top words:", ", ".join(f"{word} x{count}" for word, count in info["top"]))
        return

    if args.file:
        with open(args.file, encoding="utf-8", errors="ignore") as fh:
            text = fh.read()
    else:
        text = args.text if args.text is not None else input("Text: ")
    info = summarize(text)
    for key in ("characters", "lines", "words", "unique_words"):
        print(f"{key}: {info[key]}")
    print("most common:", ", ".join(f"{w} x{c}" for w, c in info["top"]))

if __name__ == "__main__":
    main()
