# Patient / Doctor Scheduler

**Category:** Classes

## Problem

Create a patient class and a doctor class. Have a doctor that can handle multiple patients and setup a scheduling program where a doctor can only handle 16 patients during an 8 hr work day.

## Solution

Doctors own a per-date slot map covering 09:00-16:30 in 30-minute increments, exactly 16 slots. Booking validates that the time lands on a slot, rejects duplicates and enforces the daily cap; patients carry an id and contact details, and the scheduler prints a per-day report.

## How to run

Requires Python 3.8+ and no third-party packages.

```bash
python3 main.py --demo
```

## Example

```text
Dr. Chen (Cardiology) on 2026-11-03: 4/16 slots
  09:00  Ada Lovelace
  09:30  Grace Hopper
  11:00  Alan Turing
  14:30  Katherine Johnson
conflict: 2026-11-03 09:00 is already taken
after cancellation: 3 appointments
```
