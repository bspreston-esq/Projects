# Alarm Clock

**Category:** Numbers

## Problem

A simple clock where it plays a sound after X number of minutes/seconds or at a particular time.

## Solution

A monotonic-clock countdown prints a live remaining-time line, then plays a generated 880 Hz WAV through whichever system player exists (aplay, paplay, afplay, play) and falls back to the terminal bell. `--at HH:MM` schedules the next occurrence of that wall-clock time.

## How to run

Requires Python 3.8+ and no third-party packages.

```bash
python3 main.py --seconds 90
python3 main.py --at 07:30
python3 main.py --demo     # rings after half a second
```

## Example

```text
Demo: ringing in 0.5 seconds
Demo: alarm rang after 0.5 seconds
```
