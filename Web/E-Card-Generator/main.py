#!/usr/bin/env python3
"""Generate a self-contained HTML e-card from a template."""
import argparse
import html
import os

TEMPLATES = {
    "birthday": ("Happy Birthday, {name}!", "Wishing you a day full of cake, laughter and excellent company."),
    "holiday": ("Season's Greetings, {name}", "May the holidays bring you rest, warmth and good food."),
    "thankyou": ("Thank You, {name}", "Your kindness made all the difference. Consider this a small token of gratitude."),
}

PAGE = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><title>{title}</title>
<style>
  :root {{ color-scheme: dark; }}
  body {{ margin: 0; min-height: 100vh; display: grid; place-items: center;
         font-family: Georgia, 'Times New Roman', serif;
         background: radial-gradient(circle at 30% 20%, {accent1}, {accent2} 70%); }}
  .card {{ background: rgba(15,15,20,.78); color: #f7f3e9; max-width: 34rem;
          padding: 3rem 3.5rem; border-radius: 18px; text-align: center;
          box-shadow: 0 25px 60px rgba(0,0,0,.45); border: 1px solid rgba(255,255,255,.12); }}
  h1 {{ font-size: 2.1rem; margin: 0 0 1rem; letter-spacing: .02em; }}
  p {{ font-size: 1.15rem; line-height: 1.7; margin: 0 0 1.5rem; }}
  .from {{ font-style: italic; opacity: .8; }}
  img {{ max-width: 100%; border-radius: 10px; margin-bottom: 1.5rem; }}
</style></head>
<body><div class="card">
{image}
<h1>{title}</h1>
<p>{message}</p>
<p class="from">- {sender}</p>
</div></body></html>"""

ACCENTS = {"birthday": ("#7a1f4b", "#1a0b2e"), "holiday": ("#0f4d3a", "#071b17"),
           "thankyou": ("#3a2c6e", "#0d0a1a")}

def generate(template: str, name: str, sender: str, message: str = "", image_url: str = "") -> str:
    if template not in TEMPLATES:
        raise ValueError(f"unknown template '{template}'; choose from {', '.join(TEMPLATES)}")
    default_title, default_message = TEMPLATES[template]
    title = html.escape(default_title.format(name=name))
    body = html.escape(message or default_message)
    image = f'<img src="{html.escape(image_url)}" alt="card illustration">' if image_url else ""
    accent1, accent2 = ACCENTS[template]
    return PAGE.format(title=title, message=body, sender=html.escape(sender), image=image,
                       accent1=accent1, accent2=accent2)

def demo() -> None:
    import tempfile
    cards = [
        ("birthday", "Ada", "Grace", "", ""),
        ("thankyou", "Alan", "Katherine", "Thanks for the review, it genuinely helped.", ""),
    ]
    with tempfile.TemporaryDirectory() as tmp:
        for template, name, sender, message, image in cards:
            output = os.path.join(tmp, f"ecard_{template}.html")
            with open(output, "w", encoding="utf-8") as fh:
                fh.write(generate(template, name, sender, message, image))
            print(f"ecard_{template}.html: {os.path.getsize(output)} bytes, title contains '{name}': {name in open(output).read()}")

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--template", choices=sorted(TEMPLATES), default="birthday")
    parser.add_argument("--name", default="Friend")
    parser.add_argument("--from", dest="sender", default="Me")
    parser.add_argument("--message")
    parser.add_argument("--image")
    parser.add_argument("--output", default="ecard.html")
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()
    if args.demo:
        demo(); return
    try:
        page = generate(args.template, args.name, args.sender, args.message or "", args.image or "")
    except ValueError as exc:
        raise SystemExit(f"Error: {exc}")
    with open(args.output, "w", encoding="utf-8") as fh:
        fh.write(page)
    print("wrote", args.output)

if __name__ == "__main__":
    main()
