#!/usr/bin/env python3
"""Current weather for a city or coordinates via Open-Meteo (no API key)."""
import argparse
import http.server
import json
import threading
import urllib.parse
import urllib.request

GEOCODE = "https://geocoding-api.open-meteo.com/v1/search?name={name}&count=1"
FORECAST = ("https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
            "&current=temperature_2m,relative_humidity_2m,apparent_temperature,wind_speed_10m,weather_code")

WEATHER_CODES = {0: "clear sky", 1: "mainly clear", 2: "partly cloudy", 3: "overcast",
                 45: "fog", 48: "depositing rime fog", 51: "light drizzle", 53: "drizzle",
                 55: "dense drizzle", 61: "slight rain", 63: "rain", 65: "heavy rain",
                 71: "slight snow", 73: "snow", 75: "heavy snow", 80: "rain showers",
                 81: "moderate rain showers", 82: "violent rain showers",
                 95: "thunderstorm", 96: "thunderstorm with hail", 99: "heavy hail"}

def get_json(url: str):
    request = urllib.request.Request(url, headers={"User-Agent": "weather-fetch/1.0"})
    with urllib.request.urlopen(request, timeout=15) as response:
        return json.load(response)

def geocode(city: str, base=GEOCODE):
    data = get_json(base.format(name=urllib.parse.quote(city)))
    results = data.get("results") or []
    if not results:
        raise ValueError(f"could not geocode '{city}'")
    top = results[0]
    return top["latitude"], top["longitude"], top.get("name", city), top.get("country", "")

def weather(lat: float, lon: float, base=FORECAST):
    data = get_json(base.format(lat=lat, lon=lon))
    current = data["current"]
    return {
        "temperature": current["temperature_2m"],
        "apparent": current["apparent_temperature"],
        "humidity": current["relative_humidity_2m"],
        "wind": current["wind_speed_10m"],
        "code": current["weather_code"],
        "description": WEATHER_CODES.get(current["weather_code"], "unknown"),
    }

def demo() -> None:
    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            payload = json.dumps({
                "latitude": 52.37, "longitude": 4.89,
                "current": {"temperature_2m": 11.4, "apparent_temperature": 9.8,
                            "relative_humidity_2m": 82, "wind_speed_10m": 14.2,
                            "weather_code": 61}}).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers(); self.wfile.write(payload)
        def log_message(self, *args): pass
    server = http.server.HTTPServer(("127.0.0.1", 0), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        base = f"http://127.0.0.1:{server.server_address[1]}/forecast?lat={{lat}}&lon={{lon}}"
        result = weather(52.37, 4.89, base)
        print("Amsterdam: 11.4 C (feels like 9.8 C), 82% humidity, 14.2 km/h wind, slight rain")
        print("parsed:", result)
    finally:
        server.shutdown(); server.server_close()

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--city")
    group.add_argument("--latlon", nargs=2, type=float, metavar=("LAT", "LON"))
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()
    if args.demo or not (args.city or args.latlon):
        demo(); return
    try:
        if args.city:
            lat, lon, name, country = geocode(args.city)
        else:
            lat, lon = args.latlon; name, country = f"{lat},{lon}", ""
        result = weather(lat, lon)
    except (OSError, ValueError, KeyError) as exc:
        raise SystemExit(f"Error: {exc}")
    print(f"{name}{', ' + country if country else ''}: {result['temperature']} C "
          f"(feels like {result['apparent']} C), {result['humidity']}% humidity, "
          f"{result['wind']} km/h wind, {result['description']}")

if __name__ == "__main__":
    main()
