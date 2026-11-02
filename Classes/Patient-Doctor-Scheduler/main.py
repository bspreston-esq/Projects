#!/usr/bin/env python3
"""Doctor/patient scheduling with 16 half-hour slots in an 8-hour day."""
import argparse
import datetime as dt

START = dt.time(9, 0)
SLOT_MINUTES = 30
SLOTS_PER_DAY = 16

def day_slots(day: dt.date):
    return [dt.datetime.combine(day, START) + dt.timedelta(minutes=SLOT_MINUTES * i)
            for i in range(SLOTS_PER_DAY)]

class Patient:
    def __init__(self, patient_id: str, name: str, phone: str = ""):
        self.patient_id = patient_id
        self.name = name
        self.phone = phone

    def __str__(self):
        return f"{self.patient_id} ({self.name})"

class Doctor:
    def __init__(self, name: str, specialty: str):
        self.name = name
        self.specialty = specialty
        self.schedule = {}

    def book(self, patient: Patient, when: dt.datetime) -> None:
        if when.date() != when.date() or when.time() not in [s.time() for s in day_slots(when.date())]:
            raise ValueError("appointments must be on the hour or half hour between 09:00 and 16:30")
        booked = self.schedule.setdefault(when.date(), {})
        if when.time() in booked:
            raise ValueError(f"{when:%Y-%m-%d %H:%M} is already taken")
        if len(booked) >= SLOTS_PER_DAY:
            raise ValueError("doctor is fully booked that day (16 patients)")
        booked[when.time()] = patient

    def cancel(self, when: dt.datetime) -> Patient:
        try:
            return self.schedule[when.date()].pop(when.time())
        except KeyError:
            raise ValueError(f"no appointment at {when:%Y-%m-%d %H:%M}")

    def day(self, day: dt.date):
        return sorted(self.schedule.get(day, {}).items())

class Scheduler:
    def __init__(self):
        self.doctors = []

    def add_doctor(self, doctor: Doctor) -> None:
        self.doctors.append(doctor)

    def book(self, doctor: Doctor, patient: Patient, when: dt.datetime) -> None:
        doctor.book(patient, when)

    def report(self, doctor: Doctor, day: dt.date) -> str:
        lines = [f"{doctor.name} ({doctor.specialty}) on {day}: {len(doctor.schedule.get(day, {}))}/{SLOTS_PER_DAY} slots"]
        for slot, patient in doctor.day(day):
            lines.append(f"  {slot:%H:%M}  {patient.name}")
        return "\n".join(lines)

def demo() -> None:
    scheduler = Scheduler()
    doctor = Doctor("Dr. Chen", "Cardiology")
    scheduler.add_doctor(doctor)
    day = dt.date(2026, 11, 3)
    patients = [Patient(f"P{i:03d}", name) for i, name in enumerate(
        ["Ada Lovelace", "Grace Hopper", "Alan Turing", "Katherine Johnson"], 1)]
    for patient, slot in zip(patients, [dt.time(9, 0), dt.time(9, 30), dt.time(11, 0), dt.time(14, 30)]):
        scheduler.book(doctor, patient, dt.datetime.combine(day, slot))
    print(scheduler.report(doctor, day))
    try:
        scheduler.book(doctor, Patient("P999", "Double Booked"), dt.datetime.combine(day, dt.time(9, 0)))
    except ValueError as exc:
        print("conflict:", exc)
    doctor.cancel(dt.datetime.combine(day, dt.time(9, 30)))
    print("after cancellation:", len(doctor.schedule[day]), "appointments")

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--demo", action="store_true")
    parser.parse_args()
    demo()

if __name__ == "__main__":
    main()
