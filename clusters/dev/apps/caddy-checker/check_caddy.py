import json
import os
import sys
import time
from datetime import datetime, timezone
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

CHECK_URL = os.getenv("CHECK_URL", "http://caddy.apps.svc.cluster.local")
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "30"))
TIMEOUT = int(os.getenv("TIMEOUT", "5"))


def log(level: str, msg: str, **extra):
    record = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "level": level,
        "app": "caddy-checker",
        "msg": msg,
        "check_url": CHECK_URL,
        **extra,
    }
    print(json.dumps(record), flush=True)


def check():
    req = Request(CHECK_URL, headers={"User-Agent": "caddy-checker/1.0"})
    start = time.time()
    try:
        with urlopen(req, timeout=TIMEOUT) as resp:
            duration_ms = round((time.time() - start) * 1000, 2)
            status = resp.getcode()
            if 200 <= status < 400:
                log("INFO", "Caddy is healthy", status=status, duration_ms=duration_ms)
            else:
                log("ERROR", "Caddy returned bad status", status=status, duration_ms=duration_ms)
    except HTTPError as e:
        duration_ms = round((time.time() - start) * 1000, 2)
        log("ERROR", "HTTP error while checking Caddy", status=e.code, duration_ms=duration_ms)
    except URLError as e:
        duration_ms = round((time.time() - start) * 1000, 2)
        log("ERROR", "Connection error while checking Caddy", error=str(e.reason), duration_ms=duration_ms)
    except Exception as e:
        duration_ms = round((time.time() - start) * 1000, 2)
        log("ERROR", "Unexpected error while checking Caddy", error=str(e), duration_ms=duration_ms)


def main():
    log("INFO", "Caddy checker started")
    while True:
        check()
        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log("INFO", "Caddy checker stopped")
        sys.exit(0)
