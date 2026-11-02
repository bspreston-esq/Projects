#!/usr/bin/env python3
"""Generate SVG CAPTCHAs and verify answers with a constant-time compare."""
import argparse
import hmac
import random
import string

def generate_text(length: int = 6) -> str:
    # Avoid ambiguous characters such as 0/O and 1/I.
    alphabet = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    return "".join(random.SystemRandom().choice(alphabet) for _ in range(length))

def to_svg(text: str, width: int = 220, height: int = 80) -> str:
    rng = random.Random(hash(text) & 0xFFFFFFFF)
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
             f'<rect width="100%" height="100%" fill="#f2efe6"/>']
    for _ in range(6):
        x1, y1 = rng.randint(0, width), rng.randint(0, height)
        x2, y2 = rng.randint(0, width), rng.randint(0, height)
        parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#9a9484" stroke-width="1"/>')
    slot = width / (len(text) + 1)
    for index, character in enumerate(text):
        x = slot * (index + 1)
        y = height / 2 + rng.randint(-6, 6)
        angle = rng.randint(-22, 22)
        parts.append(f'<text x="{x:.1f}" y="{y:.1f}" font-family="monospace" font-size="34" '
                     f'font-weight="bold" fill="#2c2a26" text-anchor="middle" '
                     f'transform="rotate({angle} {x:.1f} {y:.1f})">{character}</text>')
    parts.append("</svg>")
    return "\n".join(parts)

def verify(expected: str, answer: str) -> bool:
    return hmac.compare_digest(expected.upper(), answer.strip().upper())

def demo() -> None:
    for _ in range(2):
        text = generate_text(6)
        svg = to_svg(text)
        print(f"captcha {text}: {len(svg)} bytes, valid svg: {svg.startswith('<svg') and svg.endswith('</svg>')}")
        print(f"  verify correct: {verify(text, text.lower())}, wrong: {verify(text, 'XXXXXX')}")

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--length", type=int, default=6)
    parser.add_argument("--output", default="captcha.svg")
    parser.add_argument("--verify", help="answer to check against a newly generated captcha")
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()
    if args.demo:
        demo(); return
    text = generate_text(args.length)
    with open(args.output, "w", encoding="utf-8") as fh:
        fh.write(to_svg(text))
    print("wrote", args.output)
    if args.verify is not None:
        print("verified" if verify(text, args.verify) else "incorrect")
    else:
        print("answer:", text)

if __name__ == "__main__":
    main()
