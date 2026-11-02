#!/usr/bin/env python3
"""A guestbook/journal backed by SQLite, with timestamps and search."""
import argparse
import datetime as dt
import os
import sqlite3
import tempfile

SCHEMA = """CREATE TABLE IF NOT EXISTS entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    author TEXT NOT NULL,
    message TEXT NOT NULL,
    created_at TEXT NOT NULL
)"""

class Journal:
    def __init__(self, path="journal.db"):
        self.path = path
        self.connection = sqlite3.connect(path)
        self.connection.execute(SCHEMA)
        self.connection.commit()

    def add(self, author: str, message: str) -> int:
        if not author.strip() or not message.strip():
            raise ValueError("author and message cannot be empty")
        cursor = self.connection.execute(
            "INSERT INTO entries (author, message, created_at) VALUES (?, ?, ?)",
            (author.strip(), message.strip(), dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")))
        self.connection.commit()
        return cursor.lastrowid

    def list(self, limit=20):
        return self.connection.execute(
            "SELECT id, author, message, created_at FROM entries ORDER BY id DESC LIMIT ?",
            (limit,)).fetchall()

    def search(self, query: str):
        like = f"%{query}%"
        return self.connection.execute(
            "SELECT id, author, message, created_at FROM entries "
            "WHERE message LIKE ? OR author LIKE ? ORDER BY id DESC", (like, like)).fetchall()

    def close(self):
        self.connection.close()

def show(rows):
    if not rows:
        print("(no entries)")
    for ident, author, message, created in rows:
        print(f"[{ident}] {created} {author}: {message}")

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", default="journal.db")
    parser.add_argument("--add", nargs=2, metavar=("AUTHOR", "MESSAGE"))
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--search")
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()

    if args.demo:
        with tempfile.TemporaryDirectory() as tmp:
            journal = Journal(os.path.join(tmp, "demo.db"))
            journal.add("Ada", "First note in the journal.")
            journal.add("Grace", "Debugging is twice as hard as writing the code.")
            journal.add("Alan", "A guestbook entry with a timestamp.")
            show(journal.list())
            print("search 'hard':")
            show(journal.search("hard"))
            journal.close()
        return

    journal = Journal(args.db)
    try:
        if args.add:
            new_id = journal.add(*args.add)
            print(f"added entry {new_id}")
        if args.search:
            show(journal.search(args.search))
        elif args.list or not args.add:
            show(journal.list())
    finally:
        journal.close()

if __name__ == "__main__":
    main()
