# Travel Planner System

**Category:** Databases

## Problem

Make a system that allows users to put together their own little travel itinerary and keep track of the airline / hotel arrangements, points of interest, budget and schedule.

## Solution

Four SQLite tables (trips, flights, hotels, activities) are joined into a day-by-day itinerary: flights sorted by departure, hotel stays by check-in, and activities grouped under their date. Totals are compared against the trip budget to show what remains.

## How to run

Requires Python 3.8+ and no third-party packages.

```bash
python3 main.py --db travel.db --trip Amsterdam 2026-11-10 2026-11-14 2200
python3 main.py --db travel.db --show 1
python3 main.py --demo
```

## Example

```text
Amsterdam: 2026-11-10 to 2026-11-14 (5 days, budget $2,200.00)
Flights:
  2026-11-10 13:20 KLM KL642 JFK->AMS  $640.00
Hotels:
  Canal House 2026-11-10 to 2026-11-14  $720.00
Planned cost: $2,013.00 | remaining: $187.00
```
