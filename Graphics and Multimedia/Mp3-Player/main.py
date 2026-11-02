#!/usr/bin/env python3
"""A playlist-based mp3 player that delegates decoding to a system player."""
import argparse
import os
import shutil
import subprocess
import tempfile

PLAYERS = [("ffplay", ["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet"]),
           ("mpg123", ["mpg123", "-q"]),
           ("afplay", ["afplay"]),
           ("aplay", ["aplay", "-q"])]

def read_id3v1(path: str):
    try:
        with open(path, "rb") as fh:
            fh.seek(0, os.SEEK_END)
            if fh.tell() < 128:
                return {}
            fh.seek(-128, os.SEEK_END)
            block = fh.read(128)
    except OSError:
        return {}
    if block[:3] != b"TAG":
        return {}
    def text(chunk):
        return chunk.decode("latin-1", errors="replace").strip("\x00 ").strip()
    return {"title": text(block[3:33]), "artist": text(block[33:63]), "album": text(block[63:93])}

class Playlist:
    def __init__(self):
        self.tracks = []
        self.position = 0

    def add(self, path: str) -> None:
        if not os.path.isfile(path):
            raise ValueError(f"not a file: {path}")
        self.tracks.append(path)

    def current(self):
        if not self.tracks:
            return None
        self.position %= len(self.tracks)
        return self.tracks[self.position]

    def next(self):
        if not self.tracks:
            return None
        self.position = (self.position + 1) % len(self.tracks)
        return self.current()

    def previous(self):
        if not self.tracks:
            return None
        self.position = (self.position - 1) % len(self.tracks)
        return self.current()

    def describe(self):
        lines = []
        for index, path in enumerate(self.tracks):
            tags = read_id3v1(path)
            label = f"{tags.get('artist', '?')} - {tags.get('title', os.path.basename(path))}"
            marker = ">" if index == self.position % len(self.tracks) else " "
            lines.append(f"{marker} {index + 1:>2}. {label}")
        return "\n".join(lines) or "(empty playlist)"

def find_player():
    for name, command in PLAYERS:
        if shutil.which(name):
            return name, command
    return None, None

def play(path: str) -> str:
    name, command = find_player()
    if not name:
        return "no system audio player found (install ffmpeg, mpg123 or use afplay)"
    subprocess.run(command + [path], check=False)
    return f"played with {name}"

def demo() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        playlist = Playlist()
        for index, (artist, title) in enumerate([("The Testers", "First Track"),
                                                 ("Demo Band", "Second Track"),
                                                 ("Fixture", "Third Track")], 1):
            path = os.path.join(tmp, f"track{index}.mp3")
            with open(path, "wb") as fh:
                fh.write(b"\xff\xfb\x90\x64" + b"\x00" * 400)
                fh.write(b"TAG" + title.encode().ljust(30, b"\x00") + artist.encode().ljust(30, b"\x00")
                         + b"Demo Album".ljust(30, b"\x00") + b"2026" + b"".ljust(30, b"\x00") + b"\x00")
            playlist.add(path)
        print(playlist.describe())
        print("next:", read_id3v1(playlist.next()).get("title"))
        print("previous:", read_id3v1(playlist.previous()).get("title"))
        print("system player:", find_player()[0] or "none available")

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="*")
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()
    if args.demo:
        demo(); return
    playlist = Playlist()
    for path in args.files:
        playlist.add(path)
    if not playlist.tracks:
        print("usage: main.py track1.mp3 track2.mp3 ...")
        return
    print(playlist.describe())
    print("Commands: play | next | prev | list | quit")
    while True:
        command = input("> ").strip().lower()
        if command == "play" and playlist.current():
            print(play(playlist.current()))
        elif command == "next":
            playlist.next(); print(playlist.describe())
        elif command == "prev":
            playlist.previous(); print(playlist.describe())
        elif command == "list":
            print(playlist.describe())
        elif command in ("quit", "exit"):
            break

if __name__ == "__main__":
    main()
