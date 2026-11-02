#!/usr/bin/env python3
"""Abstract Account with Checking, Savings and Business subclasses, plus an ATM."""
import argparse
from abc import ABC, abstractmethod

class Account(ABC):
    def __init__(self, number: str, owner: str, balance: float = 0.0):
        self.number = number
        self.owner = owner
        self.balance = balance

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("deposit must be positive")
        self.balance += amount

    @abstractmethod
    def withdraw(self, amount: float) -> float:
        """Withdraw and return the amount actually debited (including fees)."""

    def __str__(self):
        return f"{self.number:<8} {type(self).__name__:<16} {self.owner:<12} ${self.balance:>12,.2f}"

class CheckingAccount(Account):
    OVERDRAFT_LIMIT = 500.0
    OVERDRAFT_FEE = 35.0

    def withdraw(self, amount: float) -> float:
        if amount <= 0:
            raise ValueError("withdrawal must be positive")
        if self.balance - amount < -self.OVERDRAFT_LIMIT:
            raise ValueError("overdraft limit exceeded")
        fee = self.OVERDRAFT_FEE if amount > self.balance else 0.0
        self.balance -= amount + fee
        return amount + fee

class SavingsAccount(Account):
    MINIMUM = 100.0
    RATE = 0.02

    def withdraw(self, amount: float) -> float:
        if amount <= 0:
            raise ValueError("withdrawal must be positive")
        if self.balance - amount < self.MINIMUM:
            raise ValueError(f"savings must keep at least ${self.MINIMUM:.2f}")
        self.balance -= amount
        return amount

    def apply_interest(self) -> float:
        interest = self.balance * self.RATE
        self.balance += interest
        return interest

class BusinessAccount(Account):
    WITHDRAWAL_FEE = 2.50

    def withdraw(self, amount: float) -> float:
        if amount <= 0:
            raise ValueError("withdrawal must be positive")
        if amount + self.WITHDRAWAL_FEE > self.balance:
            raise ValueError("insufficient funds")
        self.balance -= amount + self.WITHDRAWAL_FEE
        return amount + self.WITHDRAWAL_FEE

class ATM:
    def __init__(self):
        self.accounts = {}

    def open(self, account: Account) -> None:
        if account.number in self.accounts:
            raise ValueError("account number already exists")
        self.accounts[account.number] = account

    def get(self, number: str) -> Account:
        if number not in self.accounts:
            raise ValueError(f"unknown account {number}")
        return self.accounts[number]

    def transfer(self, source: str, target: str, amount: float) -> None:
        self.get(source).withdraw(amount)
        self.get(target).deposit(amount)

    def statement(self) -> str:
        return "\n".join(str(account) for account in sorted(self.accounts.values(), key=lambda a: a.number))

def demo() -> None:
    atm = ATM()
    atm.open(CheckingAccount("C-1001", "Ada", 800.0))
    atm.open(SavingsAccount("S-2001", "Grace", 5000.0))
    atm.open(BusinessAccount("B-3001", "Initech", 12000.0))
    print(atm.statement())
    print(f"checking withdraw 900 -> debited ${atm.get('C-1001').withdraw(900):,.2f}")
    print(f"savings interest -> ${atm.get('S-2001').apply_interest():,.2f}")
    atm.transfer("B-3001", "C-1001", 100)
    print(atm.statement())

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--demo", action="store_true")
    parser.parse_args()
    demo()

if __name__ == "__main__":
    main()
