#!/usr/bin/env python3
"""Combine images into an animated GIF."""
import argparse
import os
import tempfile

try:
    from PIL import Image, ImageDraw
except ImportError:  # pragma: no cover
    Image = None

def create_gif(paths, output: str, duration: int = 200, loop: int = 0, size=None) -> str:
    if not paths:
        raise ValueError("no frames supplied")
    frames = []
    for path in paths:
        with Image.open(path) as image:
            frame = image.convert("RGB")
            if size:
                frame.thumbnail(size)
            frames.append(frame)
    width = max(frame.width for frame in frames)
    height = max(frame.height for frame in frames)
    canvas_frames = [Image.new("RGB", (width, height), (0, 0, 0)) for _ in frames]
    for canvas, frame in zip(canvas_frames, frames):
        canvas.paste(frame, ((width - frame.width) // 2, (height - frame.height) // 2))
    canvas_frames[0].save(output, save_all=True, append_images=canvas_frames[1:],
                          duration=duration, loop=loop, optimize=True)
    return output

def demo() -> None:
    if Image is None:
        print("Pillow is required for the demo (pip install pillow)")
        return
    with tempfile.TemporaryDirectory() as tmp:
        paths = []
        for index in range(12):
            image = Image.new("RGB", (320, 240), (20, 20, 30))
            draw = ImageDraw.Draw(image)
            x = 20 + index * 20
            draw.ellipse([x, 90, x + 60, 150], fill=(240, 180, 60))
            path = os.path.join(tmp, f"frame_{index:02d}.png")
            image.save(path); paths.append(path)
        output = os.path.join(tmp, "animation.gif")
        create_gif(paths, output, duration=80)
        with Image.open(output) as gif:
            print(f"gif: {gif.size[0]}x{gif.size[1]}, frames={getattr(gif, 'n_frames', 1)}, "
                  f"duration={gif.info.get('duration')} ms, loop={gif.info.get('loop')}")
            print(f"bytes: {os.path.getsize(output):,}")

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("images", nargs="*")
    parser.add_argument("--output", default="animation.gif")
    parser.add_argument("--duration", type=int, default=200, help="milliseconds per frame")
    parser.add_argument("--loop", type=int, default=0, help="0 loops forever")
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()
    if args.demo or not args.images:
        demo(); return
    print("wrote", create_gif(args.images, args.output, args.duration, args.loop))

if __name__ == "__main__":
    main()
