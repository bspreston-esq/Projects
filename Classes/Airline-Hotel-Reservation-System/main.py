#!/usr/bin/env python3
"""Hotel reservation system with room tiers, availability and overlap checks."""
import argparse
import datetime as dt
from dataclasses import dataclass, field

TIERS = {"standard": 120.0, "deluxe": 200.0, "penthouse": 500.0}

@dataclass
class Room:
    number: str
    tier: str

    def __post_init__(self):
        if self.tier not in TIERS:
            raise ValueError(f"unknown tier '{self.tier}'")
        self.rate = TIERS[self.tier]

@dataclass
class Reservation:
    guest: str
    room: Room
    check_in: dt.date
    nights: int
    confirmation: str = ""

    @property
    def check_out(self) -> dt.date:
        return self.check_in + dt.timedelta(days=self.nights)

    def overlaps(self, start: dt.date, nights: int) -> bool:
        end = start + dt.timedelta(days=nights)
        return self.check_in < end and start < self.check_out

    @property
    def total(self) -> float:
        return self.room.rate * self.nights

class Hotel:
    def __init__(self, name: str):
        self.name = name
        self.rooms = {}
        self.reservations = []
        self._counter = 1000

    def add_room(self, room: Room) -> None:
        if room.number in self.rooms:
            raise ValueError(f"room {room.number} already exists")
        self.rooms[room.number] = room

    def available(self, tier: str, start: dt.date, nights: int):
        return [room for room in self.rooms.values()
                if room.tier == tier and not any(
                    r.room is room and r.overlaps(start, nights) for r in self.reservations)]

    def book(self, guest: str, tier: str, start: dt.date, nights: int) -> Reservation:
        if nights <= 0:
            raise ValueError("nights must be positive")
        rooms = self.available(tier, start, nights)
        if not rooms:
            raise ValueError(f"no {tier} rooms available for those dates")
        room = sorted(rooms, key=lambda r: r.number)[0]
        self._counter += 1
        reservation = Reservation(guest, room, start, nights, f"CNF-{self._counter}")
        self.reservations.append(reservation)
        return reservation

    def cancel(self, confirmation: str) -> Reservation:
        for reservation in self.reservations:
            if reservation.confirmation == confirmation:
                self.reservations.remove(reservation)
                return reservation
        raise ValueError(f"unknown confirmation '{confirmation}'")

    def revenue(self) -> float:
        return sum(r.total for r in self.reservations)

def demo() -> None:
    hotel = Hotel("Grand Demo")
    for floor in range(1, 4):
        hotel.add_room(Room(f"{floor}01", "standard"))
        hotel.add_room(Room(f"{floor}02", "deluxe"))
    hotel.add_room(Room("900", "penthouse"))
    start = dt.date(2026, 12, 20)
    first = hotel.book("Ada Lovelace", "standard", start, 3)
    second = hotel.book("Grace Hopper", "penthouse", start, 2)
    print(f"{first.confirmation}: {first.guest} in room {first.room.number} "
          f"({first.room.tier}) {first.check_in} -> {first.check_out}, ${first.total:,.2f}")
    print(f"{second.confirmation}: {second.guest} in room {second.room.number} "
          f"({second.room.tier}) {second.check_in} -> {second.check_out}, ${second.total:,.2f}")
    print("standard rooms free on 2026-12-21:",
          [room.number for room in hotel.available("standard", dt.date(2026, 12, 21), 1)])
    hotel.cancel(first.confirmation)
    print(f"after cancelling {first.confirmation}: revenue ${hotel.revenue():,.2f}")

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()
    if args.demo or True:
        demo()

if __name__ == "__main__":
    main()
