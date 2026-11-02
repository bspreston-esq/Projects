#!/usr/bin/env python3
"""Get true time from an NTP server, with an HTTP fallback."""
import argparse
import datetime as dt
import json
import socket
import struct
import time
import urllib.request

NTP_EPOCH = dt.datetime(1900, 1, 1, tzinfo=dt.timezone.utc)
NTP_DELTA = 2208988800  # seconds between 1900 and 1970

def build_request() -> bytes:
    """48-byte NTP client packet, version 4, mode 3 (client)."""
    return b"\x1b" + b"\x00" * 47

def parse_response(data: bytes) -> dt.datetime:
    """Extract the transmit timestamp (bytes 40-47) from an NTP packet."""
    if len(data) < 48:
        raise ValueError("short NTP response")
    seconds, fraction = struct.unpack("!II", data[40:48])
    if seconds == 0:
        raise ValueError("server returned a zero timestamp")
    return NTP_EPOCH + dt.timedelta(seconds=seconds, microseconds=fraction * 1e6 / 2**32)

def ntp_time(server: str = "pool.ntp.org", timeout: float = 5.0) -> dt.datetime:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.settimeout(timeout)
        sock.sendto(build_request(), (server, 123))
        data, _ = sock.recvfrom(512)
    return parse_response(data)

def http_time(url: str = "https://worldtimeapi.org/api/timezone/Etc/UTC") -> dt.datetime:
    request = urllib.request.Request(url, headers={"User-Agent": "atomic-time/1.0"})
    with urllib.request.urlopen(request, timeout=10) as response:
        data = json.load(response)
    return dt.datetime.fromisoformat(data["utc_datetime"]).astimezone(dt.timezone.utc)

def demo() -> None:
    sample = dt.datetime(2026, 11, 2, 12, 34, 56, 500000, tzinfo=dt.timezone.utc)
    seconds = int((sample - NTP_EPOCH).total_seconds())
    fraction = int((sample.microsecond / 1e6) * 2**32)
    packet = b"\x00" * 40 + struct.pack("!II", seconds, fraction)
    parsed = parse_response(packet)
    print("synthetic NTP packet ->", parsed.isoformat())
    print("matches expected:", parsed.replace(microsecond=0) == sample.replace(microsecond=0))
    local = dt.datetime.now(dt.timezone.utc)
    print(f"system clock (UTC): {local.isoformat(timespec='seconds')}")

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--server", default="pool.ntp.org")
    parser.add_argument("--http", action="store_true", help="use the HTTP fallback instead of NTP")
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()
    if args.demo:
        demo(); return
    try:
        network = http_time() if args.http else ntp_time(args.server)
    except (OSError, ValueError, KeyError) as exc:
        raise SystemExit(f"time lookup failed: {exc}")
    local = dt.datetime.now(dt.timezone.utc)
    print("network time:", network.isoformat(timespec="seconds"))
    print("system time: ", local.isoformat(timespec="seconds"))
    print(f"offset: {network - local}")

if __name__ == "__main__":
    main()
