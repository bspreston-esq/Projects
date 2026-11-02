#!/usr/bin/env python3
"""Log into a site on a schedule, run an action, and log out."""
import argparse
import getpass
import http.cookiejar
import http.server
import os
import threading
import time
import urllib.parse
import urllib.request

class SiteSession:
    """Cookie-preserving HTTP client with form login."""

    def __init__(self):
        self.jar = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.jar))

    def login(self, url: str, username: str, password: str) -> str:
        data = urllib.parse.urlencode({"username": username, "password": password}).encode()
        with self.opener.open(urllib.request.Request(url, data=data), timeout=15) as response:
            body = response.read().decode("utf-8", errors="replace")
            return response.geturl() if body else response.geturl()

    def get(self, url: str) -> str:
        with self.opener.open(url, timeout=15) as response:
            return response.read().decode("utf-8", errors="replace")

    def post(self, url: str, fields=None) -> str:
        data = urllib.parse.urlencode(fields or {}).encode()
        with self.opener.open(urllib.request.Request(url, data=data), timeout=15) as response:
            return response.read().decode("utf-8", errors="replace")

DEMO_PAGE = """<!doctype html><html><body>
<h1>{heading}</h1>{extra}
</body></html>"""

def demo() -> None:
    state = {"sessions": set(), "actions": 0}

    class Handler(http.server.BaseHTTPRequestHandler):
        def _html(self, body, status=200, cookie=None):
            payload = body.encode()
            self.send_response(status)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(payload)))
            if cookie:
                self.send_header("Set-Cookie", cookie)
            self.end_headers(); self.wfile.write(payload)

        def do_GET(self):
            if self.path == "/login":
                self._html(DEMO_PAGE.format(heading="Login",
                    extra='<form method="post"><input name="username"><input name="password" type="password"><button>Sign in</button></form>'))
            elif self.path == "/dashboard":
                if "session=demo-token" in (self.headers.get("Cookie") or ""):
                    self._html(DEMO_PAGE.format(heading="Dashboard", extra="<p>Welcome back.</p>"))
                else:
                    self._html(DEMO_PAGE.format(heading="Denied"), 403)
            elif self.path == "/action":
                self._html(DEMO_PAGE.format(heading="Action", extra=f"<p>count={state['actions']}</p>"))
            else:
                self._html(DEMO_PAGE.format(heading="Home"), 404)

        def do_POST(self):
            length = int(self.headers.get("Content-Length", 0))
            fields = urllib.parse.parse_qs(self.rfile.read(length).decode())
            if self.path == "/login" and fields.get("username") == ["demo"] and fields.get("password") == ["demo"]:
                state["sessions"].add("demo-token")
                self.send_response(303); self.send_header("Location", "/dashboard")
                self.send_header("Set-Cookie", "session=demo-token; HttpOnly; Path=/")
                self.end_headers()
            elif self.path == "/action":
                if "session=demo-token" in (self.headers.get("Cookie") or ""):
                    state["actions"] += 1
                    self._html(DEMO_PAGE.format(heading="Action", extra=f"<p>count={state['actions']}</p>"))
                else:
                    self._html(DEMO_PAGE.format(heading="Denied"), 403)
            else:
                self._html(DEMO_PAGE.format(heading="Not found"), 404)

        def log_message(self, *args):
            pass

    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{server.server_address[1]}"
    try:
        session = SiteSession()
        session.login(base + "/login", "demo", "demo")
        dashboard = session.get(base + "/dashboard")
        print("dashboard reached:", "Welcome back" in dashboard)
        for _ in range(2):
            print("action:", "count=" + session.post(base + "/action").split("count=")[1].split("<")[0])
        print("sessions issued:", len(state["sessions"]))
    finally:
        server.shutdown(); server.server_close()

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--login-url")
    parser.add_argument("--user")
    parser.add_argument("--password-env", default="SITE_PASSWORD")
    parser.add_argument("--action-url")
    parser.add_argument("--interval", type=float, default=0, help="minutes between runs")
    parser.add_argument("--count", type=int, default=1)
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()

    if args.demo or not args.login_url:
        demo(); return
    password = os.environ.get(args.password_env) or getpass.getpass("Password: ")
    session = SiteSession()
    for run in range(args.count):
        try:
            session.login(args.login_url, args.user, password)
            print(f"[{time.strftime('%H:%M:%S')}] logged in as {args.user}")
            if args.action_url:
                print("action response:", session.post(args.action_url)[:120].replace("\n", " "))
        except OSError as exc:
            print(f"[{time.strftime('%H:%M:%S')}] error: {exc}")
        if run + 1 < args.count:
            time.sleep(max(0.0, args.interval * 60))

if __name__ == "__main__":
    main()
