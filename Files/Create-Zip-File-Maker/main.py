#!/usr/bin/env python3
"""Collect files from different directories into one zip archive."""
import argparse
import os
import tempfile
import zipfile

def add_path(archive: zipfile.ZipFile, path: str, arcname=None) -> int:
    """Add a file or directory tree; returns the number of files added."""
    if os.path.isfile(path):
        archive.write(path, arcname or os.path.basename(path))
        return 1
    total = 0
    root = os.path.abspath(path)
    base = arcname or os.path.basename(root)
    for directory, _, files in os.walk(root):
        for name in sorted(files):
            full = os.path.join(directory, name)
            relative = os.path.relpath(full, root)
            archive.write(full, os.path.join(base, relative))
            total += 1
    return total

def make_zip(output: str, paths, compress=zipfile.ZIP_DEFLATED) -> tuple:
    os.makedirs(os.path.dirname(os.path.abspath(output)), exist_ok=True)
    added = 0
    with zipfile.ZipFile(output, "w", compression=compress) as archive:
        for path in paths:
            if not os.path.exists(path):
                raise ValueError(f"no such path: {path}")
            added += add_path(archive, path)
    size = os.path.getsize(output)
    return added, size

def demo() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        docs = os.path.join(tmp, "docs"); photos = os.path.join(tmp, "photos")
        os.makedirs(docs); os.makedirs(photos)
        open(os.path.join(docs, "readme.txt"), "w").write("Documentation\n")
        open(os.path.join(docs, "notes.md"), "w").write("# Notes\n")
        open(os.path.join(photos, "pixel.txt"), "w").write("not really a photo\n")
        output = os.path.join(tmp, "bundle.zip")
        added, size = make_zip(output, [docs, photos])
        print(f"added {added} files, archive {size} bytes")
        with zipfile.ZipFile(output) as archive:
            for info in archive.infolist():
                print(f"  {info.filename:<28} {info.file_size:>4} bytes -> {info.compress_size} stored")
            print("test:", archive.testzip() is None)

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default="archive.zip")
    parser.add_argument("paths", nargs="*", help="files or directories to zip")
    parser.add_argument("--store", action="store_true", help="store without compression")
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()
    if args.demo or not args.paths:
        demo(); return
    try:
        added, size = make_zip(args.output, args.paths,
                               zipfile.ZIP_STORED if args.store else zipfile.ZIP_DEFLATED)
    except (OSError, ValueError) as exc:
        raise SystemExit(f"Error: {exc}")
    print(f"added {added} files -> {args.output} ({size:,} bytes)")

if __name__ == "__main__":
    main()
