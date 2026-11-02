#!/usr/bin/env python3
"""SQLite-backed event calendar with month view and recurrence."""
import argparse
import calendar
import datetime as dt
import os
import sqlite3
import tempfile

SCHEMA = """CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    start_at TEXT NOT NULL,
    end_at TEXT,
    notes TEXT DEFAULT '',
    recurrence TEXT DEFAULT 'none'
)"""

def connect(path):
    connection = sqlite3.connect(path)
    connection.executescript(SCHEMA)
    connection.commit()
    return connection

def add_event(connection, title, start_at, end_at=None, notes="", recurrence="none"):
    if recurrence not in ("none", "daily", "weekly", "monthly", "yearly"):
        raise ValueError("recurrence must be none, daily, weekly, monthly or yearly")
    start = dt.datetime.fromisoformat(start_at)
    end = dt.datetime.fromisoformat(end_at) if end_at else start + dt.timedelta(hours=1)
    if end < start:
        raise ValueError("end must be after start")
    cursor = connection.execute(
        "INSERT INTO events (title,start_at,end_at,notes,recurrence) VALUES (?,?,?,?,?)",
        (title, start.isoformat(timespec="minutes"), end.isoformat(timespec="minutes"), notes, recurrence))
    connection.commit()
    return cursor.lastrowid

def occurrences(connection, start_date: dt.date, end_date: dt.date):
    """Expand recurring events into (date, title, start_time, recurrence) tuples."""
    results = []
    rows = connection.execute("SELECT title,start_at,end_at,recurrence FROM events").fetchall()
    for title, start_at, end_at, recurrence in rows:
        start = dt.datetime.fromisoformat(start_at)
        if recurrence == "none":
            if start_date <= start.date() <= end_date:
                results.append((start.date(), start, title))
        else:
            current = start
            guard = 0
            while current.date() <= end_date and guard < 1000:
                if current.date() >= start_date:
                    results.append((current.date(), current, title))
                guard += 1
                if recurrence == "daily":
                    current += dt.timedelta(days=1)
                elif recurrence == "weekly":
                    current += dt.timedelta(weeks=1)
                elif recurrence == "monthly":
                    month = current.month % 12 + 1
                    year = current.year + (1 if current.month == 12 else 0)
                    day = min(current.day, calendar.monthrange(year, month)[1])
                    current = current.replace(year=year, month=month, day=day)
                else:
                    year = current.year + 1
                    day = min(current.day, calendar.monthrange(year, current.month)[1])
                    current = current.replace(year=year, day=day)
                if current <= start and recurrence != "daily":
                    break
    return sorted(results)

def month_view(connection, year: int, month: int) -> str:
    first = dt.date(year, month, 1)
    last = dt.date(year, month, calendar.monthrange(year, month)[1])
    days = {date.day for date, _, _ in occurrences(connection, first, last)}
    header = " ".join(f"{name:^3}" for name in ("Mo", "Tu", "We", "Th", "Fr", "Sa", "Su")).rstrip()
    lines = [f"{calendar.month_name[month]} {year}".center(len(header)).rstrip(), header]
    for week in calendar.monthcalendar(year, month):
        cells = [f"{day:2d}{'*' if day in days else ' '}" if day else "   " for day in week]
        lines.append(" ".join(cells).rstrip())
    return "\n".join(lines)

def demo() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        connection = connect(os.path.join(tmp, "calendar.db"))
        add_event(connection, "Team standup", "2026-11-02T09:30", "2026-11-02T09:45", "weekly sync", "weekly")
        add_event(connection, "Dentist", "2026-11-05T14:00", "2026-11-05T15:00", "bring insurance card")
        add_event(connection, "Retrospective", "2026-11-06T16:00", "2026-11-06T17:00", "monthly retro", "monthly")
        print(month_view(connection, 2026, 11))
        print()
        for date, start, title in occurrences(connection, dt.date(2026, 11, 2), dt.date(2026, 11, 8)):
            print(f"{date} {start:%H:%M} {title}")
        connection.close()

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", default="calendar.db")
    parser.add_argument("--add", nargs=4, metavar=("TITLE", "START", "END", "RECURRENCE"))
    parser.add_argument("--notes", default="")
    parser.add_argument("--month", help="YYYY-MM to display")
    parser.add_argument("--search")
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()
    if args.demo:
        demo(); return
    connection = connect(args.db)
    try:
        if args.add:
            print("added event", add_event(connection, args.add[0], args.add[1], args.add[2], args.notes, args.add[3]))
        if args.month:
            year, month = map(int, args.month.split("-"))
            print(month_view(connection, year, month))
        elif args.search:
            rows = connection.execute("SELECT id,title,start_at,notes FROM events WHERE title LIKE ? OR notes LIKE ?",
                                      (f"%{args.search}%", f"%{args.search}%")).fetchall()
            for row in rows:
                print(row)
        elif not args.add:
            for row in connection.execute("SELECT id,title,start_at,end_at,recurrence FROM events ORDER BY start_at").fetchall():
                print(row)
    finally:
        connection.close()

if __name__ == "__main__":
    main()
