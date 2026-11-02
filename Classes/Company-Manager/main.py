#!/usr/bin/env python3
"""Employee hierarchy and a Company that hires, fires and raises employees."""
import argparse
from abc import ABC, abstractmethod

class Employee(ABC):
    def __init__(self, employee_id: str, name: str):
        self.employee_id = employee_id
        self.name = name

    @abstractmethod
    def pay(self) -> float:
        """Pay for the current biweekly period."""

    def raise_pay(self, percent: float) -> None:
        if percent <= 0:
            raise ValueError("raise must be positive")
        self._apply_raise(percent)

    @abstractmethod
    def _apply_raise(self, percent: float) -> None:
        ...

    def __str__(self):
        return f"{self.employee_id:<5} {self.name:<18} {type(self).__name__:<16} ${self.pay():>10,.2f}"

class HourlyEmployee(Employee):
    def __init__(self, employee_id, name, hourly_rate, hours_worked=80):
        super().__init__(employee_id, name)
        self.hourly_rate = hourly_rate
        self.hours_worked = hours_worked

    def pay(self) -> float:
        regular = min(self.hours_worked, 80)
        overtime = max(0, self.hours_worked - 80)
        return regular * self.hourly_rate + overtime * self.hourly_rate * 1.5

    def _apply_raise(self, percent):
        self.hourly_rate *= 1 + percent / 100

class SalariedEmployee(Employee):
    def __init__(self, employee_id, name, annual_salary):
        super().__init__(employee_id, name)
        self.annual_salary = annual_salary

    def pay(self) -> float:
        return self.annual_salary / 26

    def _apply_raise(self, percent):
        self.annual_salary *= 1 + percent / 100

class Manager(SalariedEmployee):
    def __init__(self, employee_id, name, annual_salary, bonus=0.0):
        super().__init__(employee_id, name, annual_salary)
        self.bonus = bonus

    def pay(self) -> float:
        return super().pay() + self.bonus / 26

class Executive(Manager):
    def __init__(self, employee_id, name, annual_salary, bonus=0.0, stock_options=0):
        super().__init__(employee_id, name, annual_salary, bonus)
        self.stock_options = stock_options

    def pay(self) -> float:
        return super().pay() + self.stock_options * 10 / 26

class Company:
    def __init__(self, name: str):
        self.name = name
        self.employees = {}

    def hire(self, employee: Employee) -> None:
        if employee.employee_id in self.employees:
            raise ValueError(f"employee {employee.employee_id} already hired")
        self.employees[employee.employee_id] = employee

    def fire(self, employee_id: str) -> Employee:
        if employee_id not in self.employees:
            raise ValueError(f"unknown employee {employee_id}")
        return self.employees.pop(employee_id)

    def raise_pay(self, employee_id: str, percent: float) -> None:
        employee = self.employees.get(employee_id)
        if not employee:
            raise ValueError(f"unknown employee {employee_id}")
        employee.raise_pay(percent)

    def payroll(self) -> float:
        return sum(employee.pay() for employee in self.employees.values())

    def report(self) -> str:
        lines = [f"{self.name} payroll ({len(self.employees)} employees)"]
        lines += [str(employee) for employee in sorted(self.employees.values(), key=lambda e: e.employee_id)]
        lines.append(f"{'TOTAL':<40} ${self.payroll():>10,.2f}")
        return "\n".join(lines)

def demo() -> None:
    company = Company("Initech")
    company.hire(HourlyEmployee("E001", "Ada", 25.0, hours_worked=88))
    company.hire(SalariedEmployee("E002", "Grace", 104000))
    company.hire(Manager("E003", "Alan", 130000, bonus=12000))
    company.hire(Executive("E004", "Katherine", 190000, bonus=40000, stock_options=5000))
    print(company.report())
    company.raise_pay("E002", 5)
    company.fire("E001")
    print(f"after 5% raise to E002 and firing E001: payroll ${company.payroll():,.2f}")

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--demo", action="store_true")
    parser.parse_args()
    demo()

if __name__ == "__main__":
    main()
