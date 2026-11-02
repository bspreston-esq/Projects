#!/usr/bin/env python3
"""Store, search and display code snippets in SQLite."""
import argparse
import datetime as dt
import os
import re
import sqlite3
import tempfile

SCHEMA = """CREATE TABLE IF NOT EXISTS snippets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    language TEXT NOT NULL,
    tags TEXT NOT NULL,
    code TEXT NOT NULL,
    created TEXT NOT NULL
)"""

KEYWORDS = {
    "python": r"\b(def|class|import|from|return|if|elif|else|for|while|try|except|with|as|None|True|False|lambda|yield)\b",
    "sql": r"\b(SELECT|FROM|WHERE|JOIN|GROUP BY|ORDER BY|INSERT|UPDATE|DELETE|CREATE|TABLE)\b",
    "javascript": r"\b(const|let|var|function|return|if|else|for|while|async|await|=>)\b",
}
COLOURS = {"keyword": "\033[35m", "string": "\033[32m", "comment": "\033[90m", "reset": "\033[0m"}

class SnippetManager:
    def __init__(self, path="snippets.db"):
        self.connection = sqlite3.connect(path)
        self.connection.execute(SCHEMA)
        self.connection.commit()

    def add(self, title, language, tags, code) -> int:
        if not title.strip() or not code.strip():
            raise ValueError("title and code are required")
        cursor = self.connection.execute(
            "INSERT INTO snippets (title,language,tags,code,created) VALUES (?,?,?,?,?)",
            (title.strip(), language.strip().lower(), ",".join(t.strip() for t in tags.split(",") if t.strip()),
             code, dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")))
        self.connection.commit()
        return cursor.lastrowid

    def search(self, query="", language=None, tag=None):
        sql = "SELECT id,title,language,tags FROM snippets WHERE 1=1"
        params = []
        if query:
            sql += " AND (title LIKE ? OR code LIKE ? OR tags LIKE ?)"
            params += [f"%{query}%"] * 3
        if language:
            sql += " AND language=?"; params.append(language.lower())
        if tag:
            sql += " AND tags LIKE ?"; params.append(f"%{tag}%")
        return self.connection.execute(sql + " ORDER BY id DESC", params).fetchall()

    def get(self, snippet_id):
        row = self.connection.execute(
            "SELECT id,title,language,tags,code FROM snippets WHERE id=?", (snippet_id,)).fetchone()
        if not row:
            raise ValueError(f"no snippet {snippet_id}")
        return row

    def close(self):
        self.connection.close()

def highlight(code: str, language: str) -> str:
    pattern = KEYWORDS.get(language)
    if not pattern:
        return code
    highlighted = re.sub(r'(".*?"|\'.*?\')', COLOURS["string"] + r"\1" + COLOURS["reset"], code)
    highlighted = re.sub(pattern, lambda m: COLOURS["keyword"] + m.group(0) + COLOURS["reset"], highlighted, flags=re.MULTILINE)
    highlighted = re.sub(r"(#.*$)", COLOURS["comment"] + r"\1" + COLOURS["reset"], highlighted, flags=re.MULTILINE)
    return highlighted

def demo() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        manager = SnippetManager(os.path.join(tmp, "snippets.db"))
        manager.add("Read a file", "python", "files,io",
                    "with open('data.txt') as fh:\n    print(fh.read())")
        manager.add("Top customers", "sql", "sqlite,reporting",
                    "SELECT name, SUM(total) AS spend\nFROM orders\nGROUP BY name\nORDER BY spend DESC;")
        manager.add("Debounce", "javascript", "events,ui",
                    "const debounce = (fn, ms) => {\n  let timer;\n  return (...args) => {\n    clearTimeout(timer);\n    timer = setTimeout(() => fn(...args), ms);\n  };\n};")
        print("stored:", len(manager.search()))
        print("python snippets:", [row[1] for row in manager.search(language="python")])
        print("tagged reporting:", [row[1] for row in manager.search(tag="reporting")])
        snippet = manager.get(2)
        print(f"#{snippet[0]} {snippet[1]} [{snippet[2]}] tags={snippet[3]}")
        print(highlight(snippet[4], snippet[2]))
        manager.close()

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", default="snippets.db")
    parser.add_argument("--add", nargs=4, metavar=("TITLE", "LANGUAGE", "TAGS", "CODE"))
    parser.add_argument("--search", default="")
    parser.add_argument("--language")
    parser.add_argument("--tag")
    parser.add_argument("--show", type=int)
    parser.add_argument("--color", action="store_true")
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()
    if args.demo:
        demo(); return
    manager = SnippetManager(args.db)
    try:
        if args.add:
            print("added snippet", manager.add(*args.add))
        if args.show is not None:
            ident, title, language, tags, code = manager.get(args.show)
            print(f"#{ident} {title} [{language}] tags={tags}\n")
            print(highlight(code, language) if args.color else code)
        elif args.add is None:
            for row in manager.search(args.search, args.language, args.tag):
                print(f"#{row[0]:<3} {row[1]:<28} {row[2]:<12} {row[3]}")
    finally:
        manager.close()

if __name__ == "__main__":
    main()
