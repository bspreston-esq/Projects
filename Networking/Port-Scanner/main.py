#!/usr/bin/env python3
"""Scan a host's TCP ports with a bounded thread pool."""
import argparse
import socket
from concurrent.futures import ThreadPoolExecutor

def scan_port(host: str, port: int, timeout: float = 0.3):
    """Return True when a TCP connection succeeds."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        return sock.connect_ex((host, port)) == 0

def scan(host: str, start: int, end: int, workers: int = 200, timeout: float = 0.3):
    ports = range(start, end + 1)
    with ThreadPoolExecutor(max_workers=workers) as pool:
        results = pool.map(lambda port: (port, scan_port(host, port, timeout)), ports)
        return sorted(port for port, is_open in results if is_open)

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--start", type=int, default=1)
    parser.add_argument("--end", type=int, default=1024)
    parser.add_argument("--timeout", type=float, default=0.3)
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()

    if args.demo:
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.bind(("127.0.0.1", 0))
        listener.listen(1)
        port = listener.getsockname()[1]
        try:
            found = scan("127.0.0.1", max(1, port - 2), port + 2, timeout=0.2)
            print(f"listening on 127.0.0.1:{port}")
            print(f"open ports in {max(1, port-2)}-{port+2}: {found}")
            print(f"detected the listener: {port in found}")
        finally:
            listener.close()
        return

    open_ports = scan(args.host, args.start, args.end, timeout=args.timeout)
    if not open_ports:
        print(f"no open TCP ports on {args.host} in {args.start}-{args.end}")
    else:
        print(f"open TCP ports on {args.host}: {', '.join(map(str, open_ports))}")

if __name__ == "__main__":
    main()
