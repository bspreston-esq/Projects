#!/usr/bin/env python3
"""Look up the country (and city/ISP) registered to an IP address."""
import argparse
import http.server
import ipaddress
import json
import threading
import urllib.request

API = "http://ip-api.com/json/{ip}?fields=status,country,countryCode,regionName,city,isp,query"

def lookup(ip: str, base: str = API):
    """Return a dict of location data for `ip`; raises ValueError on failure."""
    address = ipaddress.ip_address(ip)
    if address.is_private or address.is_loopback:
        return {"query": ip, "country": "Private network", "countryCode": "--",
                "regionName": "", "city": "", "isp": "non-routable", "status": "success"}
    request = urllib.request.Request(base.format(ip=ip), headers={"User-Agent": "ip-lookup/1.0"})
    with urllib.request.urlopen(request, timeout=10) as response:
        data = json.load(response)
    if data.get("status") != "success":
        raise ValueError(data.get("message", "lookup failed"))
    return data

def demo() -> None:
    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            payload = json.dumps({"status": "success", "country": "Netherlands",
                                  "countryCode": "NL", "regionName": "North Holland",
                                  "city": "Amsterdam", "isp": "Example ISP",
                                  "query": "93.184.216.34"}).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
        def log_message(self, *args):
            pass

    server = http.server.HTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        base = f"http://127.0.0.1:{server.server_address[1]}/json/{{ip}}?fields=all"
        result = lookup("93.184.216.34", base)
        print(f"{result['query']}: {result['city']}, {result['regionName']}, {result['country']} "
              f"({result['countryCode']}) via {result['isp']}")
        print("192.168.1.10:", lookup("192.168.1.10")["country"])
    finally:
        server.shutdown()
        server.server_close()

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ip", nargs="?")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()

    if args.demo:
        demo()
        return
    ip = args.ip or input("IP address: ").strip()
    try:
        result = lookup(ip)
    except (ValueError, OSError) as exc:
        raise SystemExit(f"Error: {exc}")
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"{result.get('query', ip)}: {result.get('city') or '-'}, "
              f"{result.get('regionName') or '-'}, {result.get('country')} "
              f"({result.get('countryCode')}) via {result.get('isp') or '-'}")

if __name__ == "__main__":
    main()
