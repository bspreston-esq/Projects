# Port Scanner

**Category:** Networking

## Problem

Enter an IP address and a port range where the program will then attempt to find open ports on the given computer by connecting to each of them. On any successful connections mark the port as open.

## Solution

Uses non-blocking-style `connect_ex` probes with a short timeout, dispatched through a bounded `ThreadPoolExecutor` so a full range scans quickly without exhausting file descriptors. Results are sorted and printed as a single list.

## How to run

Requires Python 3.8+ and no third-party packages.

```bash
python3 main.py --host 127.0.0.1 --start 1 --end 1024
python3 main.py --host 192.168.1.10 --start 20 --end 25 --timeout 0.5
python3 main.py --demo
```

## Example

```text
listening on 127.0.0.1:41337
open ports in 41335-41339: [41337]
detected the listener: True
```
