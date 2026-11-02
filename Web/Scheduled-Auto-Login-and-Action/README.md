# Scheduled Auto Login and Action

**Category:** Web

## Problem

Make an application which logs into a given site on a schedule and invokes a certain action and then logs out. This can be useful for checking web mail, posting regular content, or getting info for other applications and saving it to your computer.

## Solution

`SiteSession` wraps urllib with an `http.cookiejar` so the session cookie persists across requests; it posts the login form, runs the action, and can repeat on a minute interval. Passwords come from an environment variable or a prompt, never from the command line. The demo runs a loopback site with a protected dashboard.

## How to run

Requires Python 3.8+ and no third-party packages.

```bash
SITE_PASSWORD=secret python3 main.py --login-url https://example.com/login --user me \
  --action-url https://example.com/action --interval 30 --count 4
python3 main.py --demo
```

## Example

```text
dashboard reached: True
action: count=1
action: count=2
sessions issued: 1
```
