import json
import os
import sys
import time
import threading
from datetime import datetime, timezone
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from http.server import BaseHTTPRequestHandler, HTTPServer

CHECK_URL = os.getenv("CHECK_URL", "http://caddy.apps.svc.cluster.local")
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "30"))
TIMEOUT = int(os.getenv("TIMEOUT", "5"))
METRICS_PORT = int(os.getenv("METRICS_PORT", "8000"))

last_health = 0
last_status_code = 0
last_response_time_ms = 0.0
last_check_timestamp = 0


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
    global last_health, last_status_code, last_response_time_ms, last_check_timestamp

    req = Request(CHECK_URL, headers={"User-Agent": "caddy-checker/2.0"})
    start = time.time()
    last_check_timestamp = int(time.time())

    try:
        with urlopen(req, timeout=TIMEOUT) as resp:
            duration_ms = round((time.time() - start) * 1000, 2)
            status = resp.getcode()

            last_status_code = status
            last_response_time_ms = duration_ms
            last_health = 1 if 200 <= status < 400 else 0

            if last_health == 1:
                log("INFO", "Caddy is healthy", status=status, duration_ms=duration_ms)
            else:
                log("ERROR", "Caddy returned bad status", status=status, duration_ms=duration_ms)

    except HTTPError as e:
        duration_ms = round((time.time() - start) * 1000, 2)
        last_health = 0
        last_status_code = e.code
        last_response_time_ms = duration_ms
        log("ERROR", "HTTP error while checking Caddy", status=e.code, duration_ms=duration_ms)

    except URLError as e:
        duration_ms = round((time.time() - start) * 1000, 2)
        last_health = 0
        last_status_code = 0
        last_response_time_ms = duration_ms
        log("ERROR", "Connection error while checking Caddy", error=str(e.reason), duration_ms=duration_ms)

    except Exception as e:
        duration_ms = round((time.time() - start) * 1000, 2)
        last_health = 0
        last_status_code = 0
        last_response_time_ms = duration_ms
        log("ERROR", "Unexpected error while checking Caddy", error=str(e), duration_ms=duration_ms)


class MetricsHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/metrics":
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"not found\n")
            return

        metrics = f"""# HELP caddy_checker_health Caddy health status. 1 means healthy, 0 means unhealthy.
# TYPE caddy_checker_health gauge
caddy_checker_health {last_health}

# HELP caddy_checker_response_time_ms Last Caddy response time in milliseconds.
# TYPE caddy_checker_response_time_ms gauge
caddy_checker_response_time_ms {last_response_time_ms}

# HELP caddy_checker_status_code Last HTTP status code returned by Caddy.
# TYPE caddy_checker_status_code gauge
caddy_checker_status_code {last_status_code}

# HELP caddy_checker_last_check_timestamp Unix timestamp of the last Caddy check.
# TYPE caddy_checker_last_check_timestamp gauge
caddy_checker_last_check_timestamp {last_check_timestamp}
"""

        self.send_response(200)
        self.send_header("Content-Type", "text/plain; version=0.0.4")
        self.end_headers()
        self.wfile.write(metrics.encode("utf-8"))

    def log_message(self, format, *args):
        return


def metrics_server():
    server = HTTPServer(("0.0.0.0", METRICS_PORT), MetricsHandler)
    log("INFO", "Metrics server started", port=METRICS_PORT)
    server.serve_forever()


def main():
    log("INFO", "Caddy checker exporter started")

    thread = threading.Thread(target=metrics_server, daemon=True)
    thread.start()

    while True:
        check()
        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log("INFO", "Caddy checker stopped")
        sys.exit(0)
