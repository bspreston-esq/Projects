#!/usr/bin/env python3
"""Build an HTML slide show (with fades) or open a Tkinter viewer."""
import argparse
import base64
import io
import os
import tempfile

try:
    from PIL import Image, ImageDraw
except ImportError:  # pragma: no cover
    Image = None

def data_uri(path: str, box=(960, 540)) -> str:
    with Image.open(path) as image:
        image = image.convert("RGB")
        image.thumbnail(box)
        buffer = io.BytesIO()
        image.save(buffer, "JPEG", quality=85)
    return "data:image/jpeg;base64," + base64.b64encode(buffer.getvalue()).decode()

def build_html(paths, output: str, duration: float = 4.0, title="Slide Show") -> str:
    if not paths:
        raise ValueError("no images supplied")
    duration_ms = int(max(1.0, duration) * 1000)
    slides = "\n".join(
        f'<figure class="slide" style="animation-delay:{index * duration_ms}ms">'
        f'<img src="{data_uri(path)}" alt="{os.path.basename(path)}">'
        f'<figcaption>{os.path.basename(path)}</figcaption></figure>'
        for index, path in enumerate(paths))
    total = duration_ms * len(paths)
    html = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><title>{title}</title>
<style>
  html, body {{ margin:0; height:100%; background:#0b0c10; color:#eee; font-family:system-ui, sans-serif; }}
  .stage {{ position:relative; height:100vh; overflow:hidden; }}
  .slide {{ position:absolute; inset:0; margin:0; opacity:0; animation: fade {total}ms infinite; }}
  .slide img {{ width:100%; height:100%; object-fit:contain; }}
  figcaption {{ position:absolute; bottom:1rem; left:0; right:0; text-align:center; opacity:.75; }}
  @keyframes fade {{
    0% {{ opacity:0; }} 4% {{ opacity:1; }} {100/len(paths)*0.8:.2f}% {{ opacity:1; }}
    {100/len(paths):.2f}% {{ opacity:0; }} 100% {{ opacity:0; }}
  }}
</style></head><body><div class="stage">{slides}</div></body></html>"""
    with open(output, "w", encoding="utf-8") as fh:
        fh.write(html)
    return output

def gui(paths):
    try:
        import tkinter as tk
    except ImportError:
        print("Tkinter is not installed; writing an HTML show instead.")
        return build_html(paths, "slideshow.html")
    root = tk.Tk(); root.title("Slide Show"); root.configure(bg="black")
    label = tk.Label(root, bg="black")
    label.pack(fill="both", expand=True)
    images = []
    for path in paths:
        with Image.open(path) as image:
            image = image.convert("RGB")
            image.thumbnail((1200, 800))
            images.append(image.copy())
    index = {"value": 0}
    def advance():
        label.configure(image=images[index["value"]])
        index["value"] = (index["value"] + 1) % len(images)
        root.after(4000, advance)
    advance(); root.mainloop()
    return "gui"

def demo() -> None:
    if Image is None:
        print("Pillow is required for the demo (pip install pillow)")
        return
    with tempfile.TemporaryDirectory() as tmp:
        colours = [(180, 60, 60), (60, 140, 90), (60, 90, 190), (190, 150, 40)]
        paths = []
        for index, colour in enumerate(colours):
            path = os.path.join(tmp, f"slide_{index}.png")
            image = Image.new("RGB", (800, 450), colour)
            ImageDraw.Draw(image).text((40, 40), f"Slide {index + 1}", fill="white")
            image.save(path); paths.append(path)
        output = build_html(paths, os.path.join(tmp, "show.html"), duration=3)
        html = open(output, encoding="utf-8").read()
        print(f"slides: {html.count('class=\"slide\"')}, bytes: {os.path.getsize(output):,}")
        print("embedded images:", html.count("data:image/jpeg;base64,"))

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("images", nargs="*")
    parser.add_argument("--output", default="slideshow.html")
    parser.add_argument("--duration", type=float, default=4.0)
    parser.add_argument("--gui", action="store_true")
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()
    if args.demo or not args.images:
        demo(); return
    if args.gui:
        print(gui(args.images)); return
    print("wrote", build_html(args.images, args.output, args.duration))

if __name__ == "__main__":
    main()
