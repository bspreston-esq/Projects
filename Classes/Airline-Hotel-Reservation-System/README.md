# Airline / Hotel Reservation System

**Category:** Classes

## Problem

Create a reservation system which books airline seats or hotel rooms. It charges various rates for particular sections of the plane or hotel. Example, first class is going to cost more than coach. Hotel rooms have penthouse suites which cost more. Keep track of when rooms will be available and can be scheduled.

## Solution

Models rooms with tiers (standard $120, deluxe $200, penthouse $500) and reservations with check-in, nights and computed check-out. Availability is a date-overlap test against existing bookings, so double-booking is impossible; bookings carry a confirmation code and can be cancelled.

## How to run

Requires Python 3.8+ and no third-party packages.

```bash
python3 main.py --demo
```

## Example

```text
CNF-1001: Ada Lovelace in room 101 (standard) 2026-12-20 -> 2026-12-23, $360.00
CNF-1002: Grace Hopper in room 900 (penthouse) 2026-12-20 -> 2026-12-22, $1,000.00
standard rooms free on 2026-12-21: ['201', '301']
after cancelling CNF-1001: revenue $1,000.00
```
