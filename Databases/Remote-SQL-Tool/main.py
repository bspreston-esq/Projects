#!/usr/bin/env python3
"""Execute SQL against a remote SQLite server over a small JSON/TCP protocol."""
import argparse
import json
import os
import socketserver
import sqlite3
import threading
import time

MAX_REQUEST = 1_000_000

class SQLRequestHandler(socketserver.StreamRequestHandler):
    def handle(self):
        line = self.rfile.readline(MAX_REQUEST)
        if not line:
            return
        try:
            request = json.loads(line)
        except json.JSONDecodeError:
            self.wfile.write(json.dumps({"ok": False, "error": "invalid JSON"}).encode() + b"\n"); return
        if request.get("token") != self.server.token:
            self.wfile.write(json.dumps({"ok": False, "error": "unauthorized"}).encode() + b"\n"); return
        try:
            connection = sqlite3.connect(self.server.db_path)
            cursor = connection.execute(request.get("sql", ""))
            if cursor.description:
                columns = [column[0] for column in cursor.description]
                rows = cursor.fetchall()
                payload = {"ok": True, "columns": columns, "rows": rows}
            else:
                connection.commit()
                payload = {"ok": True, "columns": [], "rows": [], "rowcount": cursor.rowcount}
            connection.close()
        except sqlite3.Error as exc:
            payload = {"ok": False, "error": str(exc)}
        self.wfile.write(json.dumps(payload).encode() + b"\n")

class SQLServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True

    def __init__(self, address, db_path, token):
        super().__init__(address, SQLRequestHandler)
        self.db_path = db_path
        self.token = token

def run_query(host: str, port: int, token: str, sql: str, timeout=10):
    import socket
    with socket.create_connection((host, port), timeout=timeout) as connection:
        connection.sendall(json.dumps({"token": token, "sql": sql}).encode() + b"\n")
        buffer = b""
        while not buffer.endswith(b"\n"):
            chunk = connection.recv(65536)
            if not chunk:
                break
            buffer += chunk
    return json.loads(buffer or b"{}")

def demo() -> None:
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        db_path = os.path.join(tmp, "remote.db")
        connection = sqlite3.connect(db_path)
        connection.executescript("CREATE TABLE items (id INTEGER PRIMARY KEY, name TEXT, qty INTEGER);"
                                 "INSERT INTO items (name,qty) VALUES ('bolt',40),('nut',75),('washer',12);")
        connection.commit(); connection.close()
        server = SQLServer(("127.0.0.1", 0), db_path, "demo-token")
        threading.Thread(target=server.serve_forever, daemon=True).start()
        try:
            port = server.server_address[1]
            result = run_query("127.0.0.1", port, "demo-token", "SELECT name, qty FROM items ORDER BY qty DESC")
            print("columns:", result["columns"])
            for row in result["rows"]:
                print(" ", row)
            denied = run_query("127.0.0.1", port, "wrong", "SELECT 1")
            print("bad token:", denied.get("error"))
            run_query("127.0.0.1", port, "demo-token", "UPDATE items SET qty = qty + 1 WHERE name = 'nut'")
            print("after update:", run_query("127.0.0.1", port, "demo-token", "SELECT qty FROM items WHERE name='nut'")["rows"])
        finally:
            server.shutdown(); server.server_close()

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=False)
    serve = sub.add_parser("serve")
    serve.add_argument("--db", required=True); serve.add_argument("--host", default="127.0.0.1")
    serve.add_argument("--port", type=int, default=9000); serve.add_argument("--token", default=os.environ.get("SQL_TOKEN", "change-me"))
    client = sub.add_parser("query")
    client.add_argument("--host", required=True); client.add_argument("--port", type=int, default=9000)
    client.add_argument("--token", default=os.environ.get("SQL_TOKEN", "change-me")); client.add_argument("--sql", required=True)
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()
    if args.demo:
        demo(); return
    if args.command == "serve":
        server = SQLServer((args.host, args.port), args.db, args.token)
        print(f"SQL server on {args.host}:{args.port} (db={args.db})")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            server.server_close()
    elif args.command == "query":
        result = run_query(args.host, args.port, args.token, args.sql)
        if not result.get("ok"):
            raise SystemExit("Error: " + result.get("error", "unknown error"))
        if result["columns"]:
            print(" | ".join(result["columns"]))
            for row in result["rows"]:
                print(" | ".join(str(value) for value in row))
        else:
            print(f"OK, {result.get('rowcount', 0)} rows affected")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
