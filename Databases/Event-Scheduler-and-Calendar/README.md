# Event Scheduler and Calendar

**Category:** Databases

## Problem

Make an application which allows the user to enter a date and time of an event, event notes and then schedule those events on a calendar. The user can then browse the calendar or search the calendar for specific events. Optional: Allow the application to create re-occurrence events that reoccur every day, week, month, year etc.

## Solution

SQLite `events` table with start/end timestamps, notes and recurrence (none/daily/weekly/monthly/yearly). Occurrences are expanded into a requested date range, the month view marks days with events using `*`, and search covers both title and notes.

## How to run

Requires Python 3.8+ and no third-party packages.

```bash
python3 main.py --db calendar.db --add "Standup" 2026-11-02T09:30 2026-11-02T09:45 weekly
python3 main.py --db calendar.db --month 2026-11
python3 main.py --demo
```

## Example

```text
November 2026
Mo  Tu  We  Th  Fr  Sa  Su
                         1
 2*  3   4   5*  6*  7   8
 9* 10  11  12  13  14  15
2026-11-02 09:30 Team standup
2026-11-05 14:00 Dentist
2026-11-06 16:00 Retrospective
```
