#!/usr/bin/env python3
"""Add a tiled text watermark to images, optionally in parallel."""
import argparse
import os
import tempfile
from concurrent.futures import ThreadPoolExecutor

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:  # pragma: no cover
    Image = None

def watermark(path: str, output: str, text: str = "(c) Your Name",
              opacity: int = 90, spacing: int = 220, angle: int = 30) -> str:
    """Overlay repeated translucent text across the image."""
    if Image is None:
        raise RuntimeError("Pillow is required (pip install pillow)")
    with Image.open(path) as source:
        image = source.convert("RGBA")
    layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    font = ImageFont.load_default(size=max(18, image.width // 28))
    tile = Image.new("RGBA", (spacing * 2, spacing * 2), (0, 0, 0, 0))
    tile_draw = ImageDraw.Draw(tile)
    tile_draw.text((spacing // 2, spacing // 2), text, font=font, fill=(255, 255, 255, opacity))
    tile = tile.rotate(angle, expand=False)
    for y in range(-spacing, image.height + spacing, spacing):
        for x in range(-spacing, image.width + spacing, spacing):
            layer.alpha_composite(tile, (x, y))
    result = Image.alpha_composite(image, layer).convert("RGB")
    result.save(output, quality=90)
    return output

def batch(paths, output_dir, text, opacity, workers=4):
    os.makedirs(output_dir, exist_ok=True)
    results = []
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(watermark, path, os.path.join(output_dir, "wm_" + os.path.basename(path)),
                               text, opacity): path for path in paths}
        for future in futures:
            results.append(future.result())
    return results

def demo() -> None:
    if Image is None:
        print("Pillow is required for the demo (pip install pillow)")
        return
    with tempfile.TemporaryDirectory() as tmp:
        source = os.path.join(tmp, "photo.png")
        image = Image.new("RGB", (1200, 800), (40, 90, 140))
        ImageDraw.Draw(image).rectangle([200, 200, 900, 600], fill=(220, 200, 160))
        image.save(source)
        output = os.path.join(tmp, "watermarked.png")
        watermark(source, output, "DEMO COPY", opacity=110)
        original = Image.open(source).convert("RGB")
        result = Image.open(output).convert("RGB")
        differing = sum(1 for a, b in zip(original.tobytes(), result.tobytes()) if a != b)
        print(f"watermarked {original.size[0]}x{original.size[1]} -> {result.size[0]}x{result.size[1]}")
        print(f"changed pixels: {differing:,} of {original.size[0]*original.size[1]:,}")
        print(f"output bytes: {os.path.getsize(output):,}")

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("images", nargs="*")
    parser.add_argument("--text", default="(c) Your Name")
    parser.add_argument("--opacity", type=int, default=90)
    parser.add_argument("--output", default="watermarked")
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()
    if args.demo or not args.images:
        demo(); return
    results = batch(args.images, args.output, args.text, args.opacity)
    for path in results:
        print(path)

if __name__ == "__main__":
    main()
