# Mail Checker (POP3 / IMAP)

**Category:** Networking

## Problem

The user enters various account information include web server and IP, protocol type (POP3 or IMAP) and the application will check for email at a given interval.

## Solution

Wraps `poplib` and `imaplib` with SSL-by-default connections, logs in, and reports the message count (and mailbox size for POP3). Passwords are prompted for at runtime rather than stored. The demo runs a loopback POP3 server so the POP3 path is exercised end to end.

## How to run

Requires Python 3.8+ and no third-party packages.

```bash
python3 main.py --protocol imap --host imap.example.com --user you@example.com
python3 main.py --protocol pop3 --host pop.example.com --user you --no-ssl
python3 main.py --demo
```

## Example

```text
POP3 demo at 127.0.0.1:47751: 2 messages, 133 bytes
IMAP mode is implemented for real servers (imaplib, 993/SSL by default).
```
