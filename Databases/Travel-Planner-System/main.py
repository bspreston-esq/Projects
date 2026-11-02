#!/usr/bin/env python3
"""Plan a trip: flights, hotels, activities, itinerary and budget."""
import argparse
import datetime as dt
import os
import sqlite3
import tempfile

SCHEMA = """
CREATE TABLE IF NOT EXISTS trips (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL, start_date TEXT NOT NULL, end_date TEXT NOT NULL, budget REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS flights (
    id INTEGER PRIMARY KEY AUTOINCREMENT, trip_id INTEGER, airline TEXT, flight_no TEXT,
    depart TEXT, arrive TEXT, origin TEXT, destination TEXT, cost REAL
);
CREATE TABLE IF NOT EXISTS hotels (
    id INTEGER PRIMARY KEY AUTOINCREMENT, trip_id INTEGER, name TEXT,
    check_in TEXT, check_out TEXT, cost REAL
);
CREATE TABLE IF NOT EXISTS activities (
    id INTEGER PRIMARY KEY AUTOINCREMENT, trip_id INTEGER, date TEXT, title TEXT, cost REAL
);"""

def connect(path):
    connection = sqlite3.connect(path)
    connection.executescript(SCHEMA)
    connection.commit()
    return connection

def add_trip(connection, name, start, end, budget):
    start_date, end_date = dt.date.fromisoformat(start), dt.date.fromisoformat(end)
    if end_date < start_date:
        raise ValueError("end date must not precede start date")
    cursor = connection.execute("INSERT INTO trips (name,start_date,end_date,budget) VALUES (?,?,?,?)",
                                (name, start, end, budget))
    connection.commit()
    return cursor.lastrowid

def add_flight(connection, trip_id, airline, flight_no, depart, arrive, origin, destination, cost):
    dt.datetime.fromisoformat(depart); dt.datetime.fromisoformat(arrive)
    connection.execute("INSERT INTO flights (trip_id,airline,flight_no,depart,arrive,origin,destination,cost) "
                       "VALUES (?,?,?,?,?,?,?,?)",
                       (trip_id, airline, flight_no, depart, arrive, origin, destination, cost))
    connection.commit()

def add_hotel(connection, trip_id, name, check_in, check_out, cost):
    connection.execute("INSERT INTO hotels (trip_id,name,check_in,check_out,cost) VALUES (?,?,?,?,?)",
                       (trip_id, name, check_in, check_out, cost))
    connection.commit()

def add_activity(connection, trip_id, date, title, cost):
    dt.date.fromisoformat(date)
    connection.execute("INSERT INTO activities (trip_id,date,title,cost) VALUES (?,?,?,?)",
                       (trip_id, date, title, cost))
    connection.commit()

def itinerary(connection, trip_id):
    trip = connection.execute("SELECT name,start_date,end_date,budget FROM trips WHERE id=?", (trip_id,)).fetchone()
    if not trip:
        raise ValueError(f"no trip {trip_id}")
    name, start, end, budget = trip
    start_date, end_date = dt.date.fromisoformat(start), dt.date.fromisoformat(end)
    days = (end_date - start_date).days + 1
    flights = connection.execute("SELECT airline,flight_no,depart,arrive,origin,destination,cost FROM flights WHERE trip_id=? ORDER BY depart", (trip_id,)).fetchall()
    hotels = connection.execute("SELECT name,check_in,check_out,cost FROM hotels WHERE trip_id=? ORDER BY check_in", (trip_id,)).fetchall()
    activities = connection.execute("SELECT date,title,cost FROM activities WHERE trip_id=? ORDER BY date", (trip_id,)).fetchall()
    lines = [f"{name}: {start} to {end} ({days} days, budget ${budget:,.2f})", "", "Flights:"]
    lines += [f"  {depart[:10]} {depart[11:16]} {airline} {flight_no} {origin}->{destination}  ${cost:,.2f}"
              for airline, flight_no, depart, arrive, origin, destination, cost in flights]
    lines += ["", "Hotels:"]
    lines += [f"  {hotel} {check_in} to {check_out}  ${cost:,.2f}" for hotel, check_in, check_out, cost in hotels]
    lines += ["", "Itinerary:"]
    by_date = {}
    for date, title, cost in activities:
        by_date.setdefault(date, []).append((title, cost))
    current = start_date
    while current <= end_date:
        key = current.isoformat()
        for title, cost in by_date.get(key, []):
            lines.append(f"  {key}  {title}  ${cost:,.2f}")
        current += dt.timedelta(days=1)
    total = sum(row[-1] for row in flights) + sum(row[-1] for row in hotels) + sum(row[-1] for row in activities)
    lines += ["", f"Planned cost: ${total:,.2f} | remaining: ${budget - total:,.2f}"]
    return "\n".join(lines), total

def demo() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        connection = connect(os.path.join(tmp, "travel.db"))
        trip_id = add_trip(connection, "Amsterdam", "2026-11-10", "2026-11-14", 2200)
        add_flight(connection, trip_id, "KLM", "KL642", "2026-11-10T13:20", "2026-11-10T21:05", "JFK", "AMS", 640.0)
        add_flight(connection, trip_id, "KLM", "KL641", "2026-11-14T10:30", "2026-11-14T13:00", "AMS", "JFK", 610.0)
        add_hotel(connection, trip_id, "Canal House", "2026-11-10", "2026-11-14", 720.0)
        add_activity(connection, trip_id, "2026-11-11", "Rijksmuseum", 25.0)
        add_activity(connection, trip_id, "2026-11-12", "Canal cruise", 18.0)
        text, total = itinerary(connection, trip_id)
        print(text)
        connection.close()

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", default="travel.db")
    parser.add_argument("--trip", nargs=4, metavar=("NAME", "START", "END", "BUDGET"))
    parser.add_argument("--show", type=int)
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()
    if args.demo:
        demo(); return
    connection = connect(args.db)
    try:
        if args.trip:
            print("trip id", add_trip(connection, args.trip[0], args.trip[1], args.trip[2], float(args.trip[3])))
        if args.show:
            text, _ = itinerary(connection, args.show)
            print(text)
        elif not args.trip:
            for row in connection.execute("SELECT id,name,start_date,end_date,budget FROM trips").fetchall():
                print(row)
    finally:
        connection.close()

if __name__ == "__main__":
    main()
