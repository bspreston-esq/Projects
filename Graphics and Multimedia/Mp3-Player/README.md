# Mp3 Player

**Category:** Graphics and Multimedia

## Problem

A simple program for playing your favorite music files. Add features you think are missing from your favorite music player.

## Solution

A `Playlist` with wrap-around next/previous and ID3v1 metadata, plus playback delegated to whichever system decoder exists (ffplay, mpg123, afplay, aplay). The demo builds tagged files, exercises navigation and reports which player is installed without blocking on audio.

## How to run

Requires Python 3.8+ and no third-party packages.

```bash
python3 main.py track1.mp3 track2.mp3
python3 main.py --demo
```

## Example

```text
>  1. The Testers - First Track
   2. Demo Band - Second Track
   3. Fixture - Third Track
next: Second Track
previous: First Track
system player: ffplay
```
