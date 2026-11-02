# Guestbook / Journal

**Category:** Text

## Problem

A simple application that allows people to add comments or write journal entries. It can allow comments or not and timestamps for all entries. Could also be made into a shout box. Optional: Deploy it on Google App Engine or Heroku or any other PaaS (if possible, of course).

## Solution

A SQLite-backed journal with an entries table (author, message, UTC timestamp). Commands add entries, list the newest first, and search author or message text with `LIKE`. The demo uses a throwaway database.

## How to run

Requires Python 3.8+ and no third-party packages.

```bash
python3 main.py --add Ada "First note"
python3 main.py --list
python3 main.py --search debugging
python3 main.py --demo
```

## Example

```text
[3] <timestamp> Alan: A guestbook entry with a timestamp.
[2] <timestamp> Grace: Debugging is twice as hard as writing the code.
[1] <timestamp> Ada: First note in the journal.
search 'hard':
[2] <timestamp> Grace: Debugging is twice as hard as writing the code.
```
