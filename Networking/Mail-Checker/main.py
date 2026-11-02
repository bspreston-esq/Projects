#!/usr/bin/env python3
"""Check a mailbox over POP3 or IMAP and report message counts."""
import argparse
import getpass
import imaplib
import os
import poplib
import socket
import socketserver
import threading

def check_pop3(host: str, user: str, password: str, port: int = 110, ssl: bool = False):
    client = poplib.POP3_SSL(host, port, timeout=15) if ssl else poplib.POP3(host, port, timeout=15)
    try:
        client.user(user)
        client.pass_(password)
        count, size = client.stat()
        return {"protocol": "POP3", "messages": count, "bytes": size}
    finally:
        client.quit()

def check_imap(host: str, user: str, password: str, port: int = 993, ssl: bool = True):
    client = imaplib.IMAP4_SSL(host, port, timeout=15) if ssl else imaplib.IMAP4(host, port, timeout=15)
    try:
        client.login(user, password)
        status, data = client.select("INBOX", readonly=True)
        if status != "OK":
            raise imaplib.IMAP4.error("could not select INBOX")
        return {"protocol": "IMAP", "messages": int(data[0]), "bytes": None}
    finally:
        try:
            client.logout()
        except Exception:
            pass

class MiniPOP3Server(socketserver.StreamRequestHandler):
    """Tiny POP3 server used only by --demo."""
    messages = [
        b"From: ada@example.com\r\nSubject: Demo one\r\n\r\nFirst demo message.\r\n",
        b"From: grace@example.com\r\nSubject: Demo two\r\n\r\nSecond demo message.\r\n",
    ]

    def handle(self):
        self.wfile.write(b"+OK MiniPOP3 ready\r\n")
        while True:
            line = self.rfile.readline()
            if not line:
                return
            command, _, argument = line.decode(errors="replace").strip().partition(" ")
            command = command.upper()
            if command == "USER":
                self.wfile.write(b"+OK user accepted\r\n")
            elif command == "PASS":
                self.wfile.write(b"+OK mailbox locked and ready\r\n")
            elif command == "STAT":
                total = sum(len(m) for m in self.messages)
                self.wfile.write(f"+OK {len(self.messages)} {total}\r\n".encode())
            elif command == "LIST":
                self.wfile.write(f"+OK {len(self.messages)} messages\r\n".encode())
                for index, message in enumerate(self.messages, 1):
                    self.wfile.write(f"{index} {len(message)}\r\n".encode())
                self.wfile.write(b".\r\n")
            elif command == "RETR":
                index = int(argument) - 1
                if 0 <= index < len(self.messages):
                    self.wfile.write(b"+OK message follows\r\n")
                    for line in self.messages[index].splitlines(keepends=True):
                        if line.startswith(b"."):
                            line = b"." + line
                        self.wfile.write(line.replace(b"\n", b"\r\n") if not line.endswith(b"\r\n") else line)
                    self.wfile.write(b".\r\n")
                else:
                    self.wfile.write(b"-ERR no such message\r\n")
            elif command == "QUIT":
                self.wfile.write(b"+OK bye\r\n")
                return
            else:
                self.wfile.write(b"-ERR unsupported\r\n")

def demo() -> None:
    server = socketserver.TCPServer(("127.0.0.1", 0), MiniPOP3Server)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        port = server.server_address[1]
        result = check_pop3("127.0.0.1", "demo", "demo", port=port)
        print(f"POP3 demo at 127.0.0.1:{port}: {result['messages']} messages, {result['bytes']} bytes")
        print("IMAP mode is implemented for real servers (imaplib, 993/SSL by default).")
    finally:
        server.shutdown()
        server.server_close()

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--protocol", choices=["pop3", "imap"], default="imap")
    parser.add_argument("--host")
    parser.add_argument("--port", type=int)
    parser.add_argument("--user")
    parser.add_argument("--password", help="omit to be prompted (never hard-code passwords)")
    parser.add_argument("--no-ssl", action="store_true")
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()

    if args.demo:
        demo()
        return
    if not args.host or not args.user:
        raise SystemExit("--host and --user are required (or use --demo)")
    password = args.password or getpass.getpass("Password: ")
    try:
        if args.protocol == "pop3":
            result = check_pop3(args.host, args.user, password, args.port or 110, not args.no_ssl)
        else:
            result = check_imap(args.host, args.user, password, args.port or 993, not args.no_ssl)
    except (OSError, poplib.error_proto, imaplib.IMAP4.error, socket.timeout) as exc:
        raise SystemExit(f"{args.protocol.upper()} error: {exc}")
    print(f"{result['protocol']}: {result['messages']} messages in the mailbox")
    if result["bytes"] is not None:
        print(f"mailbox size: {result['bytes']} bytes")

if __name__ == "__main__":
    main()
